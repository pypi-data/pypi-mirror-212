"""
DBOD instances
"""

from distutils.util import strtobool
from abc import ABCMeta, abstractmethod
import requests
import psycopg2
import pymysql
import subprocess
from distutils.version import StrictVersion

try:
    from itertools import izip as zip  # pylint: disable=redefined-builtin
except ImportError:  # Python 3.x
    pass


# compatible with Python 2 *and* 3:
ABC = ABCMeta('ABC', (object,), {'__slots__': ()})


# Python 2 - 3 compatibility
try:
    basestring
except NameError:
    basestring = (str, bytes)  # pylint: disable=invalid-name


class EntityMalformedException(Exception):
    """
    Raised when there is missing information in the metadata
    returned by the DBOD API
    """


class DbodInstance(ABC):
    # pylint: disable=too-many-instance-attributes
    # All of the attributes are considered necessary

    """
    Represents DBOD instance and is created from dictionary
        returned by a DBOD API call
    """
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    BUSY = "BUSY"

    def __init__(self, api_dict, user=None, password=None, influx2_client=None):
        """
        Takes dictionary as it was returned by the DBOD API
            and fills instance attributes
        user - since user/password doesn't come from the API information
            we nedd separate args to set them

        Raises:
            EntityMalformedException - when one of the necessary attributes is
                not present in the dictionary.
        """
        self.connection = None
        if user:
            self.user = user
        if password:
            self.password = password
        if influx2_client:
            self.influx2_client = influx2_client

        try:
            self.instance = "dbod-%s.cern.ch" \
                % (api_dict["db_name"].replace("_", "-"))
            #check if we use the old api:
            if "db_type" in api_dict:
                self.db_type = api_dict["db_type"]
                self.active = api_dict["active"]
            else:
                self.id = api_dict["id"]
                self.db_type = api_dict["type"]
                self.active = (api_dict["status"] == "ACTIVE")
            self.port = api_dict["port"]
            self.socket = api_dict["socket"]
            self.category = api_dict["class"]
            self.notification = api_dict["attributes"]["notifications"]
            self.state = api_dict["state"]
            self.db_name = api_dict["db_name"]
            self.db_version = api_dict["version"]
            self.bindir = api_dict["bindir"]
            self.cluster_type = api_dict['cluster_type']
            self.role = api_dict['role']
        except KeyError as e:
            raise EntityMalformedException(
                "Attribute %s missing from the metadata! (DBOD API)"
                % e.args[0])

        #####################################
        # Change attribute types
        #####################################
        try:
            self.port = int(self.port)
        except ValueError as e:
            raise EntityMalformedException(
                "Attribute port has incorrect value! (DBOD API metadata): %s"
                % (e))
        if isinstance(self.notification, basestring):
            try:
                self.notification = bool(strtobool(self.notification))
            except ValueError as e:
                raise EntityMalformedException(
                    "Attribute notifications has incorrect value! "
                    "(DBOD API metadata): %s" % (e))

        ########################################
        # If slave was not defined, use False
        ########################################
        try:
            self.slave = api_dict["attributes"]["slave"]
            if isinstance(self.slave, basestring):
                try:
                    self.slave = bool(strtobool(self.slave))
                except ValueError as e:
                    raise EntityMalformedException(
                        "Attribute slave has incorrect value! "
                        "(DBOD API metadata): %s" % (e))
        except KeyError:
            self.slave = False

        #############################################################
        # If slave monit_notif_max_lag_seconds is not defined, use 0
        #############################################################
        try:
            self.max_lag_seconds = \
                int(api_dict["attributes"]["monit_notif_max_lag_seconds"])
        except KeyError:
            self.max_lag_seconds = 300

    @abstractmethod
    def connect(self):
        """Connect to an instance."""

    def disconnect(self):
        """
        Default implementation that works for both
            Postgres and MySQL library
        """
        self.connection.close()

    def execute(self, statement):
        """
        Default implementation that works for both
            Postgres and MySQL library
        """
        cursor = self.connection.cursor()
        cursor.execute(statement)
        self.connection.commit()
        cursor.close()

    def select(self, statement):
        """
        Default implementation that works for both
            Postgres and MySQL library
        For now it can select only one value!
        """
        cursor = self.connection.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()
        cursor.close()
        return results[0][0]

    def insert(self, query):
        """
        By default it just executes, maybe for InfluxDB
        we need to override it, to be seen...
        """
        self.execute(query)

    def create(self, query):
        """
        Same as 'insert'. To be verified if needed at all
        """
        self.execute(query)

    def get_replication_lag(self):
        """
        Unfortunately we need a separate function for that.
        This is because while in Postgres, we can get this info with
        a select statement, in mysql we have to run 'SHOW SLAVE STATUS'.
        Show slave status, doesn't allow for easy filtering for the info that
        we're interested with, so we have to do it in Python.

        Implementation in the base class is the one that will be used in
        Postgres. Also, future release (8.0) of mysql has a table
        that can be selected for this info, then we can remove this method
        and use plain select
        """
        return self.select(self.slave_lag_query)  # pylint: disable=no-member


class MySQLDbodInstance(DbodInstance):
    """Represents a MySQL instance."""
    ping_insert_query = "INSERT INTO collectd_ping VALUES ({0});"
    ping_select_query = "SELECT * FROM collectd_ping;"
    ping_create_query = None
    ping_delete_query = "DELETE FROM collectd_ping;"
    slave_lag_query = "SHOW SLAVE STATUS"
    read_only_query = "SHOW VARIABLES LIKE 'read_only'"
    replica_status_query = "SHOW REPLICA STATUS"
    ping_read_only_query = "SELECT  1 FROM DUAL"
    def connect(self):
        self.connection = pymysql.connect(
            unix_socket=self.socket,
            user=self.user,
            passwd=self.password,
            db="dod_dbmon",
            port=self.port,
            connect_timeout=10)

    def create(self, query):
        pass

    def get_replication_lag(self):
        """
        SHOW SLAVE STATUS, then we have to process what we get
        from this statement to get the interesting bit - Seconds_Behind_Master
        """
        cursor = self.connection.cursor()
        cursor.execute(self.slave_lag_query)
        results = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        column_names = [desc[0] for desc in cursor.description]
        results = dict(zip(column_names, results))
        return results['Seconds_Behind_Master']

    def get_read_only_variable_value(self):
        """
        executes show variables like 'read_only'
        """
        cursor = self.connection.cursor()
        cursor.execute(self.read_only_query)
        results = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        dct = dict(results)
        return dct['read_only']

    def get_replica_io_thread_status(self):
        """
        executes SHOW SLAVE STATUS or SHOW REPLICA STATUS depending on the MySQL server version
        and checks the status of the Replica IO thread
        """
        result_field = ''
        cursor = self.connection.cursor()
        if StrictVersion(self.db_version) > StrictVersion('8.0.0'):
            cursor.execute(self.replica_status_query)
            result_field = 'Replica_IO_Running'
        elif StrictVersion(self.db_version) < StrictVersion('8.0.0'):
            cursor.execute(self.slave_lag_query)
            result_field = 'Slave_IO_Running'
        results = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        column_names = [desc[0] for desc in cursor.description]
        results = dict(zip(column_names, results))
        return results[result_field]

    def get_replica_sql_thread_status(self):
        """
        executes SHOW SLAVE STATUS or SHOW REPLICA STATUS depending on the MySQL server version
        and checks the status of the Replica SQL thread
        """
        result_field = ''
        cursor = self.connection.cursor()
        if StrictVersion(self.db_version) > StrictVersion('8.0.0'):
            cursor.execute(self.replica_status_query)
            result_field = 'Replica_SQL_Running'
        elif StrictVersion(self.db_version) < StrictVersion('8.0.0'):
            cursor.execute(self.slave_lag_query)
            result_field = 'Slave_SQL_Running'
        results = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        column_names = [desc[0] for desc in cursor.description]
        results = dict(zip(column_names, results))
        return results[result_field]

class PostgresDbodInstance(DbodInstance):
    """Represents a Postgresql instance. Is a subclass of DbodInstance"""
    ping_insert_query = "INSERT INTO collectd_ping VALUES ({0});"
    ping_select_query = "SELECT * FROM collectd_ping;"
    ping_create_query = None
    ping_delete_query = "DELETE FROM collectd_ping;"
    slave_lag_query = "SELECT CASE WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0::int ELSE " \
                      "EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())::int END AS time_lag;"
    replication_status_query = "SELECT status FROM get_replication_status();"

    def connect(self):
        """
        Connect to the database using psycopg2
        """
        self.connection = psycopg2.connect(
            database="dod_dbmon",
            user=self.user,
            password=self.password,
            host="/var/lib/pgsql/",
            port=self.port
        )

    def create(self, query):
        pass

    def get_replication_status(self):
        cursor = self.connection.cursor()
        cursor.execute(self.replication_status_query)
        results = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        if isinstance(results, tuple):
            return results[0]
        else:
            return results

class StatusCodeException(Exception):
    """
    Raised when using InfluxDbodInstance, and result
    code was different than 200
    """


class InfluxDbodInstance(DbodInstance):
    """Represents a InfluxDB instance. Is a subclass of DbodInstance"""
    ping_insert_query = "collectd_ping,measurement=ping value={0}"
    ping_select_query = "q=select * from collectd_ping order by "\
        "time desc limit 1"
    ping_create_query = None
    ping_delete_query = None
    seconds_since_epoch = 0

    def connect(self):
        """
        Since we access InfluxDB with HTTP API there is no point
        in doing anything in the connect method
        """

    def select(self, statement):
        """
        Select writen point if Influx 1.x or ping command if Influx 2.x
        """
        if StrictVersion(self.db_version) >= StrictVersion('2.0'):
            # We call Influx 2.0 ping method
            # example: /usr/local/influxdb/influxdb-client-latest/bin/influx ping --host "https://dbod-xxx.cern.ch:8082"
            executable = "%s" % self.influx2_client
            param_host = "https://%s:%s" % (self.instance, self.port)
            out = subprocess.Popen([executable, 'ping', '--host', param_host],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = out.communicate()
            if stderr:
                raise StatusCodeException(
                    "Error pinging instance %s. Response code was: %s" %
                    (self.instance, stderr))
            else:
                return self.seconds_since_epoch
        else:
            url = "https://%s:%s/query?db=dod_dbmon" % (self.instance, self.port)
            response = requests.get(
                url, auth=(self.user, self.password), params=statement,
                verify=False, timeout=10)  # nosec
            if response.status_code != 200:
                raise StatusCodeException(
                    "Error executing GET statement on %s instance. Response "
                    "code was: %s" % (self.instance, response.status_code))
            return response.json()["results"][0]["series"][0]["values"][0][2]

    def insert(self, query):
        """
        Write a point if instance is running Influx 1.x
        """
        if StrictVersion(self.db_version) < StrictVersion('2.0'):
            # Influx uses HTTP API to write, here we POST to the influx write URL
            url = "https://%s:%s/write?db=dod_dbmon" % (self.instance, self.port)
            response = requests.post(
                url, auth=(self.user, self.password), data=query,
                verify=False, timeout=10)  # nosec
            if response.status_code != 204:
                raise StatusCodeException(
                    "Error executing POST statement on %s instance. Response "
                    "code was: %s" % (self.instance, response.status_code))
        else:
            self.seconds_since_epoch = int(query.split("value=")[1])

    def execute(self, statement):
        pass

    def create(self, query):
        pass

    def disconnect(self):
        """
        Also, here we won't do anything
        """


class MalformedDbodInstance(DbodInstance):
    """Represents a malformed instance, i.e. an instance that has some missing
    information in it's description (in entities.json). For example, such
    missing information makes connecting impossible."""
    # pylint: disable=super-init-not-called
    def __init__(self, api_dict, user=None, password=None):
        """
        Don't call parent class constructor, keep the dict, to see
            what was missing
        """
        self.api_dict = api_dict
        try:
            self.state = api_dict["state"]
        except KeyError:
            self.state = "UNKNOWN"

    def connect(self):
        pass

    def execute(self, statement):
        pass

    def disconnect(self):
        pass


instance_types = {    # pylint: disable=invalid-name
    "PG": PostgresDbodInstance,
    "MYSQL": MySQLDbodInstance,
    "InfluxDB": InfluxDbodInstance
}
