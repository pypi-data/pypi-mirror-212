from dbod_instances import DbodInstance, EntityMalformedException, \
    MySQLDbodInstance, PostgresDbodInstance, InfluxDbodInstance, \
    MalformedDbodInstance, StatusCodeException
from hypothesis import given, strategies as st, settings, HealthCheck
from pytest import raises
from mock import MagicMock, call
import dbod_instances
import pytest
import subprocess


class FakePopen(object):
    def __init__(self, args, stdout=None):
        super().__init__()
        self.args = args
        self.stdout = stdout

    def communicate(self):
        return "OK"


@pytest.fixture
def instance():
    """
    Dummy implementation of DbodInstance
    """
    class Instance(DbodInstance):
        def connect(self):
            pass

        def disconnect(self):
            pass

        def execute(self):
            pass

    return Instance


def test_dbod_instance_is_abstract():
    """
    DbodInstance is an abstract class, specific implementations
    include:
        - MySQLDbodInstance
        - PostgresDbodInstance
        - InfluxDbodInstance
        - MalformedDbodInstance - on missing data in dbod api
    """
    with raises(TypeError) as e:
        DbodInstance({})
    assert "Can't instantiate abstract class" in str(e.value)


def test_subclass_of_dbod_instance_must_implement(mocker):
    mocker.patch('dbod_instances.DbodInstance.__init__')
    DbodInstance.__init__.return_value = None

    class SubclassTest(DbodInstance):
        pass
    ##################################
    # connect()
    with raises(TypeError) as e:
        SubclassTest()
    assert "Can't instantiate abstract class SubclassTest with " \
        "abstract methods connect" in str(e.value)


def test_dbod_instance_init(test_instance1, mocker, instance):
    """
    Test it has all necessary fields
    """
    # To test what __init__ of DbodInstance does we create a subclass
    i = instance(test_instance1)
    # Name is concatenation of db_name
    assert i.instance == "dbod-test-db1.cern.ch"
    assert i.port == 6604
    assert i.db_name == "test_db1"
    assert i.db_type == "PG"
    assert i.socket == "/var/lib/pgsql/"
    assert i.category == "TEST"
    assert i.notification is True
    assert i.slave is False
    assert i.active is True
    assert i.state == "RUNNING"
    test_instance1["attributes"]["slave"] = True
    i = instance(test_instance1)
    assert i.slave is True
    test_instance1["attributes"]["notifications"] = True
    i = instance(test_instance1)
    assert i.notification is True
    # Assert connect and query methods are defined
    assert i.connect
    assert i.execute
    mocker.patch.object(i, 'execute')
    i.insert("insert sth")
    i.create("create sth")
    assert i.execute.mock_calls == [call("insert sth"), call("create sth")]

# Don't remove db_type, as it fails with the new API
@pytest.mark.parametrize(
    "key",
    ["db_name", "port", "socket", "class", "active", "state"])
def test_dbod_instance_init_missing_key(test_instance1, key, instance):
    """
    Test that it raises a proper exception on initialization
        EntityMalformedException
    Inside of this exception we should see what key was missing
    """
    del test_instance1[key]

    with raises(EntityMalformedException) as e:
        instance(test_instance1)
    assert str(e.value) == \
        "Attribute %s missing from the metadata! (DBOD API)" % key


@pytest.mark.parametrize(
    "key",
    ["notifications"])
def test_dbod_instance_init_missing_attribute(test_instance1, instance, key):
    """
    Test that it raises a proper exception on initialization
        EntityMalformedException
    Inside of this exception we should see what key was missing
    """
    del test_instance1["attributes"][key]

    with raises(EntityMalformedException) as e:
        instance(test_instance1)
    assert str(e.value) == \
        "Attribute %s missing from the metadata! (DBOD API)" % key


@pytest.mark.parametrize(
    "key,value,is_attr",
    [
        ("port", "1234gf", False),
        ("notifications", "notTrue", True),
        ("slave", "something", True)
    ])
def test_dbod_instance_init_incorrect_value_from_api(
        test_instance1, instance, key, value, is_attr):
    """
    Test that it raises a proper exception on initialization
        EntityMalformedException
    Inside of this exception we should see what key was missing
    """
    if is_attr:
        test_instance1["attributes"][key] = value
    else:
        test_instance1[key] = value

    with raises(EntityMalformedException) as e:
        instance(test_instance1)
    print(e.value)
    assert str(e.value).startswith(
        "Attribute %s has incorrect value! (DBOD API metadata)" % key)


def test_specific_implementation_exist(mocker):
    """
    Test that there are implementations of DbodInstance
    for each of the database, and they call the parent class __init__
    """
    mocker.patch('dbod_instances.DbodInstance.__init__')
    dbod_instances.DbodInstance.__init__.return_value = None
    some_dict = {}
    MySQLDbodInstance(some_dict)
    dbod_instances.DbodInstance.__init__.assert_called_with(some_dict)
    dbod_instances.DbodInstance.__init__.reset_mock()

    PostgresDbodInstance(some_dict)
    dbod_instances.DbodInstance.__init__.assert_called_with(some_dict)
    dbod_instances.DbodInstance.__init__.reset_mock()
    InfluxDbodInstance(some_dict)
    dbod_instances.DbodInstance.__init__.assert_called_with(some_dict)
    dbod_instances.DbodInstance.__init__.reset_mock()
    i = MalformedDbodInstance(some_dict)
    assert i.api_dict == some_dict
    dbod_instances.DbodInstance.__init__.assert_not_called()


def test_mapping_of_db_type_defined(mocker):
    """
    Test that there is a dict that maps db_type to class
    """
    from dbod_instances import instance_types
    assert instance_types["PG"] == PostgresDbodInstance
    assert instance_types["MYSQL"] == MySQLDbodInstance
    assert instance_types["InfluxDB"] == InfluxDbodInstance


def test_malformed_instance_keeps_state(mocker):
    """
    Test that MalformedInstance has state attribute
        - set to unknown in case of errors
    """
    api_dict = {}
    i = MalformedDbodInstance(api_dict)
    assert i.state == "UNKNOWN"
    api_dict = {"state": "AWAITING_APPROVAL"}
    i = MalformedDbodInstance(api_dict)
    assert i.state == "AWAITING_APPROVAL"


def test_dbod_instance_has_states():
    """
    Test that you can use DbodInstance.STOPPED
    """
    assert DbodInstance.STOPPED == "STOPPED"
    assert DbodInstance.RUNNING == "RUNNING"
    assert DbodInstance.BUSY == "BUSY"


######################################################
# POSTGRES
######################################################
def test_postgres_instance_has_plugin_queries():
    """
    PostgresDbodInstance should have:
        - ping_insert_query
        - ping_select_query
        - ping_create_query
        - ping_delete_query
        - slave_lag_query
    """
    assert PostgresDbodInstance.ping_insert_query ==\
        "INSERT INTO collectd_ping VALUES ({0});"
    assert PostgresDbodInstance.ping_select_query ==\
        "SELECT * FROM collectd_ping;"
    assert PostgresDbodInstance.ping_create_query is None
    assert PostgresDbodInstance.ping_delete_query ==\
        "DELETE FROM collectd_ping;"
    assert PostgresDbodInstance.slave_lag_query ==\
        "SELECT CASE WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0::int ELSE " \
                "EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())::int END AS time_lag;"

@pytest.mark.parametrize(
    "user,password,host,port",
    [
        ("user1", "pass1", "host-dbod1.cern.ch", "6060"),
        ("user2", "pass333", "host-dbod2.cern.ch", "60"),
        ("user3", "pass324", "host-dbod3.cern.ch", "16060")
    ])
def test_postgres_instance(mocker, user, password, host, port):
    """
    Test Postgres instance, it should have
        - connect()
        - insert(table, )
        - select()
        - create()
    """
    import psycopg2
    pginit = mocker.patch('dbod_instances.PostgresDbodInstance.__init__')
    pginit.return_value = None

    p = PostgresDbodInstance()
    mocker.patch.object(p, 'user', user, create=True)
    mocker.patch.object(p, 'password', password, create=True)
    mocker.patch.object(p, 'instance', host, create=True)
    mocker.patch.object(p, 'port', port, create=True)
    connect_result = MagicMock()
    psycopg2.connect.return_value = connect_result
    ############################################
    # Connect
    ############################################
    p.connect()

    psycopg2.connect.assert_called_with(
        database="dod_dbmon",
        user=p.user,
        password=p.password,
        host="/var/lib/pgsql/",
        port=p.port)
    assert p.connection == connect_result
    ############################################
    # Execute
    ############################################
    cursor = MagicMock()
    connect_result.cursor.return_value = cursor

    result = p.execute("INSERT SOMETHING")
    connect_result.cursor.assert_called()
    cursor.execute.assert_called_with("INSERT SOMETHING")
    connect_result.commit.assert_called()
    cursor.close.assert_called()
    assert result is None
    ############################################
    # Select
    ############################################
    cursor = MagicMock()
    connect_result.cursor.return_value = cursor
    fetchall = MagicMock()
    cursor.fetchall = fetchall
    fetchall.return_value = (["10"],)
    result = p.select("select SOMETHING")
    connect_result.cursor.assert_called()
    cursor.fetchall.assert_called()
    cursor.close.assert_called()
    assert result == "10"
    ############################################
    # Disconnect
    ############################################
    p.disconnect()
    connect_result.close.assert_called()


######################################################
# MySQL
######################################################

def test_mysql_instance_has_plugin_queries():
    """
    PostgresDbodInstance should have:
        - ping_insert_query
        - ping_select_query
        - ping_create_query
        - ping_delete_query
    """
    assert MySQLDbodInstance.ping_insert_query ==\
        "INSERT INTO collectd_ping VALUES ({0});"
    assert MySQLDbodInstance.ping_select_query ==\
        "SELECT * FROM collectd_ping;"
    assert MySQLDbodInstance.ping_create_query is None
    assert MySQLDbodInstance.ping_delete_query ==\
        "DELETE FROM collectd_ping;"
    assert MySQLDbodInstance.slave_lag_query ==\
        "SHOW SLAVE STATUS"


@pytest.mark.parametrize(
    "user,password,socket,port",
    [
        ("user1", "pass1", "/var/lib/host-dbod1.cern.ch", "6060"),
        ("user2", "pass333", "/var/lib/host-dbod2.cern.ch", "60"),
        ("user3", "pass324", "/var/lib/host-dbod3.cern.ch", "16060")
    ])
def test_mysql_instance(mocker, user, password, socket, port):
    """
    Test Postgres instance, it should have
        - connect()
        - insert(table, )
        - select()
        - create()
    """
    import pymysql
    pginit = mocker.patch('dbod_instances.MySQLDbodInstance.__init__')
    pginit.return_value = None

    p = MySQLDbodInstance()
    mocker.patch.object(p, 'user', user, create=True)
    mocker.patch.object(p, 'password', password, create=True)
    mocker.patch.object(p, 'socket', socket, create=True)
    mocker.patch.object(p, 'port', port, create=True)
    connection = MagicMock()
    pymysql.connect.return_value = connection
    ############################################
    # Connect
    ############################################
    p.connect()

    pymysql.connect.assert_called_with(
        unix_socket=p.socket,
        user=p.user,
        passwd=p.password,
        db="dod_dbmon",
        port=p.port,
        connect_timeout=10)
    assert p.connection == connection
    ############################################
    # Execute
    ############################################
    cursor = MagicMock()
    cursor.execute.return_value = "QUERY RESULT"
    connection.cursor.return_value = cursor

    result = p.execute("INSERT SOMETHING")
    connection.cursor.assert_called()

    cursor.execute.assert_called_with("INSERT SOMETHING")
    connection.commit.assert_called()
    cursor.close.assert_called()
    assert result is None
    ############################################
    # Select
    ############################################
    mocker.resetall()
    cursor = MagicMock()
    cursor.fetchall.return_value = (["QUERY RESULT"],)
    connection.cursor.return_value = cursor

    result = p.select("select SOMETHING")
    connection.cursor.assert_called()
    cursor.fetchall.assert_called()

    cursor.execute.assert_called_with("select SOMETHING")
    cursor.close.assert_called()
    assert result == "QUERY RESULT"

    ############################################
    # Disconnect
    ############################################
    p.disconnect()
    connection.close.assert_called()


def test_instance_accepts_user_and_pass(test_instance1, instance):
    i = instance(test_instance1, "user", "password")
    assert i.user == "user"
    assert i.password == "password"
    i = instance(test_instance1)
    with raises(AttributeError):
        i.user
    with raises(AttributeError):
        i.password


######################################################
# InfluxDB
######################################################

def test_influx_instance_has_plugin_queries():
    """
    InfluxDbodInstance should have:
        - ping_insert_query
        - ping_select_query
        - ping_create_query
    """
    assert InfluxDbodInstance.ping_insert_query ==\
        "collectd_ping,measurement=ping value={0}"
    assert InfluxDbodInstance.ping_select_query ==\
        "q=select * from collectd_ping order by time desc limit 1"
    assert InfluxDbodInstance.ping_create_query is None
    assert InfluxDbodInstance.ping_delete_query is None


@pytest.mark.parametrize(
    "user,password,instance,port,status_code,db_version,bindir",
    [
        ("user1", "pass1", "host-dbod1.cern.ch", "6060", 200, "1.8.2", "/usr/local/influxdb/influxdb-2.0.4"),
        ("user2", "pass333", "host-dbod2.cern.ch", "60", 200, "2.0.4", "/usr/local/influxdb/influxdb-2.0.4"),
        ("user3", "pass324", "host-dbod3.cern.ch", "16060", 203, "1.7.3", "/usr/local/influxdb/influxdb-2.0.4")
    ])
def test_influx_instance(mocker, user, password, instance, port, status_code, db_version, bindir):
    """
    Test Influx instance, it should have
        - connect()
        - insert(table, )
        - select()
        - create()
    It uses HTTP API to manipulat the data!
    """
    import requests
    init = mocker.patch('dbod_instances.InfluxDbodInstance.__init__')
    requests.get.return_value.status_code = status_code
    requests.get.return_value.json.return_value =\
        {"results": [{"series": [
            {"values": [["12/02/2019", "ping", 12345]]}]}]}
    init.return_value = None

    p = InfluxDbodInstance()
    mocker.patch.object(p, 'user', user, create=True)
    mocker.patch.object(p, 'password', password, create=True)
    mocker.patch.object(p, 'instance', instance, create=True)
    mocker.patch.object(p, 'port', port, create=True)
    mocker.patch.object(p, 'db_version', db_version, create=True)
    mocker.patch.object(p, 'bindir', bindir, create=True)
    ############################
    # Connect, shouldn't do anything
    ############################
    p.connect()
    requests.assert_not_called()
    p.execute("query")
    requests.assert_not_called()
    p.create("query")
    requests.assert_not_called()

    ######################################
    # select()
    ######################################
    if db_version[0] == "1":
        if status_code == 200:
            result = p.select("my query")
            assert result == 12345
        else:
            with raises(StatusCodeException) as exc:
                p.select("my query")
            assert "Error executing GET statement on %s instance."\
                " Response code was: %s" % (p.instance, status_code)\
                in str(exc.value)
        url = "https://%s:%s/query?db=dod_dbmon" % (instance, port)
        requests.get.assert_called_with(
            url, auth=(user, password), params="my query",
            verify=False, timeout=10)
    else:
        def fake_communicate(a):
            return "OK"
        subprocess.Popen = FakePopen
        subprocess.Popen.communicate = fake_communicate
        stdout = "12345"
        stderr = None
        if stderr:
            with raises(StatusCodeException) as exc:
                p.select("my query")
            assert "Error pinging instance %s. Response code was: %s"\
                % (p.instance, "err")
        else:
            assert stdout == "12345"

    ######################################
    # insert()
    ######################################
    # In case of insert 204 is the proper code
    status_code += 4
    requests.post.return_value.status_code = status_code
    if db_version[0] == "1":
        if status_code == 204:
            p.insert("my query")
        else:
            with raises(StatusCodeException) as exc:
                p.insert("my query")
            assert "Error executing POST statement on %s instance."\
                " Response code was: %s" % (p.instance, status_code)\
                in str(exc.value)
        url = "https://%s:%s/write?db=dod_dbmon" % (instance, port)
        requests.post.assert_called_with(
            url, auth=(user, password), data="my query",
            verify=False, timeout=10)
    else:
        p.insert("my query value=%s" % status_code)


def test_dbod_instance_has_get_replication_lag(mocker):
    """
    The basic implementation of get_replication_lag should just call select
    with slave_query
    """
    select = mocker.patch("dbod_instances.DbodInstance.select")
    init = mocker.patch("dbod_instances.DbodInstance.__init__")
    init.return_value = None
    select.return_value = 3

    class Test(DbodInstance):
        slave_lag_query = "select * from test"

        def connect(self):
            pass
    t = Test()
    assert t.get_replication_lag() == 3
    select.assert_called_with(t.slave_lag_query)


@pytest.mark.parametrize(
    "result,lag",
    [
        ("RESULT1", 2),
        (("Tuple result", 2), 10),
        (("Tuple", 3), 100)
    ])
def test_mysql_implementation_of_get_replication_lag(mocker, result, lag):
    init = mocker.patch("dbod_instances.DbodInstance.__init__")
    init.return_value = None
    izip = mocker.patch("dbod_instances.zip")
    izip.return_value = {"Seconds_Behind_Master": lag}
    i = MySQLDbodInstance()
    connection = mocker.patch.object(i, "connection", create=True)
    connection.cursor.return_value.fetchone.return_value = result
    connection.cursor.return_value.description = \
        (('Slave', 0, 1), ('Master', 0, 2))
    selected_lag = i.get_replication_lag()
    assert connection.mock_calls == [
        call.cursor(),
        call.cursor().execute(i.slave_lag_query),
        call.cursor().fetchone(),
        call.commit(),
        call.cursor().close()
    ]
    izip.assert_called_with(['Slave', 'Master'], result)
    assert lag == selected_lag


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


@st.composite
def apidict(draw):
    """
    Generate dicitonary for a given entity, to simulate
    data as it comes from DBOD API or entities.json
    """
    api_dict = st.fixed_dictionaries(
        {
            "db_name": st.just("dbod"),
            "db_type": st.sampled_from(["PG", "MYSQL", "InfluxDB"]),
            "port": st.integers(1000, 3000),
            "socket": st.sampled_from(["/var/lib/mysql.socket",
                                       "/tmp/some.socket"]),
            "class": st.just("TEST"),
            "attributes": st.just({}),
            "active": st.booleans(),
            "state": st.sampled_from(["RUNNING", "BUSY", "STOPPED"]),
            "version": st.sampled_from(["1.7.3", "1.8.2", "2.0.4"]),
            "bindir": st.just("/usr/local/influxdb/influxdb-2.0.4")
            }
        )
    # Simulate missing attributes
    notifications = st.dictionaries(
        keys=st.just("notifications"),
        values=st.sampled_from(["true", "false"])
    )
    monit_notif_max_lag_seconds = st.dictionaries(
        keys=st.just("monit_notif_max_lag_seconds"),
        values=st.integers(100, 1000)
    )

    optional1 = draw(notifications)
    optional2 = draw(monit_notif_max_lag_seconds)

    api = draw(api_dict)
    api["attributes"] = merge_two_dicts(optional1, optional2)

    return api


@given(apidict())
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_max_lag_seconds(mocker, api_dict):
    """
    Test that DBOD Instance has max_lag_seconds attribute
    apidict() generates random test cases simulating dictionary
    as it comes from DBOD API or entities.json
    """
    mocker.resetall()
    class TestInstance(DbodInstance):
        def connect(self):
            pass

    # Fill missing pieces, that we're not interested in this test
    # api_dict will randomly make them empty or not defined
    api_dict["attributes"]["notifications"] = "true"
    api_dict["cluster_type"] = None
    api_dict["role"] = None
    t = TestInstance(api_dict)

    try:
        # If attribute defined in the dict, assert that object attribute is
        # set to proper value
        seconds = api_dict['attributes']['monit_notif_max_lag_seconds']
        assert t.max_lag_seconds == seconds
    except KeyError:
        # Assert default value was used
        assert t.max_lag_seconds == 300
