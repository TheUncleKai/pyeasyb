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

from typing import Tuple

from numpy import uint8, uint16, uint32, int32, uint64, bitwise_and, bitwise_or, bitwise_xor, left_shift, right_shift

__all__ = [
    "convert_u16",
    "convert_u32",

    "decode_u16",
    "decode_u32",

    "create_crc",
    "check_crc"
]


def convert_u16(bytea: int, byteb: int) -> int:
    data = (255 - bytea) << 8
    data = data | byteb
    return data


def convert_u32(inputa: int, inputb: int) -> int:
    data = (inputa << 16) | inputb
    return data


def decode_u16(byte3: uint8, byte4: uint8) -> Tuple[int, float]:
    u16_integer = convert_u16(byte3, byte4)
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


def decode_u32(byte3: uint8, byte4: uint8, byte6: uint8, byte7: uint8) -> Tuple[int, float]:
    u16_integer1 = convert_u16(byte3, byte4)
    u16_integer2 = convert_u16(byte6, byte7)
    u32_integer = convert_u32(u16_integer1, u16_integer2)

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


def create_crc(byte1: int, byte2: int) -> int:
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


def check_crc(byte1: int, byte2: int, crc: int) -> bool:
    value_crc = create_crc(byte1, byte2)

    if value_crc == crc:
        return True

    error_text = "CRC check failed: {0:s} {1:s}, crc {2:s}, calculated {3:s}".format(hex(byte1), hex(byte2), hex(crc),
                                                                                     hex(value_crc))
    easyb.log.error(error_text)
    return False
