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

import easyb.bit


# noinspection DuplicatedCode
class TestBit(unittest.TestCase):
    """Testing class for message coding and decoding module."""

    def setUp(self):
        """set up test.
        """
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_create_crc(self):

        byte1 = 0xfe
        byte2 = 0x00

        crc = easyb.bit.create_crc(byte1, byte2)

        self.assertEqual(crc, 0x3d, "Failed: crc: " + hex(crc))
        return

    def test_check_crc_1(self):

        check = easyb.bit.check_crc(0xfe, 0x00, 0x3d)

        self.assertIs(check, True, "Failed: crc")
        return

    def test_check_crc_2(self):

        check = easyb.bit.check_crc(0xfe, 0x00, 0x3c)

        self.assertIs(check, False, "Failed: crc")
        return

    def test_decode_u32(self):
        error, value = easyb.bit.decode_u32(0x72, 0xff, 0x00, 0xfc)

        self.assertIsNone(error)
        self.assertEqual(value, -0.04)
        return

    def test_encode_u32_1(self):
        value = -0.04
        check = [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        data = easyb.bit.encode_u32(value)
        self.assertListEqual(data, check, "Failed: encode_u32")
        return

    def test_encode_u32_2(self):
        value = 53.84

        data = easyb.bit.encode_u32(value)
        error, check = easyb.bit.decode_u32(data[0], data[1], data[3], data[4])
        self.assertIsNone(error)
        self.assertEqual(check, value)
        return
