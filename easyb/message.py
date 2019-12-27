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

import crc8

from typing import List, Tuple
from easyb.data import MessageDirection, MessageLength, MessagePriority

__all__ = [
    "Message"
]


class Message(object):

    @property
    def priority(self) -> MessagePriority:
        return self._priority

    @property
    def address(self) -> int:
        return self._address

    @property
    def code(self) -> int:
        return self._code

    @property
    def length(self) -> MessageLength:
        return self._length

    @property
    def direction(self) -> MessageDirection:
        return self._direction

    @property
    def data(self) -> List[int]:
        return self._data

    @property
    def command(self) -> List[int]:
        return self._command

    def __init__(self, **kwargs):
        """Initialise the Message.

        :Arguments:
        * address: address of unit to read
        * code: F1 command code
        * priority: message priority
        * length: message length

        :param kwargs: keyworded variable length of arguments.
        :type kwargs: **dict
        """

        self._address = 0
        self._code = 0
        self._priority = MessagePriority.NoPriority
        self._length = MessageLength.Byte3
        self._direction = MessageDirection.FromMaster
        self._data = []
        self._command = []

        item = kwargs.get("address", 0)
        if item is not None:
            self._address = item

        item = kwargs.get("code", None)
        if item is not None:
            self._code = item

        item = kwargs.get("priority", None)
        if item is not None:
            self._priority = item

        item = kwargs.get("length", None)
        if item is not None:
            self._length = item

        item = kwargs.get("direction", None)
        if item is not None:
            self._direction = item
        return

    def encode(self) -> Tuple[int, int, int]:
        crc = crc8.crc8()

        byte1 = 255 - self.address
        crc.update(byte1)

        direction = self.direction.value
        length = self.length.value << 1
        priority = self.priority.value << 3
        code = self.code << 4

        byte2 = 0x00
        byte2 = byte2 | direction
        byte2 = byte2 | length
        byte2 = byte2 | priority
        byte2 = byte2 | code
        crc.update(byte2)

        result = (byte1, byte2, crc.digest())
        return result
