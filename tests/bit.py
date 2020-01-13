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

import unittest

from easyb.bit import Value, debug_data


# noinspection DuplicatedCode
class TestBit(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_debug_data(self):
        data = [255, 0, 5]
        tests = "0xff 0x00 0x05"
        value = debug_data(bytes(data))

        self.assertEqual(tests, value)
        return

    def test_create_crc(self):

        bitio = Value()

        byte1 = 0xfe
        byte2 = 0x00

        crc = bitio.create_crc(byte1, byte2)

        self.assertEqual(crc, 0x3d)
        return

    def test_crop_u8_1(self):
        bitio = Value()

        value1 = 0xffffffffffffffff
        value2 = 0x00000000000000ff

        value = bitio.crop_u8(value1)
        self.assertEqual(value2, value)
        return

    def test_crop_u8_2(self):
        bitio = Value()

        value1 = 0xffffffff
        value2 = 0x000000ff

        value = bitio.crop_u8(value1)
        self.assertEqual(value2, value)
        return

    def test_crop_u8_3(self):
        bitio = Value()

        value1 = 0xfff
        value2 = 0x0ff

        value = bitio.crop_u8(value1)
        self.assertEqual(value2, value)
        return

    def test_crop_u16_1(self):
        bitio = Value()

        value1 = 0xffffffff
        value2 = 0x0000ffff

        value = bitio.crop_u16(value1)
        self.assertEqual(value2, value)
        return

    def test_crop_u16_2(self):
        bitio = Value()

        value1 = 0xffffffffffffffff
        value2 = 0x000000000000ffff

        value = bitio.crop_u16(value1)
        self.assertEqual(value2, value)
        return

    def test_crop_u32_1(self):
        bitio = Value()

        value1 = 0xffffffffffffffff
        value2 = 0x00000000ffffffff

        value = bitio.crop_u32(value1)
        self.assertEqual(value2, value)
        return

    def test_check_crc_1(self):
        bitio = Value()

        check = bitio.check_crc(0xfe, 0x00, 0x3d)

        self.assertIs(check, True)
        return

    def test_check_crc_2(self):
        bitio = Value()

        check = bitio.check_crc(0xfe, 0x00, 0x3c)

        self.assertIs(check, False)
        return

    def test_value_decode_u32_1(self):
        data = [0, 0, 0, 0x72, 0xff, 0, 0x00, 0xfc]

        bitio = Value(data=data)

        check = bitio.value_decode_u32()

        self.assertTrue(check)
        self.assertIsNone(bitio.error)
        self.assertEqual(bitio.value, -0.04)
        return

    def test_value_decode_u32_2(self):
        data = [0xfe, 0x65, 0x01, 0x70, 0xf6, 0x91, 0xdf, 0xed, 0x0b]

        bitio = Value(data=data)

        check = bitio.value_decode_u32()

        self.assertFalse(check)
        self.assertIsNotNone(bitio.error)
        self.assertEqual(bitio.value, 0.0)
        self.assertEqual(bitio.error.text, "No sensor")
        return

    def test_encode_u32_1(self):
        value = -0.04
        check = [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        bitio = Value(value=value)
        bitio.encode_u32()

        self.assertListEqual(bitio.data, check)
        return

    def test_encode_u32_2(self):
        value = 53.84

        bitio1 = Value(value=value)
        bitio1.encode_u32()

        data = [0, 0, 0]

        for item in bitio1.data:
            data.append(item)

        bitio2 = Value(data=data)
        check = bitio2.value_decode_u32()

        self.assertIsNone(bitio1.error)
        self.assertIsNone(bitio2.error)
        self.assertTrue(check)

        self.assertEqual(value, bitio2.value)
        return
