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
from typing import List

from easyb.definitions import Length


class Command(object):

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> int:
        return self._code

    @property
    def length(self) -> Length:
        return self._length

    @property
    def param(self) -> List[int]:
        return self._param

    def call(self, message) -> bool:
        check = self._func_call(message)
        return check

    def __init__(self, **kwargs):
        self.number = 0
        self.address = 1

        self._name = ""
        self._code = 0
        self._length = Length.Byte3
        self._param = []
        self._func_call = None

        item = kwargs.get("name", "")
        if item is not None:
            self._name = item

        item = kwargs.get("address", None)
        if item is not None:
            self.address = item

        item = kwargs.get("number", None)
        if item is not None:
            self.number = item

        item = kwargs.get("code", 0)
        if item is not None:
            self._code = item

        item = kwargs.get("length", Length.Byte3)
        if item is not None:
            self._length = item

        item = kwargs.get("param", [])
        if item is not None:
            self._param = item

        item = kwargs.get("func_call", None)
        if item is not None:
            self._func_call = item
        return
