import dbod_plugin
import pytest
import string
from hypothesis import given, strategies as st, settings, HealthCheck
from mock import call
from dbod_instances import MalformedDbodInstance
from helpers import get_mocked_instance


def test_dbod_plugin(mocker):
    """
    Test that DbodCollectdPluginPing is a subclass of DbodCollectdPlugin
    """
    mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    dbod_plugin.DbodCollectdPlugin.__init__.return_value = None
    from dbod_ping import DbodCollectdPluginPing
    i = DbodCollectdPluginPing()
    assert isinstance(i, dbod_plugin.DbodCollectdPlugin)


def test_read_calls_parent_read(mocker):
    """
    Parent class read must be called to refresh instances data
    """
    mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    dbod_plugin.DbodCollectdPlugin.__init__.return_value = None
    from dbod_ping import DbodCollectdPluginPing

    plugin = DbodCollectdPluginPing()
    try:
        plugin.read()
    except: # noqa
        pass

    dbod_plugin.DbodCollectdPlugin.read.assert_called()


@pytest.fixture()
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
    mocker.resetall()
    init = mocker.patch('dbod_plugin.DbodCollectdPlugin.__init__')
    init.return_value = None
    # Read from parent class would call DBOD API to get instances
    # running locally, we provide our own instances in the tests
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    mocker.patch('dbod_plugin.DbodCollectdPlugin.dispatch')
    from dbod_ping import DbodCollectdPluginPing
    p = DbodCollectdPluginPing()
    # Mock instances attribute - this noramlly comes from the DBOD API

    mocker.patch.object(p, 'helper', create=True)
    return p


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
            notification=st.booleans()
            ),
        min_size=1,
        max_size=20
        ),
    # Simulate output of time.time() that we insert
    time_val=st.integers(min_value=1, max_value=10)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_instance_methods(mocker, plugin, instances, time_val):
    """
    Test that depending on the instance attributes (ative, slave)
    correct methods are called
    Additionally, test that MalformedDbodInstance is not taken
    into account at all
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    # mock time call
    time = mocker.patch('dbod_ping.time')
    time.return_value = time_val
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
        # Not active instance or slave. We shouldn't connect
        if instance.slave or not instance.active:
            instance.assert_not_called()
            continue
        # We should create, insert and select to not slave instances
        calls = [call.connect(),
                 call.create(instance.ping_create_query),
                 call.execute(instance.ping_delete_query),
                 call.ping_insert_query.format(time_val),
                 call.insert(instance.ping_insert_query.format()),
                 call.select(instance.ping_select_query),
                 call.disconnect()]
        instance.mock_calls == calls


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
        ),
    # Simulate output of time.time() that we insert
    time_val=st.integers(min_value=1, max_value=10)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_dispatch(mocker, plugin, instances, time_val):
    """
    Test that depending on the instance attributes (ative, slave),
    raised exceptions and inserted/selected value
    correct value is dispatched to collectd
    """
    #########################################
    # Mock various things
    #########################################
    # plugin.instances normally comes from DBOD API,
    # here we set it to mocks generated with hypothesis
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    plugin.dispatch.reset_mock()
    # mock time call
    time = mocker.patch('dbod_ping.time')
    time.return_value = time_val
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    plugin.read()
    ##################################################
    # We collect all calls to dispatch here
    dispatch_calls = []
    # We iterate over mocked instances and check
    # that proper calls to dispatch were made
    ##################################################
    log_dispatch = "| dbod_ping | {} | {:10} | [{}] | {}"
    for instance in instances:
        # Malformed instance should be skipped in the ping plugin
        # there is another plugin for them
        if isinstance(instance, MalformedDbodInstance):
            continue
        # Not active instance we send -1
        if not instance.active:
            dispatch_calls.append(
                call([-1], instance.notification,
                    log_dispatch.format("INFO", instance.db_name,
                    "-1", "Instance not active."),
                    plugin_instance=instance.db_name))
            continue

        if not instance.slave:
            # If inserted value = selected value we dispatch 0,
            # otherwise we dispatch 1
            if time_val == instance.select_value:
                dispatch_calls.append(
                    call([0], instance.notification,
                        log_dispatch.format("INFO", instance.db_name,
                        "-1", "Notifications disabled"),
                        plugin_instance=instance.db_name))
            else:
                dispatch_calls.append(
                    call([1], instance.notification,
                        log_dispatch.format("ERROR", instance.db_name,
                        "-1", "Notifications disabled"),
                        plugin_instance=instance.db_name))

    assert plugin.dispatch.mock_calls == dispatch_calls

@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
           get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.booleans(),
            active=st.just(True),
            # No Malformed instances in this test
            malformed=st.just(False),
            # simulate exception in one of the methods
            exception=st.sampled_from(
                ["connect", "insert", None, "select", "create", "execute",
                 "disconnect"]),
            # Select always returns 100 as we're testing exceptions
            select_value=st.just(100)),
        min_size=1,
        max_size=20
        ),
    # Simulate output of time.time() that we insert
    time_val=st.just(100)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_dispatch_exceptions(mocker, plugin, instances, time_val):
    """
    Test that if any of the instance methods
    (connect, insert, select, disconnect...)
    raises an exception, the plugin will dispatch a correct value
    """
    #########################################
    # Mock
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    plugin.dispatch.reset_mock()
    # mock time call
    time = mocker.patch('dbod_ping.time')
    time.return_value = time_val
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    plugin.read()
    ##################################################
    # We collect all calls to dispatch here
    dispatch_calls = []
    # We iterate over mocked instances and check
    # that proper calls to dispatch were made
    ##################################################
    log_dispatch = "| dbod_ping | {} | {:10} | [{}] | {}"

    for instance in instances:
        if not instance.active:
            dispatch_calls.append(
                call([-1], instance.notification,
                    log_dispatch.format("INFO", instance.db_name,
                    "-1", "Instance not active."),
                    plugin_instance=instance.db_name))
            continue

        if instance.slave:
            continue

        # if any method raises an exception we should dispatch 1
        # apart from the disconnect, which we consider not critical
        if instance.exception:
            if instance.exception != "disconnect":
                dispatch_calls.append(
                    call([1], instance.notification,
                        log_dispatch.format("ERROR", instance.db_name,
                        "-1", "Notifications disabled"),
                        plugin_instance=instance.db_name))
                continue

        dispatch_calls.append(
            call([0], instance.notification,
                log_dispatch.format("INFO", instance.db_name,
                "-1", "Notifications disabled"),
                plugin_instance=instance.db_name))

    assert plugin.dispatch.mock_calls == dispatch_calls


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.booleans(),
            active=st.just(True),
            # No Malformed instances in this test
            malformed=st.booleans(),
            # simulate exception in one of the methods
            exception=st.sampled_from(
                ["connect", "insert", None, "select", "create", "execute",
                 "disconnect"]),
            # Select always returns 100 as we're testing exceptions
            select_value=st.integers(
                min_value=1,
                max_value=10
                )),
        min_size=1,
        max_size=20
        ),
    # Simulate output of time.time() that we insert
    time_val=st.integers(min_value=1, max_value=10)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_updating_dbod_state(mocker, plugin, instances, time_val):
    """
    Test that instance state is correctly updated in the DBOD API
    """
    #########################################
    # Mock
    mocker.resetall()
    mocker.patch.object(plugin, 'instances', instances, create=True)
    plugin.helper.update_state.reset_mock()
    # mock time call
    time = mocker.patch('dbod_ping.time')
    time.return_value = time_val
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    plugin.read()
    ##################################################
    # We collect all calls to dispatch here
    update_state_calls = []
    # We iterate over mocked instances and check
    # that proper calls to update_state were made
    ##################################################
    from dbod_instances import DbodInstance
    for instance in instances:
        if isinstance(instance, MalformedDbodInstance):
            continue
        if instance.slave:
            continue

        # state in ping, only for master instances
        if not instance.exception or instance.exception == "disconnect":
            # If no exception was raise we should compare the inserted
            # and selected values. If they match, we update state to
            # RUNNING, otherwise to BUSY
            # also, f it failed to disconnect we should update to RUNNING
            if instance.select_value != time_val:
                update_state_calls.append(
                    call(instance, DbodInstance.BUSY))
            else:
                update_state_calls.append(
                    call(instance, DbodInstance.RUNNING))
            continue

        if instance.exception and instance.exception != "disconnect":
            # if any method raised an exception we should
            # update state to STOPPED
            # disconnect is not critical so we dont update the state
            update_state_calls.append(
                call(instance, DbodInstance.STOPPED))

    assert plugin.helper.update_state.mock_calls == update_state_calls


@given(
    instances=st.lists(
        # Create a list of 100 instance mocks
        st.builds(
            get_mocked_instance,
            db_name=st.integers(max_value=10),
            slave=st.booleans(),
            active=st.booleans(),
            # No Malformed instances in this test
            malformed=st.booleans(),
            # simulate exception in one of the methods
            exception=st.sampled_from(
                ["connect", "insert", None, "select", "create", "execute",
                 "disconnect"]),
            # Select always returns 100 as we're testing exceptions
            select_value=st.integers(
                min_value=1,
                max_value=10
                ),
            exception_message=st.text(
                alphabet=string.ascii_lowercase, max_size=30),
            notification=st.booleans(),
            ),
        min_size=1,
        max_size=20
        ),
    # Simulate output of time.time() that we insert
    time_val=st.integers(min_value=1, max_value=10)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_read_collectd_error_messages(mocker, plugin, instances, time_val):
    """
    Test that before dispatching, we log a proper message so we can inspect
    later what happened in /var/log/collectd.log
    """
    #########################################
    # Mock
    mocker.resetall()
    import collectd
    mocker.patch.object(plugin, 'instances', instances, create=True)
    plugin.helper.update_state.reset_mock()
    collectd.reset_mock()
    # mock time call
    time = mocker.patch('dbod_ping.time')
    time.return_value = time_val
    ##################################################
    # The actual call that we're testing,
    # normally read is called by collectd!
    plugin.read()
    ##################################################
    # We collect all calls to dispatch here
    expected_calls_error = []
    expected_calls_info = []
    expected_calls_warning = []
    # We iterate over mocked instances and check
    # that proper calls to collectd.error were made
    ##################################################
    for instance in instances:
        if isinstance(instance, MalformedDbodInstance):
            continue
        if not instance.active:
            # If instance is not active, we should log that we dispatch -1
            expected_calls_info.append(
                call("| dbod_ping | INFO | %s | [%s] | %s"
                     % (instance.db_name, "-1", "Instance not active.")))
            continue
        if instance.slave:
            continue

        # Not slave instance
        # Any exception apart from disconnect method
        if instance.exception and \
                instance.exception != "disconnect":
            expected_calls_error.append(
                call("| dbod_ping | ERROR | %s | [%s] | %s"
                     % (instance.db_name, "1",
                        instance.exception_message)))
        elif time_val != instance.select_value:
            # Here we check that if inserted and selectd values
            # are different and we log it
            expected_calls_error.append(
                call("| dbod_ping | ERROR | %s | [%s] | %s"
                     % (instance.db_name, "1",
                        "Inserted value different than selected.")))
        if instance.exception == "disconnect":
            # Disconnect error should be logged
            expected_calls_warning.append(
                call("| dbod_ping | WARNING | %s | [] | %s"
                     % (instance.db_name,
                        "Not able to disconnect: %s"
                        % instance.exception_message)))

    assert collectd.error.mock_calls == expected_calls_error
    assert collectd.info.mock_calls == expected_calls_info
    assert collectd.warning.mock_calls == expected_calls_warning
