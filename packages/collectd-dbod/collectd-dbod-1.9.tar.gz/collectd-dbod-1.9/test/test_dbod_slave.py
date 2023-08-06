from mock import call
from dbod_plugin import DbodCollectdPlugin
from dbod_instances import DbodInstance, MalformedDbodInstance
from helpers import get_mocked_instance
from hypothesis import given, strategies as st, settings, HealthCheck
import mock
import pytest
patcher = mock.patch('dbod_plugin.DbodCollectdPlugin.__init__')
init = patcher.start()
init.return_value = None
from dbod_slave import DbodSlavePlugin # noqa
patcher.stop()


@pytest.fixture
def plugin(mocker):
    """
    Returns an instance of DbodCollectdPlugin with
    all the real things mocked:
        - plugin.helper mocked - the constructor
            opens the config files to read passwords etc.
        - plugin.read mocked - it calls helper.get_instances which
            sends a request DBOD API to get list of entities
    """
    # We mock init of the parent class because it calls collectd methods
    # to register read
    init = mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    init.return_value = None
    # Read from parent class would call DBOD API to get instances
    # running locally, we provide our own instances in the tests
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    mocker.patch('dbod_plugin.DbodCollectdPlugin.dispatch')
    from dbod_slave import DbodSlavePlugin
    p = DbodSlavePlugin()
    # Mock instances attribute - this noramlly comes from the DBOD API

    mocker.patch.object(p, 'helper', create=True)
    return p


def test_inheritance(mocker):
    """
    Test that DbodSlavePluign inherits from DbodCollectdPlugin
    and instance can be created (so it implements all the necessary methods)
    """
    init = mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    init.return_value = None
    s = DbodSlavePlugin()
    assert isinstance(s, DbodCollectdPlugin)


def test_read_calls_parent_read(mocker):
    """
    Test that DbodSlavePlugin.read() calls parent class read() method
    It has to be called to refresh instances from DBOD API
    """
    init = mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    read = mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    init.return_value = None
    s = DbodSlavePlugin()
    try:
        s.read()
    except Exception:
        pass
    read.assert_called()


def test_importing_calls_init():
    init.assert_called()


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.booleans(),
            active=st.booleans(),
            malformed=st.booleans(),
            exception=st.sampled_from([None]),
            select_value=st.integers(
                min_value=1, max_value=10),
            notification=st.booleans()),
        min_size=1,
        max_size=20
        )
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_instance_methods(mocker, plugin, instances):
    """
    Test that depending on the instance attributes (active, slave)
    correct methods are called
    Additionally, test that MalformedDbodInstance is not taken
    into account at all
    We should perform any action only if instance is slave
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    ##################################################
    plugin.read()
    # We iterate over mocked instances and check
    # that proper calls were made
    ##################################################
    for instance in instances:
        # Malformed instance shouldn't run anything
        if isinstance(instance, MalformedDbodInstance):
            instance.assert_not_called()
            continue
        # We should perform actions only on slave instances
        if not instance.slave:
            instance.assert_not_called()
            continue
        # We should connect and select from slave instances
        calls = [call.connect(),
                 call.get_replication_lag(),
                 call.disconnect()]
        instance.mock_calls == calls


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.just(True),
            active=st.just(True),
            malformed=st.just(False),
            exception=st.sampled_from([None]),
            select_value=st.integers(
                min_value=1, max_value=10),
            # Simulate get_replicaiton_lag returning
            # from 1 to 3000 seconds
            get_replication_lag_value=st.integers(1, 10),
            max_lag_seconds=st.integers(1, 10),
            notification=st.booleans()
            ),
        min_size=1,
        max_size=20
        ),
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_dispatch(mocker, plugin, instances):
    """
    Test that depending on the get_replicaiton_lag()
    and max_lag_seconds we dispatch a correct value

    No exceptions tested here
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    ##################################################
    plugin.dispatch.reset_mock()
    plugin.read()
    ##################################################
    # We collect ispatch calls here
    expected_calls = []
    # We iterate over mocked instances and check
    # that proper calls were made
    ##################################################
    log_dispatch = "| dbod_slave | {} | {:10} | [{}] | {}"

    for instance in instances:
        if instance.get_replication_lag() > instance.max_lag_seconds:
            expected_calls.append(call([1], instance.notification,
                log_dispatch.format("ERROR", instance.db_name,
                "-1", "Notifications disabled"),
                plugin_instance=instance.db_name))
        else:
            expected_calls.append(call([0], instance.notification,
                log_dispatch.format("INFO", instance.db_name,
                "-1", "Notifications disabled"),
                plugin_instance=instance.db_name))
    assert plugin.dispatch.mock_calls == expected_calls

@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.just(True),
            active=st.just(True),
            malformed=st.just(False),
            exception=st.sampled_from(
                ["connect", "disconnect", "get_replication_lag"]),
            select_value=st.integers(
                min_value=1, max_value=10),
            # Simulate get_replicaiton_lag returning
            # from 1 to 3000 seconds
            get_replication_lag_value=st.integers(1, 10),
            max_lag_seconds=st.integers(1, 10)
            ),
        min_size=1,
        max_size=20
        ),
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_dispatch_exceptions(mocker, plugin, instances):
    """
    Test that if any method raises exception we dispatch [1]
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    ##################################################
    plugin.read()
    ##################################################
    # We collect ispatch calls here
    expected_calls = []
    # We iterate over mocked instances and check
    # that proper calls were made
    ##################################################
    log_dispatch = "| dbod_slave | {} | {:10} | [{}] | {}"

    for instance in instances:
        # If no exception raised or disconnect raised an exception
        if not instance.exception or instance.exception == "disconnect":
            if instance.get_replication_lag() > instance.max_lag_seconds:
                expected_calls.append(
                    call([1], instance.notification,
                        log_dispatch.format("ERROR", instance.db_name,
                        "-1", "Notifications disabled"),
                        plugin_instance=instance.db_name))
            else:
                expected_calls.append(
                    call([0], instance.notification,
                        log_dispatch.format("INFO", instance.db_name,
                        "-1", "Notifications disabled"),
                        plugin_instance=instance.db_name))
        elif instance.exception in ["connect", "get_replication_lag"]:
            expected_calls.append(
                call([1], instance.notification,
                    log_dispatch.format("ERROR", instance.db_name,
                    "-1", "Notifications disabled"),
                    plugin_instance=instance.db_name))
    assert plugin.dispatch.mock_calls == expected_calls
    mocker.resetall()


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.just(True),
            active=st.just(True),
            malformed=st.just(False),
            exception=st.sampled_from(
                ["connect", "get_replication_lag", "disconnect", None]),
            select_value=st.integers(
                min_value=1, max_value=10),
            # Simulate get_replicaiton_lag returning
            # from 1 to 3000 seconds
            get_replication_lag_value=st.integers(1, 10),
            max_lag_seconds=st.integers(1, 10)
            ),
        min_size=1,
        max_size=20
        ),
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_update_state(mocker, plugin, instances):
    """
    Test that we call properly update_state, to update
    instance state in DBOD API
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    ##################################################
    plugin.helper.update_state.reset_mock()
    plugin.read()
    ##################################################
    # We collect ispatch calls here
    expected_calls = []
    # We iterate over mocked instances and check
    # that proper calls were made
    ##################################################
    for instance in instances:
        # If exception was raised on connection, or getting the lag
        # update instance to stopped
        if instance.exception and \
                instance.exception in ["connect", "get_replication_lag"]:
            expected_calls.append(call(instance, DbodInstance.STOPPED))
            continue
        if instance.get_replication_lag() > instance.max_lag_seconds:
            expected_calls.append(call(instance, DbodInstance.BUSY))
        else:
            expected_calls.append(call(instance, DbodInstance.RUNNING))
    assert plugin.helper.update_state.mock_calls == expected_calls


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(0, 4),
            slave=st.just(True),
            active=st.just(True),
            malformed=st.just(False),
            exception=st.sampled_from(
                ["connect", "get_replication_lag", "disconnect", None]),
            select_value=st.integers(
                min_value=1, max_value=5),
            # Simulate get_replicaiton_lag returning
            # from 1 to 3000 seconds
            get_replication_lag_value=st.integers(1, 10),
            max_lag_seconds=st.integers(1, 10),
            notification=st.booleans()
            ),
        min_size=1,
        max_size=20
        ),
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_logging(mocker, plugin, instances):
    """
    Test that messages are logged (errors) on dispatch
    """
    import collectd
    collectd.reset_mock()
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    plugin.helper.update_state.reset_mock()
    plugin.read()
    expected_calls_warning = []
    expected_calls_info = []
    expected_calls_error = []

    # We iterate over mocked instances and check
    # that proper calls to collectd.error() were made
    ##################################################
    log_dispatch = "| dbod_slave | {} | {:10} | [{}] | {}"
    #############
    for instance in instances:
        # If exception was raised on connection, or getting the lag
        # update instance to stopped
        if instance.exception and \
                instance.exception in ["connect", "get_replication_lag"]:
            expected_calls_error.append(
                call(log_dispatch.format(
                        "ERROR", instance.db_name,
                        "1", "Exception: %s" % instance.exception_message)))
            continue
        if instance.get_replication_lag() > instance.max_lag_seconds:
            expected_calls_error.append(
                call(log_dispatch.format(
                        "ERROR", instance.db_name,
                        "1", "Instance lags %s seconds behind master"
                        % instance.get_replication_lag_value)))
        if instance.exception == "disconnect":
            # log disconnect errors as debug
            expected_calls_warning.append(
                call(log_dispatch.format(
                        "WARNING", instance.db_name,
                        "", "Not able to disconnect: %s"
                        % instance.exception_message)))

    assert collectd.error.mock_calls == expected_calls_error
    assert collectd.info.mock_calls == expected_calls_info
    assert collectd.warning.mock_calls == expected_calls_warning
