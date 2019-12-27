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

from numpy import uint8, uint16, uint32, uint64, bitwise_and, bitwise_or, bitwise_xor, left_shift, right_shift, power, \
    true_divide

from typing import List, Any
from easyb.definitions import MessageDirection, MessageLength, MessagePriority

__all__ = [
    "ExceptionEncodeByte6",
    "ExceptionEncodeByte9",

    "Message"
]


class ExceptionEncodeByte6(Exception):

    def __init___(self):
        Exception.__init__(self, "Not enough data for 6 Byte message!")


class ExceptionEncodeByte9(Exception):

    def __init___(self):
        Exception.__init__(self, "Not enough data for 9 Byte message!")


class Message(object):

    @property
    def address(self) -> int:
        return self._address

    @property
    def code(self) -> int:
        return self._code

    @property
    def priority(self) -> MessagePriority:
        return self._priority

    @property
    def length(self) -> MessageLength:
        return self._length

    @property
    def direction(self) -> MessageDirection:
        return self._direction

    @property
    def command(self) -> List[int]:
        return self._command

    @property
    def answer(self) -> List[Any]:
        return self._answer

    def error(self) -> int:
        return self._error

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
        self._priority = MessagePriority.NoPriority
        self._length = MessageLength.Byte3
        self._direction = MessageDirection.FromMaster
        self._command = []
        self._answer = []
        self._error = 0

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

        item = kwargs.get("command", None)
        if item is not None:
            self._command = item
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

    def encode(self) -> List[int]:
        result = []

        byte = self._encode_start(self.address)
        result.append(byte)

        byte = self._encode_header()
        result.append(byte)

        byte = self._crc(result[0], result[1])
        result.append(byte)

        if (self.length == MessageLength.Byte6) and (len(self.command) != 2):
            raise ExceptionEncodeByte6()

        if (self.length == MessageLength.Byte9) and (len(self.command) != 4):
            raise ExceptionEncodeByte9()

        if (self.length == MessageLength.Byte6) or (self.length == MessageLength.Byte9):
            byte = self._encode_start(self.command[0])
            result.append(byte)

            byte = self.command[1]
            result.append(byte)

            byte = self._crc(result[3], result[4])
            result.append(byte)

        if self.length == MessageLength.Byte9:
            byte = self._encode_start(self.command[2])
            result.append(byte)

            byte = self.command[3]
            result.append(byte)

            byte = self._crc(result[6], result[7])
            result.append(byte)
        return result

    @staticmethod
    def _convert_u16(inputa: uint8, inputb: uint8) -> uint16:
        itema = left_shift(uint16(255 - inputa), 8)
        itemb = uint16(inputb)

        data = uint16(bitwise_or(itema, itemb))
        return data

    @staticmethod
    def _convert_u32(inputa: uint16, inputb: uint16) -> uint32:
        itema = uint32(left_shift(inputa, 16))
        itemb = uint32(inputb)

        data = uint32(bitwise_or(itema, itemb))
        return data

    def _decode_u16(self, byte3: uint8, byte4: uint8) -> bool:

        u16_integer = self._convert_u16(byte3, byte4)
        float_pos = uint16(bitwise_and(u16_integer, 0xc000))
        float_pos = uint16(right_shift(float_pos, 14))

        u16_integer = uint16(bitwise_and(u16_integer, 0x3fff))

        if (u16_integer >= 0x3fe0) and (u16_integer <= 0x3fff):
            error = int(u16_integer) - 16352
            self._error = error
            return False

        denominator = uint32(power(10, float_pos))
        numerator = uint32(u16_integer - 2048)

        float_value = float(true_divide(numerator, denominator))
        self._answer.append(float_value)
        self._error = 0
        return True

    def _decode_u32(self, byte3: uint8, byte4: uint8, byte6: uint8, byte7: uint8) -> bool:
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
            self._error = error
            return False

        float_value = float(u32_integer)
        float_value = float(true_divide(float_value, power(10, float_pos)))
        self._answer.append(float_value)
        self._error = 0
        return True

    def _check_crc(self, byte1: int, byte2: int, crc: int) -> bool:

        check_crc = self._crc(byte1, byte2)

        if check_crc == crc:
            return True

        easyb.log.error("CRC check failed: {0:x} {1:x}, crc {2:x}, calculated {3:x}".format(byte1, byte2, crc, check_crc))
        return False

    def decode(self, answer: list) -> bool:
        self._error = 0

        if len(answer) == 3:
            check = self._check_crc(answer[0], answer[1], answer[2])
            if check is False:
                return False

        if len(answer) == 6:
            check = self._check_crc(answer[0], answer[1], answer[2])
            if check is False:
                return False

            check = self._check_crc(answer[3], answer[4], answer[5])
            if check is False:
                return False

        if len(answer) == 3:
            check = self._check_crc(answer[0], answer[1], answer[2])
            if check is False:
                return False

            check = self._check_crc(answer[3], answer[4], answer[5])
            if check is False:
                return False

            check = self._check_crc(answer[6], answer[7], answer[8])
            if check is False:
                return False
        return True
