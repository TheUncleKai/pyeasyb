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

from numpy import uint8, uint16, uint32, bitwise_and, bitwise_or, bitwise_xor, left_shift, right_shift

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
    def _decode_u16(bytea: uint8, byteb: uint8) -> uint16:
        itema = left_shift(uint16(255 - bytea), 8)
        itemb = uint16(byteb)

        data = uint16(bitwise_or(itema, itemb))
        return data

    def decode(self, answer: list) -> bool:
        return True
