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

import os
from typing import List, Union

from easyb.utils import check_dict, openjson

__all__ = [
    "Error",
    "Status",
    "Unit",
    "Config"
]


class Error(object):

    code = 0
    text = ""

    def load(self, data: dict) -> bool:
        check = check_dict(data, ["code", "text"])
        if check is False:
            return False

        self.code = data["code"]
        self.text = data["text"]
        return True


class Status(object):

    bit = 0
    text = ""

    def load(self, data: dict) -> bool:
        check = check_dict(data, ["bit", "text"])
        if check is False:
            return False

        self.bit = int(data["code"], 0)
        self.text = data["text"]
        return True


class Unit(object):

    code = 0
    value = ""

    def load(self, data: dict) -> bool:
        check = check_dict(data, ["code", "value"])
        if check is False:
            return False

        self.code = data["code"]
        self.value = data["text"]
        return True


class Config(object):

    @property
    def error(self) -> List[Error]:
        return self._error

    @property
    def status(self) -> List[Status]:
        return self._status

    @property
    def units(self) -> List[Unit]:
        return self._units

    def __init__(self):
        self._error = []
        self._status = []
        self._units = []
        return

    def get_error(self, code: int) -> Union[None, Error]:
        for item in self.error:
            if item.code == code:
                return item
        return None

    def get_unit(self, code: int) -> Union[None, Unit]:
        for item in self.units:
            if item.code == code:
                return item
        return None

    def get_status(self, value: int) -> List[Status]:
        status = []

        for item in self.status:
            if item.bit & value:
                status.append(item)

        return status

    def load(self, filename: str) -> bool:
        config_path = os.path.abspath(os.path.normpath(filename))

        config = openjson(config_path)
        check = check_dict(config, ["error", "status", "units"])
        if check is False:
            return False

        for data in config["error"]:
            item = Error()

            check = item.load(data)
            if check is False:
                continue

            self.error.append(item)

        for data in config["status"]:
            item = Status()

            check = item.load(data)
            if check is False:
                continue

            self.status.append(item)

        for data in config["units"]:
            item = Unit()

            check = item.load(data)
            if check is False:
                continue

            self.units.append(item)

        if (len(self.units) > 0) and (len(self.status) > 0) and (len(self.error) > 0):
            return True

        return False
