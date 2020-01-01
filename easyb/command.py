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
from typing import List, Any

from easyb.definitions import Length


class Command(object):

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> int:
        return self._number

    @property
    def address(self) -> int:
        return self._address

    @property
    def code(self) -> int:
        return self._code

    @property
    def length(self) -> Length:
        return self._length

    @property
    def param(self) -> List[int]:
        return self._param

    def call(self) -> bool:
        check = self._func_call()
        return check

    def __init__(self, **kwargs):
        """Initialise the Message.

        :Arguments:
        * name: command name
        * number: command number
        * address: address of unit to read
        * code: F1 command code
        * length: message length
        * param: command param
        * func_call: function call for command

        :param kwargs: keyworded variable length of arguments.
        :type kwargs: **dict
        """

        self._name = ""
        self._number = 0
        self._address = 0
        self._code = 0
        self._length = Length.Byte3
        self._param = []
        self._func_call = None

        item = kwargs.get("name", "")
        if item is not None:
            self._name = item

        item = kwargs.get("number", 0)
        if item is not None:
            self._number = item

        item = kwargs.get("address", 1)
        if item is not None:
            self._address = item

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
