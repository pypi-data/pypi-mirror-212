"""
DBOD replication
"""

from dbod_plugin import DbodCollectdPlugin
from dbod_instances import DbodInstance, MalformedDbodInstance
import collectd  # pylint: disable=import-error


class DbodReplicationPlugin(DbodCollectdPlugin):
    """
    DBOD replication plugin
    """

    log_dispatch = "| dbod_replication | {} | {:10} | [{}] | {}"

    def mysql_repl_threads_check(self, instance):
        collectd.debug(" (MySQL) dbod_replication - checking MySQL replica {} replication threads".format(instance.db_name))
        try:
            instance.connect()
            io_thread_status = instance.get_replica_io_thread_status()
            sql_thread_status = instance.get_replica_sql_thread_status()
            if io_thread_status != 'Yes' or sql_thread_status != 'Yes':
                collectd.error(
                    self.log_dispatch.format(
                        "ERROR", instance.db_name, "1",
                        "(MySQL) One of the replication threads is not running; io_thread_running: {}, sql_thread_running: {}".format(
                            io_thread_status, sql_thread_status)))
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
        except Exception as exc:
            # Catch all exception and dispatch error
            collectd.error(
                self.log_dispatch.format(
                    "ERROR", instance.db_name, "1",
                    "Exception: {}".format(exc)))
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

    def pg_repl_check(self,instance):
        try:
            instance.connect()
            repl_status = instance.get_replication_status()
            if repl_status != 'streaming':
                collectd.error(
                    self.log_dispatch.format(
                        "ERROR", instance.db_name, "1",
                        "(PostgreSQL) Replication is broken, replication status is : {}".format(
                            repl_status)))
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
        except Exception as exc:
            # Catch all exception and dispatch error
            collectd.error(
                self.log_dispatch.format(
                    "ERROR", instance.db_name, "1",
                    "Exception: {}".format(exc)))
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
        Then iterate over the list of instances, and check the replication status if they are replicas
        """
        super(DbodReplicationPlugin, self).read()
        for instance in self.instances:
            # MalformedDbodInstance means broken data in DBOD API
            # this is handled by another collectd plugin
            # Catch all exception and dispatch error
            if isinstance(instance, MalformedDbodInstance):
                continue
            if instance.cluster_type == 'InnoDB':
                continue
            if instance.slave:

                collectd.debug("dbod_replication - instance {} is a replica".format(instance.db_name))
                if instance.db_type == 'MYSQL':
                    self.mysql_repl_threads_check(instance)
                elif instance.db_type == 'PG':
                    self.pg_repl_check(instance)




DbodReplicationPlugin()
