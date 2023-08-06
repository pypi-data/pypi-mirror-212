"""
DBOD ping
"""

from time import time
from dbod_plugin import DbodCollectdPlugin
from dbod_instances import DbodInstance, MalformedDbodInstance
import collectd  # pylint: disable=import-error


class DbodCollectdPluginPing(DbodCollectdPlugin):
    """
    Plugin for the Ping metric. What it does:

    """
    log_dispatch = "| dbod_ping | {} | {:10} | [{}] | {}"

    def read(self):
        """
        Read iterates over the instances running on a given host
            then does, for each instance:
                - connect()
                - create_table()
                - insert() - test insert query
                - select() - test select query

        Then we dispatch 0 or 1 depending on the success or failure
        """
        super(DbodCollectdPluginPing, self).read()
        # Will fill this pattern with string.format

        # Get the time in seconds since the epoch
        collectd.debug("read() in DbodCollectdPluginPing")
        seconds_since_epoch = int(time())

        for instance in self.instances:
            if isinstance(instance, MalformedDbodInstance):
                continue

            collectd.debug("-------")

            # Skip not active instances
            if not instance.active:
                self.dispatch([-1], instance.notification,
                              self.log_dispatch.format(
                                  "INFO", instance.db_name,
                                  "-1", "Instance not active."),
                              plugin_instance=instance.db_name)
                collectd.info(
                    self.log_dispatch.format(
                        "INFO", instance.db_name,
                        "-1", "Instance not active."))
                continue

            # Skip slave instances
            if instance.slave:
                continue
            elif instance.cluster_type == 'InnoDB':
                continue
            try:
                collectd.debug("%s, name: %s"
                               % (type(instance).__name__, instance.db_name))
                # Iterate over all instances
                ##############################
                # Connect to the database
                ##############################
                instance.connect()

                ##############################
                # Create test table
                ##############################
                instance.create(instance.ping_create_query)
                ##############################
                # Empty test table
                ##############################
                instance.execute(instance.ping_delete_query)
                ##############################
                # Insert test value
                ##############################
                collectd.debug("Insert ping values to: %s"
                               % instance.db_name)
                instance.insert(
                    instance.ping_insert_query.format(seconds_since_epoch)
                )

                ####################################
                # Select the value we just inserted
                # to see if the select works
                ####################################
                collectd.debug("Select ping values from: %s"
                               % instance.db_name)
                value = instance.select(
                    instance.ping_select_query)

                ####################################
                # Compare selected value and dispatch
                # 0 for success 1 for error
                ####################################
                collectd.debug("Comparing inserted=selected: %s=%s"
                               % (seconds_since_epoch, value))
                if value == seconds_since_epoch:
                    self.dispatch([0], instance.notification,
                                  self.log_dispatch.format(
                                      "INFO", instance.db_name,
                                      "-1", "Notifications disabled"),
                                  plugin_instance=instance.db_name)
                    self.helper.update_state(instance,
                                             DbodInstance.RUNNING)
                else:
                    # Connection was ok but insert or select failed
                    collectd.error(
                        self.log_dispatch.format(
                            "ERROR", instance.db_name, "1",
                            "Inserted value different than selected."))
                    self.dispatch([1], instance.notification,
                                  self.log_dispatch.format(
                                      "ERROR", instance.db_name,
                                      "-1", "Notifications disabled"),
                                  plugin_instance=instance.db_name)
                    self.helper.update_state(instance, DbodInstance.BUSY)
            except Exception as exc: # noqa
                """
                We catch all exceptions. No matter what kind of exception
                it was, we dispatch [1] and update instance status
                """  # pylint: disable=pointless-string-statement
                # https://twitter.com/gvanrossum/status/112670605505077248
                collectd.error(
                    self.log_dispatch.format(
                        "ERROR", instance.db_name, "1", exc))
                self.dispatch([1], instance.notification,
                              self.log_dispatch.format(
                                  "ERROR", instance.db_name,
                                  "-1", "Notifications disabled"),
                              plugin_instance=instance.db_name)
                # we update the status there
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
                            "Not able to disconnect: %s" % exc))


DbodCollectdPluginPing()
