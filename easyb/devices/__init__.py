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
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

import easyb

from typing import List, Union, Any
from easyb.device import Device


__all__ = [
    "gmh3710",

    "get_device",
    "get_devices"
]

exception_list = [
    "get_devices",
    "get_device"
]


def get_attribute(path: str, classname: str) -> Union[Any, None]:
    """Load module attribute from given path.

    :param path: module path.
    :type path: str

    :param classname: class name.
    :type classname: str

    :return: attribute or None.
    """

    fromlist = [classname]

    try:
        m = __import__(path, globals(), locals(), fromlist)
    except ImportError:
        easyb.log.error("Unable to find module path: {0:s}".format(path))
        return None

    try:
        c = getattr(m, classname)
    except AttributeError:
        easyb.log.error("Unable to get module attribute: {0:s} with {1:s}".format(path, classname))
        return None

    return c


def get_device(device_name: str) -> Union[Device, None]:
    for item in __all__:
        if item in exception_list:
            continue

        path = "easyb.devices.{0:s}".format(item)
        name = get_attribute(path, "name")

        if name != device_name:
            continue

        device = get_attribute(path, "device")
        c = get_attribute(path, device)
        return c

    return None


def get_devices() -> list:
    device_list = []
    for item in __all__:
        if item in exception_list:
            continue

        path = "easyb.devices.{0:s}".format(item)
        name = get_attribute(path, "name")
        device_list.append(name)

    return device_list
