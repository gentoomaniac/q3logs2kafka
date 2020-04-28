#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'q3logs2kafka'
DESCRIPTION = 'Parse Q3 logs and send them to kafka'
URL = ''
EMAIL = 'marco@siebecke.se'
AUTHOR = 'Marco Siebecke'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
LICENSE = 'MIT'
EXCLUDE_FROM_PACKAGES = []
PACKAGE_DATA = []
REQUIRED = ['click', 'kafka-python']

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data={'': PACKAGE_DATA},
    license=LICENSE,
    entry_points={
        'console_scripts': [
            'q3logs2kafka = q3logs2kafka.main:cli',
        ],
    },
)
