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

import json
from typing import Union

__all__ = [
    "check_dict",
    "openjson"
]


def check_dict(checkdict: dict, keylist: list) -> bool:
    """Checks a dict for a list of keys.

    :param checkdict: dictionary to check.
    :type checkdict: dict

    :param keylist: list with keys to check for.
    :type keylist: list

    :returns: True if all keys are present, otherwise False.
    :rtype: bool
    """
    ret = True
    list_keys = list(checkdict)

    for key in keylist:
        if list_keys.count(key) == 0:
            ret = False

    return ret


def openjson(filename: str) -> Union[dict, None]:
    """opens a json file and performs some checks.

    :param filename: json filename.
    :type filename: str

    :returns: json instance if successfull, otherwise None.
    :rtype: json, None
    """

    f = open(filename, mode='r', encoding="utf-8")
    data = json.load(f)
    f.close()
    return data
