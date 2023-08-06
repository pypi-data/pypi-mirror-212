from pytest import raises
from mock import MagicMock
import dbod_helpers
import pytest
import collectd
from dbod_plugin import DbodCollectdPlugin # noqa


@pytest.fixture
def plugin(mocker):
    mocker.patch('dbod_helpers.DbodCollectdHelper.__init__')
    dbod_helpers.DbodCollectdHelper.__init__.return_value = None

    class Plugin(DbodCollectdPlugin):
        def read(self):
            super(Plugin, self).read()
            pass
    return Plugin


def test_class_is_abstract():
    """
    Test it's an abstract class with collectd_init and read methods
    """
    with raises(TypeError) as exc:
        DbodCollectdPlugin()
    assert "with abstract methods read" in str(exc.value)


def test_it_has_methods():
    """
    Test DbodCollectdPlugin has collectd_init() and read()
    methods
    """
    assert "collectd_init" in dir(DbodCollectdPlugin)
    assert "read" in dir(DbodCollectdPlugin)


def test_init_registers_methods_with_colelctd(plugin, mocker):
    """
    Constructor should register collectd_init() and read()
    """
    mocker.patch('dbod_helpers.DbodCollectdHelper.get_instances')
    dbod_helpers.DbodCollectdHelper.get_instances.return_value = []
    print(plugin)
    print(dbod_helpers.DbodCollectdHelper)
    print(dbod_helpers)
    print(DbodCollectdPlugin)
    p = plugin()
    collectd.register_read.assert_called_with(p.read)
    collectd.register_init.assert_called_with(p.collectd_init)

    dbod_helpers.DbodCollectdHelper.__init__.assert_called()
    assert p.collectd_type == "gauge"
    assert p.collectd_plugin == "test_dbod_collectd_plugin"
    assert isinstance(p.helper, dbod_helpers.DbodCollectdHelper)


def test_plugin_mock_read_calls_parent_read(mocker, plugin):
    """
    Test that read() will call get_instances
    """
    mocker.patch('dbod_plugin.DbodCollectdPlugin.read')
    p = plugin()
    p.read()
    DbodCollectdPlugin.read.assert_called()


def test_parent_read_refreshes_instances(mocker, plugin):
    """
    Constructor should register collectd_init() and read()
    """
    mocker.patch('dbod_helpers.DbodCollectdHelper.get_instances')
    dbod_helpers.DbodCollectdHelper.get_instances.return_value = []
    p = plugin()
    dbod_helpers.DbodCollectdHelper.get_instances.reset_mock()
    dbod_helpers.DbodCollectdHelper.get_instances.return_value \
        = ["test"]
    p.read()
    dbod_helpers.DbodCollectdHelper.get_instances.assert_called()
    assert p.instances == ["test"]


def test_collectd_init_calls_dbod_helper(mocker, plugin):
    """
    Test collectd_init method will get running instances
    """
    mocker.patch('dbod_helpers.DbodCollectdHelper.get_instances')
    dbod_helpers.DbodCollectdHelper.get_instances.return_value = []
    p = plugin()
    p.collectd_init()
    dbod_helpers.DbodCollectdHelper.__init__.assert_called()
    dbod_helpers.DbodCollectdHelper.get_instances.assert_called()
    assert p.instances == []
    assert isinstance(p.helper, dbod_helpers.DbodCollectdHelper)


def test_dispatch(mocker, plugin):
    """
    Test it has dispatch method, which accepts a list of values
        it should:
            - create collectd.Values
            - set values.type to gauge
            - set values.plugin to module.class
            - call values.dispatch
    """
    mock = MagicMock()
    mocker.patch("collectd.Values")
    collectd.Values.return_value = mock
    p = plugin()
    values = []
    p.dispatch(values)
    collectd.Values.assert_called()
    assert mock.type == "gauge"
    assert mock.plugin == "test_dbod_collectd_plugin"
    mock.dispatch.assert_called_with(values=values)


def test_dispatch_accepts_plugin_instance(mocker, plugin):
    """
    Test dispatch accepts plugin instance
    """
    mock_values = mocker.patch("collectd.Values")
    p = plugin()
    p.dispatch([1], plugin_instance="dbod1")
    assert mock_values.return_value.plugin_instance == "dbod1"
    mock_values.return_value.dispatch.assert_called_with(values=[1])
    p.dispatch([0], plugin_instance="dbod2")
    assert mock_values.return_value.plugin_instance == "dbod2"
    mock_values.return_value.dispatch.assert_called_with(values=[0])
    mock_values.return_value.plugin_instance = None
    p.dispatch([0])
    assert mock_values.return_value.plugin_instance is None
    mock_values.return_value.dispatch.assert_called_with(values=[0])
