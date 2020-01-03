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

from typing import List, Any, Union

from easyb.command import Command
from easyb.message.data import Data

from easyb.definitions import Direction, get_direction, Length, get_length, Priority, get_priority
from easyb.bit import decode_u16, decode_u32, check_crc, create_crc, convert_u16, convert_u32, debug_data, crop_u8

__all__ = [
    "data",

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
    def data(self) -> Data:
        return self._data

    @property
    def param(self) -> List[int]:
        return self._param

    @property
    def error(self) -> int:
        return self._error

    @property
    def success(self) -> bool:
        return self._success

    def __init__(self, **kwargs):
        """Initialise the Message.

        :Arguments:
        * address: address of unit to read
        * code: F1 command code
        * priority: message priority
        * length: message length
        * data: data for message > 3 bytes

        :param kwargs: keyworded variable length of arguments.
        :type kwargs: **dict
        """

        self._address = 0
        self._code = 0
        self._priority = Priority.NoPriority
        self._length = Length.Byte3
        self._direction = Direction.FromMaster
        self._value = None
        self._error = 0
        self._success = False
        self._param = []

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

        self._data = Data(self.length)
        return

    def command(self, command: Command) -> bool:
        self._address = command.address
        self._code = command.code
        self._priority = Priority.NoPriority
        self._length = command.length
        self._direction = Direction.FromMaster
        self._data = command.param
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

    def encode(self) -> Union[bytes, None]:

        check = self._verify_param()
        if check is False:
            return None

        result = []

        byte = crop_u8(self.address)
        result.append(byte)

        byte = self._encode_header()
        result.append(byte)

        result.append(0)

        if self.length == Length.Byte6:
            result.append(self.param[0])
            result.append(self.param[1])
            result.append(0)

        if self.length == Length.Byte9:
            result.append(self.param[0])
            result.append(self.param[1])
            result.append(0)

            result.append(self.param[2])
            result.append(self.param[3])
            result.append(0)

        self._success = True

        data = bytes(result)
        return data

    def _decode_header(self, byte0: int, byte1: int):
        self._address = 255 - byte0
        self._code = (byte1 & 0xf0) >> 4

        priority = (byte1 & 0x8) >> 3
        length = (byte1 & 0x6) >> 1
        direction = byte1 & 0x1

        self._priority = get_priority(priority)
        self._length = get_length(length)
        self._direction = get_direction(direction)
        return

    def decode(self, data: bytes):
        self._error = 0
        self._success = False
        header = []

        for item in data:
            header.append(int(item))

        if len(header) != 3:
            easyb.log.error("Header is not valid!")
            return

        check = check_crc(header[0], header[1], header[2])
        if check is False:
            easyb.log.error("Header is not valid!")
            return False

        self._decode_header(header[0], header[1])
        self._success = True
        return

    @data.setter
    def data(self, in_data: bytes):

        for item in in_data:
            self.data.append(int(item))
        return

    def info(self):
        easyb.log.debug2("ADDRESS", str(self.address))
        easyb.log.debug2("CODE", str(self.code))
        easyb.log.debug2("PRIORITY", str(self.priority.name))
        easyb.log.debug2("LENGTH", str(self.length.name))
        easyb.log.debug2("DIRECTION", str(self.direction.name))
        return

