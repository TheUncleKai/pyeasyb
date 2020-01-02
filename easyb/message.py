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
from easyb.definitions import Direction, get_direction, Length, get_length, Priority, get_priority
from easyb.bit import decode_u16, decode_u32, check_crc, create_crc, convert_u16, convert_u32

__all__ = [
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
    def data(self) -> Union[bytes, List[int]]:
        return self._data

    @property
    def error(self) -> int:
        return self._error

    @property
    def success(self) -> bool:
        return self._success

    @property
    def value(self) -> Any:
        return self._value

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
        self._data = []
        self._value = None
        self._error = 0
        self._success = False

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

        item = kwargs.get("data", None)
        if item is not None:
            self._data = item
        return

    @staticmethod
    def _encode_start(data):
        u8 = uint8(255 - data)
        result = int(u8)
        return result

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

    def _encode_byte6(self, result: list):
        byte = self._encode_start(self.data[0])
        result.append(byte)

        byte = self.data[1]
        result.append(byte)

        byte = create_crc(result[3], result[4])
        result.append(byte)
        return

    def _encode_byte9(self, result: list):
        byte = self._encode_start(self.data[2])
        result.append(byte)

        byte = self.data[3]
        result.append(byte)

        byte = create_crc(result[6], result[7])
        result.append(byte)
        return

    def command(self, command: Command) -> bool:
        self._address = command.address
        self._code = command.code
        self._priority = Priority.NoPriority
        self._length = command.length
        self._direction = Direction.FromMaster
        self._data = command.param
        return True

    def encode(self) -> Union[bytes, None]:

        if (self.length == Length.Byte6) and (len(self.data) != 2):
            easyb.log.error("Invald data size for Byte6: " + str(len(self.data)))
            self._success = False
            return None

        if (self.length == Length.Byte9) and (len(self.data) != 4):
            easyb.log.error("Invald data size for Byte4: " + str(len(self.data)))
            self._success = False
            return None

        result = []

        byte = self._encode_start(self.address)
        result.append(byte)

        byte = self._encode_header()
        result.append(byte)

        byte = create_crc(result[0], result[1])
        result.append(byte)

        if self.length == Length.Byte6:
            self._encode_byte6(result)

        if self.length == Length.Byte9:
            self._encode_byte6(result)
            self._encode_byte9(result)

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

    def decode_16(self) -> bool:
        length = len(self.data)
        self._success = False

        if (self.length is Length.Byte6) and (length != 3):
            easyb.log.error("Invalid data length for Byte6: " + str(length))
            return False

        check = check_crc(self.data[0], self.data[1], self.data[2])
        if check is False:
            return False

        self._value = int(convert_u16(self.data[0], self.data[1]))
        return True

    def decode_32(self) -> bool:
        length = len(self.data)
        self._success = False

        if (self.length is Length.Byte9) and (length != 6):
            easyb.log.error("Invalid data length for Byte9: " + str(length))
            return False

        check1 = check_crc(self.data[0], self.data[1], self.data[2])
        check2 = check_crc(self.data[3], self.data[4], self.data[5])
        if (check1 is False) or (check2 is False):
            return False

        value1 = int(convert_u16(self.data[0], self.data[1]))
        value2 = int(convert_u16(self.data[3], self.data[4]))

        self._value = int(convert_u32(value1, value2))
        return True

    def value_16(self) -> bool:
        length = len(self.data)
        self._success = False

        if (self.length is Length.Byte6) and (length != 3):
            easyb.log.error("Invalid data length for Byte6: " + str(length))
            return False

        check = check_crc(self.data[0], self.data[1], self.data[2])
        if check is False:
            return False

        error, value = decode_u16(self.data[0], self.data[1])
        if error != 0:
            self._error = error
            return False

        self._value = value
        self._success = True
        return True

    def value_32(self) -> bool:
        length = len(self.data)
        self._success = False

        if (self.length is Length.Byte9) and (length != 6):
            easyb.log.error("Invalid data length for Byte9: " + str(length))
            return False

        check1 = check_crc(self.data[0], self.data[1], self.data[2])
        check2 = check_crc(self.data[3], self.data[4], self.data[5])
        if (check1 is False) or (check2 is False):
            return False

        error, value = decode_u32(self.data[0], self.data[1], self.data[3], self.data[4])
        if error != 0:
            self._error = error
            return False

        self._value = value
        self._success = True
        return True

    def info(self):
        easyb.log.inform("ADDRESS", str(self.address))
        easyb.log.inform("CODE", str(self.code))
        easyb.log.inform("PRIORITY", str(self.priority.name))
        easyb.log.inform("LENGTH", str(self.length.name))
        easyb.log.inform("DIRECTION", str(self.direction.name))
        return
