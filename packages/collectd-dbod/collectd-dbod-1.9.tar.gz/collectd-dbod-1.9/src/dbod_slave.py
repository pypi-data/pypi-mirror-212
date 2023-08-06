"""
DBOD slave
"""

from dbod_plugin import DbodCollectdPlugin
from dbod_instances import DbodInstance, MalformedDbodInstance
import collectd  # pylint: disable=import-error


class DbodSlavePlugin(DbodCollectdPlugin):
    """
    DBOD slave plugin
    """

    log_dispatch = "| dbod_slave | {} | {:10} | [{}] | {}"

    def repl_lag_check(self,instance):

        collectd.debug("dbod_slave - checking replica {} replication lag".format(
                        instance.db_name))
        try:
            instance.connect()
            seconds = instance.get_replication_lag()
            # Compare the lag with the max_lag_seconds
            collectd.debug(
                "dbod_slave - comparing current lag ({}) with max_lag ({})".format(seconds, instance.max_lag_seconds))
            if type(seconds) is int:
                if seconds > instance.max_lag_seconds:
                    collectd.error(
                        self.log_dispatch.format(
                            "ERROR", instance.db_name, "1",
                            "Instance lags {} seconds behind master".format(seconds)))
                    self.dispatch([1], instance.notification,
                                  self.log_dispatch.format(
                                      "ERROR", instance.db_name,
                                      "-1", "Notifications disabled"),
                                  plugin_instance=instance.db_name)
                    self.helper.update_state(instance, DbodInstance.BUSY)
                else:
                    self.dispatch([0], instance.notification,
                                  self.log_dispatch.format(
                                      "INFO", instance.db_name,
                                      "-1", "Notifications disabled"),
                                  plugin_instance=instance.db_name)
                    self.helper.update_state(instance,
                                         DbodInstance.RUNNING)
            else:
                collectd.error(
                    self.log_dispatch.format(
                        "ERROR", instance.db_name, "1",
                        "Instance lag seconds behind primary is NULL"
                        ))
                self.dispatch([1], instance.notification,
                              self.log_dispatch.format(
                                  "ERROR", instance.db_name,
                                  "-1", "Notifications disabled"),
                              plugin_instance=instance.db_name)
                self.helper.update_state(instance, DbodInstance.BUSY)
        except Exception as exc:
            # Catch all exception and dispatch error
            collectd.error(
                self.log_dispatch.format(
                    "ERROR", instance.db_name, "1",
                    "Exception: {}" .format(exc)))
            self.dispatch([1], instance.notification,
                          self.log_dispatch.format(
                              "ERROR", instance.db_name,
                              "-1", "Notifications disabled"),
                          plugin_instance=instance.db_name)
            self.helper.update_state(instance, DbodInstance.STOPPED)
        finally:
            try:
                # Close connection to the database
                instance.disconnect()
            except Exception as exc:
                # We catch all exceptions - maybe the plugin
                # wasn't able to connect to the instance at all?
                collectd.warning(
                    self.log_dispatch.format(
                        "WARNING", instance.db_name, "",
                        "Not able to disconnect: {}".format(exc)))

    def read(self):
        """
        Call super - this will refresh list of instances from the Dbod API
        Then iterate over the list of instances, and check if they are slave
        """
        super(DbodSlavePlugin, self).read()
        for instance in self.instances:
            # MalformedDbodInstance means broken data in DBOD API
            # this is handled by another collectd plugin
            # Catch all exception and dispatch error
            if isinstance(instance, MalformedDbodInstance):
                continue
            if instance.cluster_type == 'InnoDB':
                continue
            if instance.slave:
                collectd.debug("-------")
                collectd.debug("dbod_slave - instance {} is a replica".format(instance.db_name))
                self.repl_lag_check(instance)



DbodSlavePlugin()
