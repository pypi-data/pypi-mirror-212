"""
DBOD plugin
"""

from abc import ABCMeta, abstractmethod
from dbod_helpers import DbodCollectdHelper
import collectd  # pylint: disable=import-error


# compatible with Python 2 *and* 3:
ABC = ABCMeta('ABC', (object,), {'__slots__': ()})


class DbodCollectdPlugin(ABC):
    """
    DBOD collectd plugin
    """
    def __init__(self):
        """
        Register collectd read and configure
        """
        self.instances = []
        collectd.debug("Registering init and read")
        collectd.register_init(self.collectd_init)
        collectd.register_read(self.read)
        # Set type and name to be dispatched
        self.collectd_type = "gauge"
        # self.collectd_plugin = \
        #    "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        self.collectd_plugin = self.__class__.__module__
        collectd.debug("Creating DbodCollectdHelper")
        self.helper = DbodCollectdHelper()

    def collectd_init(self):
        """
        In this method we'll get all the running DBOD instances
        from the current host using DbodCollectdHelper,
        it's registered as init method with collectd using register_init
        """
        self.instances = self.helper.get_instances()

    @abstractmethod
    def read(self):
        """
        A method to actually read something useful
        and dispatch values, must be implemented in the actual plugins
        In the parent method we refresh the instances
        """
        self.instances = self.helper.get_instances()

    def dispatch(self, values, notification=True, log_dispatch="",
                 plugin_instance=None):
        """
        Dispatch values to collectd
        """
        metric = collectd.Values()
        metric.type = self.collectd_type
        metric.plugin = self.collectd_plugin

        if not notification:
            values = [-1]
            collectd.info(log_dispatch)

        collectd.debug("Dispatch plugin: %s, value: %s" %
                       (metric.plugin, values))

        if plugin_instance:
            metric.plugin_instance = plugin_instance

        metric.dispatch(values=values)
