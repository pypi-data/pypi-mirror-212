# Collectd DBOD metrics

This is a technical doc about collectd plugins to monitor dbod instances.

[[_TOC_]]

## Usage

`collectd-dbod` plugins dispatch only `int` values (limitation of `collectd`). Value **1** signals an error. To see the actual error, you need to login to the machine and check the content of `/var/log/collectd.log`.

Log format inside `/var/log/collectd.log` is the following:
`| PLUGIN_NAME | LEVEL | Instance | [VALUE DISPATCHED] | Message`

For example:
`| dbod_ping | ERROR | dbod_test | 1 | Can't connect...`

## How to run unit tests locally

> :information_source: *Unit tests will also run in `Gitlab CI` when you do `git push`.*

You run unit tests locally (on any machine with Docker installed). First clone the repository:

```bash
git clone https://:@gitlab.cern.ch:8443/db/collectd/collectd-dbod.git
cd collectd-dbod
```

Then, run the container:

```bash!
docker container run --name python27 --rm -tid \
-e "TERM=xterm-256color" \
-e "PY_FORCE_COLOR=1" \
-e 'PYTEST_ADDOPTS="--color=yes"' \
-v ${PWD}:/usr/src/collectd-dbod \
-w /usr/src/collectd-dbod \
gitlab-registry.cern.ch/db/cerndb-infra-syscontrol-tools:centos7.19.1 bash
```

Install dependencies:
```
docker container exec python27 pip install -r requirements.txt
```

You can run the tests:

```bash
docker container exec -ti python27 pytest -vvx
```
Since the project directory is shared with the container, you can modify the code and run tests instantly.

If you hit the following issue
```python!
ImportMismatchError: ('conftest', '/usr/src/development/conftest.py', local('/usr/src/collectd-dbod/conftest.py'))
```
remove all directories related to `pytest` caches (locally):
```
rm -rf __pycache__/ test/__pycache__
```

## How to run integration tests

This is probably the most useful test in debugging collectd problems.
This test will connect to instances, but will not send any data to collectd. Instead it will print all calls to collectd it would make.

Running the integration test requires installing a few packages, like gcc. With their dependencies it can result in tens of packages installed. Cleanup can be hard.

- **If you want to avoid installing anything on the machine** - try [using Miniconda](#preparing-test-environment-with-miniconda). Note that virtual environments didn't work because installing mysql library required gcc which is not present on dbod machines at the moment of writing.

- **If you don't care for installing stuff on the machine** - please, go [here](#integration-tests-without-miniconda).


### Preparing test environment with Miniconda

Follow these steps **only** if you want to avoid installing additional packages on the machine. Some of the ones we need to install are: `git`, `gcc`. With Miniconda we can install anything in a separate environment and cleanup afterwards is very easy.

If you don't care and can install directly on the machine [go here](#integration-tests-without-miniconda).


To install Miniconda:
1. Create a directory where we'll put everything
    ```
    mkdir /var/tmp/collectd-test
    cd /var/tmp/collectd-test
    ```
2. Download the installation script
    ```
    wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
    ```
3. Install Miniconda
    ```
    bash Miniconda2-latest-Linux-x86_64.sh -b -p /var/tmp/collectd-test/miniconda
    ```
4. Add conda to the PATH:
    ```
    export PATH="${PATH}:/var/tmp/collectd-test/miniconda/bin/"
    ```
5. Initialize Miniconda:
    ```
    conda init
    ```
    You may need to relog to the machine.

6. Create the environment:
    ```
    conda create --name collectd-test python=2.7 git gcc_linux-64 psycopg2 pymysql
    ```
7. Activate the environment:
    ```
    conda activate collectd-test
    ```
8.  Now, we have Miniconda ready. Clone the repository (only HTTPS link will work and you need to add your username to the URL).
    ```
    git clone https://YOUR_NICE_LOGIN@gitlab.cern.ch/db/collectd/collectd-dbod.git
    ```
9.  Install `collectd-dbod`
    On CentOS 7:
    ```
    cd collectd-dbod
    python setup27.py install
    ```
    If you are on a CentOS 8 machine use:
    ```
    cd collectd-dbod
    pip install .
    ```
10. Now you can [run the tests!](#running-the-tests)

#### Miniconda cleanup

After the tests, you can easily cleanup everything.

1. Remove Miniconda related lines from `~/.bashrc`. They can be easily located as they are enclosed between `# >>> conda initialize >>>` and `# <<< conda initialize <<<`
2. Remove the Miniconda directory `/var/tmp/collectd-test/miniconda`. You can also remove all files we created (just remove the whole `/var/tmp/collectd-test`) directory.


### Integration tests without Miniconda

> :information_source: This test will connect to instances, but will not send any data to collectd. Instead it will print all calls to collectd it would make.
> Note that a connection to each database will be made. For example, for the ping plugin the script will connect to each database, `INSERT` a value to the `collect_ping` table. Then it selects this value and compares with what we inserted.


1. First, connect to a machine where dbod instances are running.

2. Clone the repository and change to a branch you'd like to test. If git is not installed, you can either install it or copy the repository from another machine.
    ```
    [dbod-gc025]# git clone https://:@gitlab.cern.ch:8443/db/collectd/collectd-dbod.git
    [dbod-gc025]# cd collectd-dbod
    [dbod-gc025]# git checkout dbod_dev
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
    If pip is not installed, please install with:
    ```
    yum install python2-pip
    ```
4. In case of problems installing dependencies, you can try:
    ```
    pip install --upgrade pip
    pip install --upgrade setuptools
    ```

5. [Run the tests!](#running-the-tests)


### Running the tests

First install the dependencies - see [How to run integration tests](#how-to-run-integration-tests).
There are two files, for *dbod_ping* and *dbod_slave* plugins. Run either one of them:

```
[dbod-gc025]# ./integration_ping.py
```

or

```
[dbod-gc025]# ./integration_slave.py
```

Examine the output, calls to collectd will be printed. You should see something like:
```bash
call.info('Registering init and read')
call.register_init(<bound method DbodCollectdPluginPing.collectd_init of <dbod_collectd_ping.DbodCollectdPluginPing object at 0x7f77bf0f9c90>>)
call.register_read(<bound method DbodCollectdPluginPing.read of <dbod_collectd_ping.DbodCollectdPluginPing object at 0x7f77bf0f9c90>>)
call.info('Creating DbodCollectdHelper')
call.info('read() in DbodCollectdPluginPing')
call.info(u'MySQLDbodInstance, name: rundeck1')
call.info(u'Insert ping values to: rundeck1')
call.info(u'Select ping values from: rundeck1')
call.info('Comparing inserted=selected: 8496167=8496167')
call.Values()
call.Values().dispatch(values=[0])
call.info(u'PostgresDbodInstance, name: pf_quant')
call.info(u'Insert ping values to: pf_quant')
call.info(u'Select ping values from: pf_quant')
call.info('Comparing inserted=selected: 8496167=8496167')
call.Values()
call.Values().dispatch(values=[0])
```

`dispatch(values=[0])` means that the database works ok, `[1]` signals an error.


## Getting around the code (Updated for `collectd-dbod-1.0-5`)

There are a couple of Python modules:

- dbod_instances.py
- dbod_collectd_plugin.py
- dbod_collectd_ping.py
- dbod_collectd_entities_malformed.py
- dbod_collectd_helpers.py

The plugin logic is in `dbod_collectd_ping` and `dbod_collectd_entities_malformed`. Since the plugin functionality is spread across all modules, have a look at the following short description on how all works.

#### Short description of the flow

1. `collectd` in the configuration file defines this line: `Import dbod_collectd_ping`. This is done in Puppet - see [collectd config](#collectd-config).
2. This setting imports `dbod_collectd_ping.py`. On import (because it's outside of any functions) the constructor is called `DbodCollectdPluginPing()` - check the last line of `dbod_collectd_ping.py`.
3. `DbodCollectdPluginPing` has no `__init__`, so parent class constructor is called. Parent class is `DbodCollectdPlugin` from `dbod_collectd_plugin.py`. It does `collectd.register_init(self.collectd_init)` and `collectd.register_read(self.read)`. These register callbacks - basically every now and then collectd will call `read` function to get fresh values for the metric.
4. After registering, the constructor creates a `DbodCollectdHelper` object.
5. In the constructor of `DbodCollectdHelper` we read configuration files of DBOD API and config file of the previous lemon metric. In the configuration files we have needed passwords and DBOD API endpoints.
6. After the constructor finishes, collectd will call the function that we registered for `init` - `self.collectd_init`.
7. And, after `collectd_init()`, `read()` is called.
8. First line of the implementation of `read()` in the `DbodCollectdPluginPing`, calls parent class `read()` function. This one is defined in `DbodCollectdPlugin`. It uses the helper object to get all instances (from DBOD API or `entities.json`).
9. Then we use the list of instances to run queries. Each item in the list is an object of `DbodInstance` type witch specific implementations for each of the db type (MySQL, Postgres, ...)
10. To dispatch a value we call `self.dispatch([VALUE])`. Implemetation of `dispatch` is again in the `DbodCollectdPlugin` class.

---
#### DbodCollectdPlugin

An abstract class defined in `dbod_collectd_plugin` module.

Each of the collectd plugins is a subclass of `DbodCollectdPlugin`. `DbodCollectdPlugin` in its constructor `__init__` calls `collectd.register_read` and `collectd.register_init`. These are collectd methods that must be called to register plugin functionality in collectd. Then, it instatiates a `DbodCollectdHelper` object which will be described.

`read` method calls `get_instances` method of `DbodCollectdHelper`. This one makes a call to the API to get instances on the current host. If the API call fails, it takes this data from a locally stored copy `entities.json`.

---
#### DbodCollectdHelper

A class defined in `dbod_collectd_helpers` module.

In `__init__` we read two config files - `/etc/dbod/conf/core.conf`. 

`DbodCollectdHelper` has two methods - `get_instances()` and `update_status()`.

**`get_instances`** - queries DBOD API using REST, or if DBOD API is unavailable it uses the content of cached `entities.json`. This method is called on every call to `read` by collectd.

**`update_status`** - this one uses DBOD API to update instance status. If there was a problem with an instance, status can be changed changed to `BUSY` or `STOPPED` etc..

---

#### dbod_instances

In this module we have the main `DbodInstance` which is an abstract class. There are 4 subclasses for each type of databases - Influx, Postgres, MySQL, Malformed
> Malformed instance signals that there was some missing data coming from DBOD API and is used by EntityMalformed metric.

Each of them define a couple of methods `connect`, `select`, `insert`, `execute`. Postgres and MySQL work the same so the implementation of all methods except from `connect` is in the parent abstract class `DbodInstance`.
Influx uses HTTP API requests to query and update the data.

> :information_source: Most of the specific methods like `insert`, `select`, `create` are doing practically the same. The only exception is Influx, and that's why I decided to have these methods separately - so when you look at the plugin code you see right away, that there is an `insert` or a `select` etc.

---

## Creating a new dbod collectd plugin

Creating a new plugin should be easy and can be done with the following steps. In this example, we create a new plugin called `dbod_mytest`. You can also have a look at existing dbod plugins, as they follow what is described below.

1. Create a new module for the new plugin `dbod_mytest.py`.
2. Inside of the module, create a class which is a subclass of `DbodCollectdPlugin`:
    ```python
    class DbodCollectdMyTest(DbodCollectdPlugin):
        """
        implementation
        """

    DbodCollectdMyTest()
    ```
    Note that outside of the class you must create the class object.
3. Implement `read()`. Remember that the first instruction should be `super(DbodCollectdMyTest, self).read()`.
4. Inside `read()` implement the logic of the plugin. You have access to all instances with `self.instances`. Instances are refreshed for you with the call to `super` (point 3)!
5. Send a value to collectd with `self.dispatch()`.


## Collectd config

Considering the way the spec file for the RPM is currently constructed, collectd configuration should look like:

```
<Plugin python>
    ModulePath "/etc/collectd/python/"
    LogTraces true
    Interactive false
    Import "dbod_collectd_entities_malformed"
    Import "dbod_collectd_ping"
    Import "dbod_mytest"
</Plugin>
```

You can read more about Puppet configuration [here.](https://ia-guide.web.cern.ch/ia-guide/monitoring/alarms/sensors.html)
