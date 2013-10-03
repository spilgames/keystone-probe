#!/usr/bin/python
# Copyright (c) 2012 Spil Games
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup

from keystone_probe import __version__ as version
name = "keystone_probe"


setup(
    name = name,
    version = version,
    author = "Jasper Capel, Spil Games",
    description = ("Middleware for sending keystone stats to statsd"),
    license = "Apache License (2.0)",
    url = "https://github.com/spilgames/keystone-probe",
    packages=['keystone_probe'],
    classifiers=[
        "Development Status :: 2 - Beta",
        "Programming Language :: Python :: 2.6",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: No Input/Output (Daemon)",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[],
    entry_points={
        "paste.filter_factory": [
            "keystone_probe=keystone_probe.middleware:filter_factory",
        ],
    },
)
