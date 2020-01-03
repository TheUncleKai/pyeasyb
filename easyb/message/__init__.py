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

from numpy import uint8, bitwise_or

from typing import List, Union

from easyb.command import Command
from easyb.message.stream import Stream

from easyb.definitions import Direction, get_direction, Length, get_length, Priority, get_priority
from easyb.bit import debug_data, crop_u8

__all__ = [
    "stream",

    "Message"
]


class Message(object):

    @property
    def address(self) -> int:
        return self._address

    @property
    def code(self) -> int:
        return self._code

    @property
    def priority(self) -> Priority:
        return self._priority

    @property
    def length(self) -> Length:
        return self._length

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def param(self) -> List[int]:
        return self._param

    @property
    def error(self) -> int:
        return self._error

    @property
    def stream(self) -> Stream:
        return self._stream

    def __init__(self, **kwargs):
        self._address = 0
        self._code = 0
        self._priority = Priority.NoPriority
        self._length = Length.Byte3
        self._direction = Direction.FromMaster
        self._value = None
        self._error = 0
        self._param = []
        self._stream = None

        item = kwargs.get("address", None)
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

        item = kwargs.get("param", None)
        if item is not None:
            self._param = item
        return

    def command(self, command: Command) -> bool:
        self._address = command.address
        self._code = command.code
        self._priority = Priority.NoPriority
        self._length = command.length
        self._direction = Direction.FromMaster
        self._param = command.param
        return True

    def _verify_param(self) -> bool:
        length = len(self._param)

        if (self.length is Length.Byte3) and (length == 0):
            return True

        check = length % 2
        if check != 0:
            easyb.log.error("Data size is not a pair! ({0:d})".format(length))
            return False

        if (self.length is Length.Byte6) and (length != 2):
            easyb.log.error("Invald data size for Byte6: {0:d}".format(length))
            return False

        if (self.length is Length.Byte9) and (length != 4):
            easyb.log.error("Invald data size for Byte4: {0:d}".format(length))
            return False

        return True

    def _encode_header(self):
        u8 = uint8(0)

        direction = uint8(self.direction.value)
        length = uint8(self.length.value << 1)
        priority = uint8(self.priority.value << 3)
        code = uint8(self.code << 4)

        u8 = bitwise_or(u8, direction)
        u8 = bitwise_or(u8, length)
        u8 = bitwise_or(u8, priority)
        u8 = bitwise_or(u8, code)

        result = int(u8)
        return result

    def _decode_header(self):
        byte0 = self.stream.data[0]
        byte1 = self.stream.data[1]

        self._address = 255 - byte0
        self._code = (byte1 & 0xf0) >> 4

        priority = (byte1 & 0x8) >> 3
        length = (byte1 & 0x6) >> 1
        direction = byte1 & 0x1

        self._priority = get_priority(priority)
        self._length = get_length(length)
        self._direction = get_direction(direction)
        return

    def encode(self) -> bool:
        check = self._verify_param()
        if check is False:
            return False

        data = []

        byte = crop_u8(self.address)
        data.append(byte)

        byte = self._encode_header()
        data.append(byte)

        data.append(0)

        if self.length == Length.Byte6:
            data.append(self.param[0])
            data.append(self.param[1])
            data.append(0)

        if self.length == Length.Byte9:
            data.append(self.param[0])
            data.append(self.param[1])
            data.append(0)

            data.append(self.param[2])
            data.append(self.param[3])
            data.append(0)

        self._stream = Stream(self.length)
        self._stream.set_data(data)

        check = self._stream.encode()
        if check is False:
            return False

        return True

    def decode(self, data: bytes) -> bool:
        self._error = 0

        self._stream = Stream(Length.Byte3)
        check = self._stream.decode(data)
        if check is False:
            easyb.log.error("Header is not valid!")
            return False

        self._decode_header()
        return True

    def info(self, debug: str):
        logging = "Address {0:d}, Code {1:d}, {2:s}, {3:s}, {4:s}".format(self.address, self.code, self.priority.name,
                                                                          self.length.name, self.direction.name)
        easyb.log.debug2(debug, logging)

        logging = debug_data(self.stream.bytes)
        easyb.log.debug2(debug, logging)
        return
