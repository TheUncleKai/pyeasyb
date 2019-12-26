#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2019, Kai Raphahn <kai.raphahn@laburec.de>
#

from setuptools import setup, find_packages
import easyb

packages = find_packages(where=".")

setup(
    name=easyb.__name__,
    license=easyb.__license__,
    version=easyb.__version__,
    description=easyb.__description__,
    author=easyb.__author__,
    author_email=easyb.__email__,
    include_package_data=True,
    scripts=[
        'easyb-tool.py',
    ],
    url='https://github.com/TheUncleKai/pyeasyb',
    packages=packages,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Development Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'colorama'
    ]
)

