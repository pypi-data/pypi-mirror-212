#!/usr/bin/python3

from dbod_helpers import DbodCollectdHelper, \
    DbodConfigException
from mock import MagicMock, call
from pytest import raises
import pytest
import requests
import json
import dbod_helpers
import dbod_instances
import yaml
import platform
PYTHON_VERSION = platform.python_version()
from pkg_resources import parse_version as version
import cerndb
from  pathlib import Path
import builtins

@pytest.fixture
def helper_mocks(mocker):
    """
    Mock all external libraries calls
    """

    mocker.patch('pathlib.Path.exists')
    path_mock = MagicMock()
    Path.exists = path_mock
    #Patch https://gitlab.cern.ch/db/python3-cerndb/-/blob/master/cerndb/config/__init__.py#L41
    path_mock.return_value = True
    mocker.patch('builtins.open')
    open_mock = MagicMock()
    builtins.open = open_mock
    #Patch https://gitlab.cern.ch/db/python3-cerndb/-/blob/master/cerndb/config/__init__.py#L52
    open_mock.return_value.__enter__.return_value = ('''
            api:
              cachefile: /some/cache/file.json
              host: https://some-url.cern.ch
              entity_endpoint: api/v1/instance
              cluster_member_endpoint: qa/api/v1/cluster-member
              user: dbod-api
              password: pass-api
            mysql:
              user: uu
              password: uu
            dbmon:
              user: uu
              password: uu
            dbod_database:
              db_name: itcore
              db_account: DBONDEMAND
              db_pwd: 12131
            influx2:
              client: /path/to/influx/client
            ''')
    mocker.patch('dbod_helpers.gethostname', create=True)
    dbod_helpers.gethostname.return_value = "dbod-test1.cern.ch"
    # Mock requests
    mocker.patch("requests.get")
    requests.get.return_value.status_code = 200
    # Mock instance
    mocker.patch('dbod_instances.DbodInstance.__init__')
    mocker.patch('dbod_instances.MySQLDbodInstance.__init__')
    mocker.patch('dbod_instances.PostgresDbodInstance.__init__')
    mocker.patch('dbod_instances.InfluxDbodInstance.__init__')
    mocker.patch('dbod_instances.MalformedDbodInstance.__init__')
    dbod_instances.MySQLDbodInstance.__init__.return_value = None
    dbod_instances.PostgresDbodInstance.__init__.return_value = None
    dbod_instances.InfluxDbodInstance.__init__.return_value = None
    dbod_instances.MalformedDbodInstance.__init__.return_value = None
    dbod_instances.DbodInstance.__init__.return_value = None

    return {"open_mock": open_mock}


def test_dbod_helper_reads_config(mocker, helper_mocks):
    """
    Test a method to get the "source of truth"
    """
    # Test configuration was read
    h = DbodCollectdHelper()
    assert h.cachefile == "/some/cache/file.json"
    assert h.api_url == 'https://some-url.cern.ch'
    assert h.api_user == 'dbod-api'
    assert h.api_password == 'pass-api'
    assert h.user == 'uu'



def test_dbod_helper_reads_config_malformed(mocker, helper_mocks):
    """
    Test a method to get the "source of truth"
    May it be YAML from the disk
    """
    # Test configuration was read
    helper_mocks["open_mock"].return_value.__enter__.return_value  = ('''a''')
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file (config.yaml):" \
                             " missing key 'api'"
    ##########################################################
    helper_mocks["open_mock"].return_value.__enter__.return_value = ('''
            api:
            ''')
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file (config.yaml): missing nested key"

    ##########################################################

    helper_mocks["open_mock"].return_value.__enter__.return_value = ('''
            api:
              cachefile: /some/cache/file.json
              host: https://some-url.cern.ch
            ''')
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "Error in DBOD config file (config.yaml): " \
                             "missing key 'entity_endpoint'"
    ##########################################################
    helper_mocks["open_mock"].return_value.__enter__.side_effect =  FileNotFoundError("sth wrong")
    with raises(DbodConfigException) as exc:
        DbodCollectdHelper()
    assert str(exc.value) == "sth wrong"


@pytest.fixture
def instances_from_json(helper_mocks, mocker):
    requests.get.return_value.status_code = 404

    mocker.patch('dbod_helpers.open')
    mocker.patch('json.load')
    json.load.return_value = [
            {"instance": "1", "type": "PG", "state": "RUNNING"},
            {"instance": "2", "type": "MYSQL", "state": "RUNNING"},
            {"instance": "3", "type": "InfluxDB", "state": "RUNNING"}
        ]

    open_file = MagicMock()
    dbod_helpers.open.return_value.__enter__.return_value = open_file

def test_get_instances_from_json(mocker, tmpdir, instances_from_json):
    """
    use entities.json
    """

    h = DbodCollectdHelper()
    instances = h.get_instances()
    json.load.assert_called_with(
        dbod_helpers.open.return_value.__enter__.return_value)
    dbod_helpers.open.assert_called_with(h.cachefile)
    assert dbod_instances.MySQLDbodInstance.__init__. \
        mock_calls == [call({"instance": "2", "type": "MYSQL", "state": "RUNNING"},
                            influx2_client="/path/to/influx/client", user="uu", password="uu")]
    assert dbod_instances.PostgresDbodInstance.__init__. \
        mock_calls == [call({"instance": "1", "type": "PG", "state": "RUNNING"},
                            influx2_client="/path/to/influx/client", user="uu", password="uu")]
    assert dbod_instances.InfluxDbodInstance.__init__. \
        mock_calls == [call({"instance": "3", "type": "InfluxDB", "state": "RUNNING"},
                            influx2_client="/path/to/influx/client", user="uu", password="uu")]
    assert len(instances) == 3

def test_get_instances_instance_raises_exception(
        mocker, tmpdir, instances_from_json):
    """
    When DbodInstance creation raises exception - we should get
        MalformedDbodInstance
    """
    dbod_instances.MySQLDbodInstance.__init__.side_effect = \
        dbod_helpers.EntityMalformedException("sth wrong")
    h = DbodCollectdHelper()
    instances = h.get_instances()
    assert dbod_instances.MalformedDbodInstance.__init__. \
        mock_calls == [call({"instance": "2", "type": "MYSQL", "state": "RUNNING"},
                            user="uu", password="uu")]
    assert len(instances) == 3
    assert isinstance(instances[1], dbod_instances.MalformedDbodInstance)

def test_get_instances_request_raises_exception_use_json(
        mocker, tmpdir, instances_from_json):
    requests.get.side_effect = requests.ConnectionError("Something wrong")
    h = DbodCollectdHelper()
    instances = h.get_instances()
    json.load.assert_called_with(
        dbod_helpers.open.return_value.__enter__.return_value)
    assert len(instances) == 3



def test_get_instances_type_missing(mocker, tmpdir, instances_from_json):
    """
    Test get_instances reading entities.json and failing with type missing
        Then it creates a list of DbodInstance object
        which is returned
    """
    mocker.patch('dbod_helpers.open')
    mocker.patch('json.load')
    json.load.return_value = [
            {"instance": "1", "type": "MYSQL", "state": "RUNNING"},
            {"instance": "2", "type": "InfluxDB", "state": "RUNNING"},
            {"instance": "3", "type": "MYSQL", "state": "RUNNING"},
            {"instance": "4", "state": "RUNNING"}
        ]

    open_file = MagicMock()
    dbod_helpers.open.return_value.__enter__.return_value = open_file
    h = DbodCollectdHelper()
    instances = h.get_instances()
    assert len(instances) == 4
    assert dbod_instances.MalformedDbodInstance.__init__. \
        mock_calls == [call({"instance": "4", "state": "RUNNING"},
                            password='uu', user='uu')]
    assert isinstance(instances[3], dbod_instances.MalformedDbodInstance)


@pytest.mark.parametrize(
    "state,api_url,endpoint,id,status_code,current_state",
    [("STOPPED", "api.cern.ch:3", "api/test", "db1",
      204, "RUNNING"),
     ("RUNNING", "a.c/232", "api/ent", "db2",
      204, "RUNNING"),
     ("BUSY", "test-api:33", "api/entities", "db3",
      200, "RUNNING"),
     ("RUNNING", "test-api:33", "api/entities", "db5",
      200, "AWAITING_APPROVAL"),
     ("BUSY", "test-api:33", "api/entities", "db4",
      200, "MAINTENANCE"),
     ])
def test_update_state(mocker, state, api_url, endpoint, id,
                       status_code, current_state,test_entities_file_name):
    init = mocker.patch('dbod_helpers.DbodCollectdHelper.__init__')
    init.return_value = None
    helper = DbodCollectdHelper()
    helper.api_url = api_url
    helper.instance_endpoint = endpoint
    helper.api_user = "user"
    helper.api_password = "pass"
    helper.cachefile = test_entities_file_name

    import requests
    import collectd
    mocker.resetall()
    requests.put.reset_mock()

    class Instance:
        pass
    instance = Instance()
    instance.id = id
    instance.db_name = id
    instance.state = current_state
    expected_url = "%s/%s/%s" % (api_url, endpoint, id)
    requests.put.return_value.status_code = status_code
    helper.update_state(instance, state)

    if current_state in ["AWAITING_APPROVAL", "MAINTENANCE"]:
        requests.put.assert_not_called()
        collectd.debug.assert_called_with(
            "Not updating state of %s. Instance state: %s"
            % (instance.db_name, current_state))
    elif current_state == state:
        requests.put.assert_not_called()
        collectd.debug("Instance %s state [%s] has not changed"
                        % (instance.db_name, instance.state))
    else:
        collectd.debug("Updating %s instance state to: %s"
                        % (instance.db_name, instance.state))
        expected_url = "%s/%s/%s" % (api_url,
                                    endpoint,
                                    instance.id)

        data_to_post = {"state": state}
        headers={'auth': '{ "admin" : true , "groups" : [ ] , "owner" : "collectd" }'}
        requests.put.assert_called_with(
            expected_url,
            headers=headers,
            auth=(helper.api_user, helper.api_password),
            json=data_to_post,
            verify=False
            )
        if status_code != 204:
            collectd.error.assert_called_with(
                "Failed updating state of %s. Response code %s, url %s, self.api_url %s, self.instance_endpoint %s, headers %s"
                % (instance.db_name, status_code, expected_url, api_url, endpoint, headers))

