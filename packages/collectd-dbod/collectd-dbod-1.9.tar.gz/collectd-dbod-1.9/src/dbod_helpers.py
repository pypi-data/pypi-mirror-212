"""Update instance status, get list of instances on a host

Raises:
    DbodConfigException: Missing configuration in  /etc/dbod/conf/core.conf
"""
import json
from socket import gethostname

import requests
from dbod_instances import EntityMalformedException, MalformedDbodInstance, \
    instance_types
import collectd  # pylint: disable=import-error

import platform
PYTHON_VERSION = platform.python_version()
from pkg_resources import parse_version as version

if version(PYTHON_VERSION) >= version("3.0"):
    from cerndb.config import Config
else:
    try:
        from ConfigParser import ConfigParser
    except ImportError:
        from configparser import ConfigParser
    import apacheconfig



class DbodConfigException(Exception):
    """Raised when the config is missing or malformed."""


class DbodCollectdHelper:
    """Class mostly used in performing operations with DBOD API."""

    # pylint: disable=unsubscriptable-object, too-many-instance-attributes
    # pylint: disable=import-outside-toplevel
    def __init__(self):
        if version(PYTHON_VERSION) >= version("3.0"):
            """Use cerndb-config"""

            try:
                self.config = Config( module_name="collectd-dbod")
            except Exception as e:
                raise DbodConfigException(e)
            ##################################################
            # Get interesting info from the config file /etc/collectd-dbod/config.yaml
            ##################################################
            try:
                self.cachefile = self.config['api']['cachefile']
                self.api_url = self.config['api']['host']
                self.instance_endpoint = \
                    self.config['api']['entity_endpoint']
                self.api_user = self.config['api']['user']
                self.api_password = self.config['api']['password']
                self.user = self.config['dbmon']['user']
                self.password = self.config['dbmon']['password']
                self.influx2_client = self.config['influx2']['client']
                self.cluster_member_endpoint = self.config['api']['cluster_member_endpoint']

            except KeyError as e:
                raise DbodConfigException(
                    "Error in DBOD config file (%s): missing key '%s'"
                    % ('config.yaml', e.args[0]))

            except TypeError as e:
                raise DbodConfigException(
                    "Error in DBOD config file (%s): missing nested key"
                    % ('config.yaml'))

        else:
            """Regethostnamead DBOD config file."""
            from apacheconfig import make_loader
            config_file = "/etc/dbod/conf/core.conf"
            ##################################################
            # Load DBOD config file to get api endpoints and
            # cachefile location
            ##################################################
            with make_loader() as loader:
                try:
                    self.config = loader.load(config_file)
                except apacheconfig.error.ConfigFileReadError as e:
                    raise DbodConfigException(e)
            ##################################################
            # Get interesting info from the config file
            ##################################################
            try:
                self.cachefile = self.config['api']['cachefile']
                self.api_url = self.config['api']['host']
                self.instance_endpoint = \
                    self.config['api']['entity_endpoint']
                self.api_user = self.config['api']['user']
                self.api_password = self.config['api']['password']
                self.user = self.config['dbmon']['user']
                self.password = self.config['dbmon']['password']
                self.influx2_client = self.config['influx2']['client']
                self.cluster_member_endpoint = \
                    self.config['api']['cluster_member_endpoint']

            except KeyError as e:
                raise DbodConfigException(
                    "Error in DBOD config file (%s): missing key '%s'"
                    % (config_file, e.args[0]))


    def get_instances(self):
        """
        Get running instances in the node using entities.json
        Returns:
            entities data as a dict (from /etc/dbod/conf/cache/entities.json)
        """
        ###################################
        # Get data from the cache: /etc/dbod/conf/cache/entities.json
        ###################################
        with open(self.cachefile) as f:
            data = json.load(f)

        ######################################
        # Create Instances from the response
        ######################################
        instances = []

        for instance_dict in data:
            # If creating DbodInstance raises exception, we either
            # pass it further or ignore it - depends on the metric!
            try:
                #####################################################
                # Create instances based on the db_type attribute
                #####################################################
                # Dynamically decide which instance
                # to create based on the db_type
                if instance_dict['state'] != 'MAINTENANCE':
                    try:
                        type = instance_dict['type']
                        instances.append(
                            instance_types[type](instance_dict,
                              user=self.user,
                              password=self.password,
                              influx2_client=self.influx2_client
                        ))

                    except KeyError:
                        # Missing db_type
                        instances.append(
                            MalformedDbodInstance(instance_dict,
                                                  user=self.user,
                                                  password=self.password))
            except EntityMalformedException:
                # Create MalformedDbodInstance
                instances.append(MalformedDbodInstance(
                    instance_dict, user=self.user, password=self.password))
        return instances

    def write_to_cache(self,db_name, key, value):
        with open(self.cachefile,'r') as f:
            data = json.load(f)
        for instance_dict in data:
            if instance_dict['name'] == db_name:
                instance_dict[key] = value
                break
        with open(self.cachefile,'w') as f:
            json.dump(data,f,indent=2,separators=(',', ': '))

    def update_state(self, instance, state):
        """
        instance - one of DbodInstance
        state - DbodInstance.STOPPED or DbodInstance.RUNNING for now

        update instance state in DBOD API
        """

        if instance.state == state:
            collectd.debug("Instance %s state [%s] has not changed from [%s]"
                           % (instance.db_name, instance.state, state))
        else:
            collectd.debug("Updating %s instance state to: %s"
                           % (instance.db_name, state))
            url = "%s/%s/%s" % (self.api_url,
                                self.instance_endpoint,
                                instance.id)
            # check the actual current value
            request = requests.get(url)
            # If status code != 200 there was an issue connecting to the DBOD api
            if request.status_code != 200:
                collectd.error("Failed getting current state of %s. Response code %s, url %s, self.api_url %s, self.instance_endpoint %s"
                               % (instance.db_name, request.status_code, url, self.api_url, self.instance_endpoint))
                # we then consider that the cache is good
                current_state = instance.state
            else:
               current_state = request.json()["response"][0]['state']
            # if the new instance state is one of these don't update
            if current_state in ["AWAITING_APPROVAL","MAINTENANCE", "TO_BE_DELETED"]:
                collectd.debug("Not updating state of %s. Instance state: %s"
                           % (instance.db_name, instance.state))
            elif current_state == state:
                collectd.debug("Instance %s state [%s] has not changed, but the cache needs to be updated"
                           % (instance.db_name, current_state))
                self.write_to_cache(instance.db_name, 'state', state)
            else:
                headers = {'auth': '{ "admin" : true , "groups" : [ ] , "owner" : "collectd" }' }
                response = requests.put(
                url, headers=headers,
                auth=(self.api_user, self.api_password),
                json={"state": state},
                verify=False)  # nosec
                if response.status_code != 204:
                    collectd.error("Failed updating state of %s. Response code %s, url %s, self.api_url %s, self.instance_endpoint %s, headers %s"
                               % (instance.db_name, response.status_code, url, self.api_url, self.instance_endpoint, headers))
                #also update the cache (DBOD-2744)
                self.write_to_cache(instance.db_name,'state', state)

    def update_instance_role(self, instance, role):
        """
        instance - one of DbodInstance
        role - PRIMARY or REPLICA for now
        update instance role in DBOD API
        """

        collectd.debug("Updating %s instance role to: %s"
                       % (instance, role))

        try:
            role_id = 1 if role == 'PRIMARY' else 2
            request_dict = {"instance_id": instance, "role_id": role_id}
            body = json.dumps(request_dict)
            headers = {'Content-Type': 'application/json',
                       'auth': '{ "admin" : true , "groups" : [ ] , "owner" : "collectd-agent" }'}
            url = '{base_path}/{cluster_member_endpoint}'.format(base_path=self.api_url,cluster_member_endpoint=self.cluster_member_endpoint)
            response = requests.put(url, data=body, headers=headers, auth=(self.api_user, self.api_password))

            if response.status_code == 200:
                collectd.debug(
                    "Instance  {node}  {role} attribute updated successfully".format(node=instance,
                                                                                          role=role))
            else:
                collectd.error("DBOD api returned code: {code}".format(code=response.status_code))
        except Exception as e:
            collectd.error("There was an error while updating {node} role. Error: {err}".format(node=instance, err=e))


    def update_instance_attribute(self, instance_name, attribute, value):
        """
        :param self:
        :param instance_name:
        :param attribute:
        :return:
        """
        collectd.debug("Updating {} '{}' attribute".format(instance_name, attribute))

        try:
            body = value
            headers = {'Content-Type': 'text/html; charset=utf-8',
                       'auth': '{ "admin" : true , "groups" : [ ] , "owner" : "collectd-agent" }'}
            url = '{base_path}/{entity_endpoint}/{node}/attribute/{attr}'.format(base_path=self.api_url, entity_endpoint=self.instance_endpoint,node=instance_name,
                                                                   attr=attribute)
            response = requests.put(url, data=body, headers=headers, auth=(self.api_user, self.api_password))

            if response.status_code == 200:
                collectd.debug(
                    "Instance  {node}  {attribute} attribute updated successfully".format(node=instance_name,
                                                                                          attribute=attribute))
            else:
                collectd.error("DBOD api returned code: {code}".format(code=response.status_code))
        except Exception as e:
            collectd.error("There was an error while updating {node} attribute. Error: {err}".format(node=instance_name, err=e))
