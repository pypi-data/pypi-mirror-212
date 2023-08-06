#!/usr/bin/env python
"""
setup.py configuration
"""

from setuptools import setup, find_packages

setup(
    name='collectd-dbod',
    version='1.9',
    description='Collectd plugins for DBoD',
    author='Damian Moskalik',
    author_email='damian.moskalik@cern.ch',
    url='https://gitlab.cern.ch/db/collectd/collectd-dbod',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[
        'dbod_entities_malformed',
        'dbod_helpers',
        'dbod_ping',
        'dbod_plugin',
        'dbod_instances',
        'dbod_slave',
        'dbod_innodb_cluster_ping',
        'dbod_replication'
    ],
    install_requires=[
        "cerndb-base",
        "apacheconfig",
        "requests",
        "psycopg2-binary",
        "psycopg2",
        "six",
        "pymysql",
        "setuptools"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ]
)
