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

from numpy import uint8, uint16, uint32, int32, uint64, bitwise_and, bitwise_or, bitwise_xor, left_shift, right_shift

from typing import List, Any, Tuple
from easyb.definitions import Direction, get_direction, Length, get_length, Priority, get_priority

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
    def data(self) -> List[int]:
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
    def _crc(byte1: int, byte2: int) -> int:
        ui16_integer = uint16((byte1 << 8) | byte2)

        counter = 0
        while counter < 16:
            if bitwise_and(ui16_integer, 0x8000) == 0x8000:
                ui16_integer = left_shift(ui16_integer, 1)
                ui16_integer = bitwise_xor(ui16_integer, 0x0700)
            else:
                ui16_integer = left_shift(ui16_integer, 1)

            counter += 1

        crc = uint8(255 - right_shift(ui16_integer, 8))
        result = int(crc)
        return result

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

        byte = self._crc(result[3], result[4])
        result.append(byte)
        return

    def _encode_byte9(self, result: list):
        byte = self._encode_start(self.data[2])
        result.append(byte)

        byte = self.data[3]
        result.append(byte)

        byte = self._crc(result[6], result[7])
        result.append(byte)
        return

    def encode(self) -> List[int]:

        if (self.length == Length.Byte6) and (len(self.data) != 2):
            easyb.log.error("Invald data size for Byte6: " + str(len(self.data)))
            self._success = False
            return []

        if (self.length == Length.Byte9) and (len(self.data) != 4):
            easyb.log.error("Invald data size for Byte4: " + str(len(self.data)))
            self._success = False
            return []

        result = []

        byte = self._encode_start(self.address)
        result.append(byte)

        byte = self._encode_header()
        result.append(byte)

        byte = self._crc(result[0], result[1])
        result.append(byte)

        if self.length == Length.Byte6:
            self._encode_byte6(result)

        if self.length == Length.Byte9:
            self._encode_byte6(result)
            self._encode_byte9(result)

        self._success = True
        return result

    @staticmethod
    def _convert_u16(bytea: int, byteb: int) -> int:
        data = (255 - bytea) << 8
        data = data | byteb
        return data

    @staticmethod
    def _convert_u32(inputa: int, inputb: int) -> int:
        data = (inputa << 16) | inputb
        return data

    def _decode_u16(self, byte3: uint8, byte4: uint8) -> Tuple[int, float]:
        u16_integer = self._convert_u16(byte3, byte4)
        float_pos = uint16(bitwise_and(u16_integer, 0xc000))
        float_pos = uint16(right_shift(float_pos, 14))

        u16_integer = uint16(bitwise_and(u16_integer, 0x3fff))

        if (u16_integer >= 0x3fe0) and (u16_integer <= 0x3fff):
            error = int(u16_integer) - 16352
            return error, 0.0

        nenner = 10 ** int(float_pos)
        zaehler = float(u16_integer) - 2048.0

        float_value = float(zaehler / nenner)
        return 0, float_value

    def _decode_u32(self, byte3: uint8, byte4: uint8, byte6: uint8, byte7: uint8) -> Tuple[int, float]:
        u16_integer1 = self._convert_u16(byte3, byte4)
        u16_integer2 = self._convert_u16(byte6, byte7)
        u32_integer = self._convert_u32(u16_integer1, u16_integer2)

        float_pos = uint16(0xff - byte3)
        float_pos = uint16(right_shift(float_pos, 3) - 15)

        u32_integer = uint32(bitwise_and(u32_integer, 0x07ffffff))

        if (100000000 + 0x2000000) > u32_integer:
            compare = uint32(bitwise_and(u32_integer, 0x04000000))

            if 0x04000000 == compare:
                u32_integer = uint32(bitwise_or(u32_integer, 0xf8000000))

            u32_integer = uint32(uint64(u32_integer) + 0x02000000)
        else:
            error = int(u32_integer - 0x02000000 - 16352)
            return error, 0.0

        i32_integer = int32(u32_integer)
        float_value = float(i32_integer) / float(float(10.0) ** float_pos)
        return 0, float_value

    def _check_crc(self, byte1: int, byte2: int, crc: int) -> bool:

        check_crc = self._crc(byte1, byte2)

        if check_crc == crc:
            return True

        easyb.log.error(
            "CRC check failed: {0:s} {1:s}, crc {2:s}, calculated {3:s}".format(hex(byte1), hex(byte2), hex(crc),
                                                                                hex(check_crc)))
        return False

    def _decode_header(self, byte0: int, byte1: int) -> bool:
        self._address = 255 - byte0
        self._code = (byte1 & 0xf0) >> 4

        priority = (byte1 & 0x8) >> 3
        length = (byte1 & 0x6) >> 1
        direction = byte1 & 0x1

        self._priority = get_priority(priority)
        self._length = get_length(length)
        self._direction = get_direction(direction)

        if (self._priority is None) or (self._length is None) or (self._direction is None):
            return False
        return True

    def decode(self, header: list):
        self._error = 0
        self._success = False

        if len(header) != 3:
            easyb.log.error("Header is not valid!")
            return

        check = self._check_crc(header[0], header[1], header[2])
        if check is False:
            easyb.log.error("Header is not valid!")
            return False

        check = self._decode_header(header[0], header[1])
        if check is False:
            easyb.log.error("Unable to decode header!")
            return False

        self._success = True
        return

    @data.setter
    def data(self, data: list):
        length = len(data)
        self._success = False

        if (self.length is Length.Byte6) and (length != 3):
            easyb.log.error("Invalid data length for Byte6: " + str(length))
            return

        if (self.length is Length.Byte9) and (length != 6):
            easyb.log.error("Invalid data length for Byte9: " + str(length))
            return

        if self.length is Length.Byte6:
            check = self._check_crc(data[0], data[1], data[2])
            if check is False:
                return

            error, value = self._decode_u16(data[0], data[1])
            if error != 0:
                self._error = error
                return

            self._value = value

        if self.length is Length.Byte9:
            check1 = self._check_crc(data[0], data[1], data[2])
            check2 = self._check_crc(data[3], data[4], data[5])
            if (check1 is False) or (check2 is False):
                return

            error, value = self._decode_u32(data[0], data[1], data[3], data[4])
            if error != 0:
                self._error = error
                return

            self._value = value

        self._success = True
        return

    def info(self):
        easyb.log.inform("ADDRESS", str(self.address))
        easyb.log.inform("CODE", str(self.code))
        easyb.log.inform("PRIORITY", str(self.priority.name))
        easyb.log.inform("LENGTH", str(self.length.name))
        easyb.log.inform("DIRECTION", str(self.direction.name))
        return
