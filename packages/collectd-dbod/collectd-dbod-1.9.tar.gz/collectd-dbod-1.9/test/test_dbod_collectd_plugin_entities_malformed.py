import pytest
from mock import MagicMock
import dbod_instances
import dbod_plugin # noqa


@pytest.fixture
def plugin(mocker):
    """
    Mock instances etc
    """
    values = MagicMock()
    mocker.patch('collectd.Values', values)
    mocker.patch("dbod_instances.MySQLDbodInstance.__init__")
    mocker.patch("dbod_instances.PostgresDbodInstance.__init__")
    mocker.patch("dbod_instances.InfluxDbodInstance.__init__")
    mocker.patch("dbod_instances.MalformedDbodInstance.__init__")
    dbod_instances.MySQLDbodInstance.__init__.return_value = None
    dbod_instances.PostgresDbodInstance.__init__.return_value = None
    dbod_instances.InfluxDbodInstance.__init__.return_value = None
    dbod_instances.MalformedDbodInstance.__init__.return_value = None
    mocker.patch("dbod_plugin.DbodCollectdPlugin.__init__")
    mocker.patch("dbod_plugin.DbodCollectdPlugin.read")
    dbod_plugin.DbodCollectdPlugin.__init__.return_value = None


def test_is_subclass_of_dbod_plugin(plugin):
    """
    Test that DbodCollectdPluginEntitiesMalformed is a subclass of
        DbodCollectdPlugin
    """
    from dbod_entities_malformed \
        import DbodCollectdPluginEntitiesMalformed # noqa
    i = DbodCollectdPluginEntitiesMalformed()
    assert isinstance(i, dbod_plugin.DbodCollectdPlugin)


def test_read_calls_parent_read(mocker, plugin):
    """
    Parent class read must be called to refresh instances data
    """
    from dbod_entities_malformed \
        import DbodCollectdPluginEntitiesMalformed # noqa
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    i = DbodCollectdPluginEntitiesMalformed()
    i.instances = []
    i.collectd_type = "gauge"
    i.collectd_plugin = "name"
    i.read()
    dbod_plugin.DbodCollectdPlugin.read.assert_called()


@pytest.mark.parametrize(
    "classes,number",
    [
        ([dbod_instances.MySQLDbodInstance], 0),
        ([dbod_instances.MySQLDbodInstance,
          dbod_instances.MalformedDbodInstance], 1),
        ([dbod_instances.MySQLDbodInstance,
          dbod_instances.MalformedDbodInstance,
          dbod_instances.PostgresDbodInstance,
          dbod_instances.MalformedDbodInstance], 2),
        ([dbod_instances.MySQLDbodInstance,
          dbod_instances.MalformedDbodInstance,
          dbod_instances.PostgresDbodInstance,
          dbod_instances.InfluxDbodInstance,
          dbod_instances.MalformedDbodInstance,
          dbod_instances.MalformedDbodInstance], 3),
    ])
def test_read_goes_through_list_of_entities(plugin, mocker, classes, number):
    """
    Read should go through the list of instances, get number of
        MalformedDbodInstance, and call collectd dispatch
    """
    from dbod_entities_malformed \
        import DbodCollectdPluginEntitiesMalformed # noqa
    instances = []
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    for cls in classes:
        instance = cls()
        instance.state = "UNKNOWN"
        instances.append(instance)
    p = DbodCollectdPluginEntitiesMalformed()
    mocker.patch.object(p, "dispatch")
    mocker.patch.object(p, 'instances', instances, create=True)
    p.read()
    p.dispatch.assert_called_with([number])


def test_read_omits_instances_awaiting_approval(plugin, mocker):
    """
    Malformed instances with state AWAITING_APPROVAL should be ommited
    in the count
    """
    from dbod_entities_malformed \
        import DbodCollectdPluginEntitiesMalformed # noqa
    p = DbodCollectdPluginEntitiesMalformed()
    mocker.patch.object(p, 'dispatch')
    instance1 = dbod_instances.MalformedDbodInstance()
    instance1.state = "AWAITING_APPROVAL"
    instance2 = dbod_instances.MalformedDbodInstance()
    instance2.state = "UNKNOWN"
    p.instances = [instance1, instance2]
    p.read()
    p.dispatch.assert_called_with([1])
