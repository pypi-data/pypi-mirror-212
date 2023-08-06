"""
DBOD InnoDB Cluster
"""

from time import time
from dbod_plugin import DbodCollectdPlugin
from dbod_instances import DbodInstance, MalformedDbodInstance
import collectd  # pylint: disable=import-error


class DbodCollectdInnoDBClusterPingPlugin(DbodCollectdPlugin):

    """
    Plugin for the Ping metric.
    """
    log_dispatch = "| dbod_innodb_cluster_ping | {} | {:10} | [{}] | {}"

    def primary_check(self, instance):
        if instance.role == 'REPLICA':
            self.helper.update_instance_role(instance.id, 'PRIMARY')
            self.helper.write_to_cache(instance.db_name, 'role', 'PRIMARY')
            self.helper.write_to_cache(instance.db_name, 'role_id', 1)
            self.helper.update_instance_attribute(instance.db_name, 'slave', 'false')
            collectd.warning(
                self.log_dispatch.format(
                    "WARNING", instance.db_name, "",
                    "Instance role ({}) does not match the current role, updating role in dbod01 to PRIMARY".format(instance.role) ))
        try:
            seconds_since_epoch = int(time())
            collectd.debug("%s, name: %s"
                           % (type(instance).__name__, instance.db_name))
            ##############################
            # Connect to the database
            ##############################
            instance.connect()
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
        except Exception as exc:  # noqa
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

    def replica_check(self, instance):
        if instance.role == 'PRIMARY':
            collectd.warning(
                self.log_dispatch.format(
                    "WARNING", instance.db_name, "",
                    "Instance role ({}) does not match the current role, updating role in dbod01 to REPLICA".format(instance.role)))
            self.helper.update_instance_role(instance.id, 'REPLICA')
            self.helper.write_to_cache(instance.db_name, 'role', 'REPLICA')
            self.helper.write_to_cache(instance.db_name, 'role_id', 2)
            self.helper.update_instance_attribute(instance.db_name, 'slave', 'true')
        try:
            collectd.debug("%s, name: %s"
                           % (type(instance).__name__, instance.db_name))
            ##############################
            # Connect to the database
            ##############################
            instance.connect()
            ####################################
            # Select the value we just inserted
            # to see if the select works
            ####################################
            collectd.debug("Select from d : %s"
                           % instance.db_name)
            value = instance.select(
                instance.ping_read_only_query)

            ####################################
            # Compare selected value and dispatch
            # 0 for success 1 for error
            ####################################
            collectd.debug("Comparing = selected: %s=%s"
                           % ('1', value))
            if value == 1:
                self.dispatch([0], instance.notification,
                              self.log_dispatch.format(
                                  "INFO", instance.db_name,
                                  "-1", "Notifications disabled"),
                              plugin_instance=instance.db_name)
                self.helper.update_state(instance,
                                         DbodInstance.RUNNING)
        except Exception as exc:
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
    def read(self):
        """
        Read iterates over the instances running on a given host
            then does, for each instance:
                - connect()
                - insert() - test insert query
                - select() - test select query
                - delete() - test delete query

        Then we dispatch 0 or 1 depending on the success or failure
        """
        super(DbodCollectdInnoDBClusterPingPlugin, self).read()
        # Will fill this pattern with string.format

        # Get the time in seconds since the epoch
        collectd.debug("read() in DbodCollectdInnoDBClusterPingPlugin")
        for instance in self.instances:
            if isinstance(instance, MalformedDbodInstance):
                continue
            collectd.debug("-------")
            if instance.cluster_type != 'InnoDB':
                continue
            else:
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
                else:
                    try:
                        instance.connect()
                        read_only = instance.get_read_only_variable_value()
                        if read_only == 'ON':
                            self.replica_check(instance)
                        elif read_only == 'OFF':
                            self.primary_check(instance)
                    except Exception as ex:
                        collectd.error(
                            self.log_dispatch.format(
                                "ERROR", instance.db_name, "1", ex))
                        self.helper.update_state(instance, DbodInstance.STOPPED)
                        self.dispatch([1], instance.notification,
                                      self.log_dispatch.format(
                                          "ERROR", instance.db_name,
                                          "-1", "Notifications disabled"),
                                      plugin_instance=instance.db_name)
                        if instance.role == 'PRIMARY':
                            self.helper.update_instance_role(instance.id, 'REPLICA')
                            self.helper.write_to_cache(instance.db_name, 'role', 'REPLICA')
                            self.helper.write_to_cache(instance.db_name, 'role_id', 2)
                            self.helper.update_instance_attribute(instance.db_name, 'slave', 'true')

DbodCollectdInnoDBClusterPingPlugin()
