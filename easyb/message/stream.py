#!/usr/bin/python3
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

from typing import List, Union
from easyb.definitions import Length
from easyb.bit import debug_data, check_crc, crop_u8, create_crc

__all__ = [
    "Stream"
]


class Stream(object):

    def __init__(self, length: Length):
        self._data = []
        self.length = length
        return

    @property
    def length(self) -> Length:
        return self._length

    @length.setter
    def length(self, in_length: Length):
        self._length = in_length

        if self._length is Length.Byte3:
            self._expand_data(3)

        if self._length is Length.Byte6:
            self._expand_data(6)

        if self._length is Length.Byte9:
            self._expand_data(9)
        return

    @property
    def data(self) -> List[int]:
        return self._data

    @property
    def bytes(self) -> bytes:
        res = bytes(self._data)
        return res

    @property
    def len(self) -> int:
        return len(self._data)

    def __str__(self):
        return debug_data(self.bytes)

    def __repr__(self):
        return debug_data(self.bytes)

    def _expand_data(self, number):
        if number == self.len:
            return

        n = self.len
        while n < number:
            self._data.append(0)
            n += 1
        return

    def encode(self) -> bool:
        length = len(self.data)
        check = False

        for item in self.data:
            if item != 0:
                check = True

        if check is False:
            easyb.log.error("Data is empty!")
            return False

        pos_set = 0
        while True:
            if pos_set >= length:
                break

            pos1 = pos_set + 0
            pos2 = pos_set + 1
            pos3 = pos_set + 2

            byte1 = crop_u8(255 - self.data[pos1])
            byte2 = self.data[pos2]
            crc = create_crc(byte1, byte2)

            self.data[pos1] = byte1
            self.data[pos2] = byte2
            self.data[pos3] = crc

            pos_set += 3
        return True

    def decode(self, data_input: bytes):
        self._data = []

        for item in data_input:
            self._data.append(int(item))

        length = len(self.data)

        if length == 0:
            easyb.log.error("Data packet is empty!")
            return False

        check = length % 3
        if check != 0:
            easyb.log.error("Data size is not a triplet! ({0:d})".format(length))
            return False

        check = self.verify_crc()
        return check

    def append(self, data_input: bytes):
        length = len(data_input)

        if length == 0:
            easyb.log.error("Data packet is empty!")
            return False

        check = length % 3
        if check != 0:
            easyb.log.error("Data size is not a triplet! ({0:d})".format(length))
            return False

        for item in data_input:
            self._data.append(int(item))

        check = self.verify_crc()
        return check

    def verify_length(self) -> bool:
        length = len(self.data)

        if length == 0:
            easyb.log.error("Data is empty!")
            return False

        check = length % 3
        if check != 0:
            easyb.log.error("Data size is not a triplet! ({0:d})".format(length))
            return False

        if (self.length is Length.Byte3) and (length != 3):
            easyb.log.error("Invalid data length for Byte6: " + str(length))
            return False

        if (self.length is Length.Byte6) and (length != 6):
            easyb.log.error("Invalid data length for Byte6: " + str(length))
            return False

        if (self.length is Length.Byte9) and (length != 9):
            easyb.log.error("Invalid data length for Byte9: " + str(length))
            return False

        return True

    def verify_crc(self) -> bool:
        length = len(self.data)

        pos_set = 0
        while True:
            if pos_set >= length:
                break

            byte1 = self.data[pos_set + 0]
            byte2 = self.data[pos_set + 1]
            crc = self.data[pos_set + 2]

            check = check_crc(byte1, byte2, crc)
            if check is False:
                return False

            pos_set += 3
        return True

    def set_data(self, data_input) -> bool:
        length = len(data_input)

        if length != self.len:
            easyb.log.error("Invalid data size of {0:d}, need {1:d}!".format(length, self.len))
            return False

        n = 0
        for item in data_input:
            value = int(item)
            self.data[n] = value
            n += 1
        return True
