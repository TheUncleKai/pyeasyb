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

import easyb.message

from easyb.definitions import MessageDirection, MessageLength, MessagePriority


# noinspection DuplicatedCode
class TestMessage(unittest.TestCase):
    """Testing class for message coding and decoding module."""

    def setUp(self):
        """set up test.
        """
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_message_1(self):
        message = easyb.message.Message()

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 0, "Failed: address")
        self.assertIs(message.code, 0, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.NoPriority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte3, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromMaster, "Failed: direction")
        return

    def test_message_2(self):
        message = easyb.message.Message(address=1, code=1, priority=MessagePriority.Priority,
                                        length=MessageLength.Byte6, direction=MessageDirection.FromSlave)

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 1, "Failed: address")
        self.assertIs(message.code, 1, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.Priority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte6, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromSlave, "Failed: direction")
        return

    def test_encode_1(self):
        message = easyb.message.Message(address=1, code=0, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte3, direction=MessageDirection.FromMaster)

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 1, "Failed: address")
        self.assertIs(message.code, 0, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.NoPriority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte3, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromMaster, "Failed: direction")

        result = message.encode()

        byte0 = result[0]
        byte1 = result[1]
        byte2 = result[2]

        self.assertIs(byte0, 0xfe, "Failed: byte0: " + hex(byte0))
        self.assertIs(byte1, 0x00, "Failed: byte1: " + hex(byte1))
        self.assertIs(byte2, 0x3d, "Failed: byte2: " + hex(byte2))
        return

    def test_encode_2(self):
        """Test constructor.
        """
        message = easyb.message.Message(address=2, code=3, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte3, direction=MessageDirection.FromMaster)

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 2, "Failed: address")
        self.assertIs(message.code, 3, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.NoPriority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte3, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromMaster, "Failed: direction")

        result = message.encode()

        byte0 = result[0]
        byte1 = result[1]
        byte2 = result[2]

        self.assertIs(byte0, 0xfd, "Failed: byte0: " + hex(byte0))
        self.assertIs(byte1, 0x30, "Failed: byte1: " + hex(byte1))
        self.assertIs(byte2, 0x92, "Failed: byte2: " + hex(byte2))
        return

    def test_encode_3(self):
        """Test constructor.
        """
        message = easyb.message.Message(address=3, code=0xf, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte6, direction=MessageDirection.FromMaster,
                                        command=[0xca, 0x00])

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 3, "Failed: address")
        self.assertIs(message.code, 0xf, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.NoPriority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte6, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromMaster, "Failed: direction")

        result = message.encode()

        byte0 = result[0]
        byte1 = result[1]
        byte2 = result[2]

        byte3 = result[3]
        byte4 = result[4]
        byte5 = result[5]

        self.assertIs(byte0, 0xfc, "Failed: byte0: " + hex(byte0))
        self.assertIs(byte1, 0xf2, "Failed: byte1: " + hex(byte1))
        self.assertIs(byte2, 0xc7, "Failed: byte2: " + hex(byte2))

        self.assertIs(byte3, 0x35, "Failed: byte3: " + hex(byte3))
        self.assertIs(byte4, 0x00, "Failed: byte4: " + hex(byte4))
        self.assertIs(byte5, 0x47, "Failed: byte5: " + hex(byte5))
        return

    def test_encode_4(self):
        """Test constructor.
        """
        message = easyb.message.Message(address=3, code=0xf, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte9, direction=MessageDirection.FromMaster,
                                        command=[0xca, 0x00, 0xca, 0x00])

        self.assertNotEqual(message, None, "Failed: constructor")
        self.assertIs(message.address, 3, "Failed: address")
        self.assertIs(message.code, 0xf, "Failed: code")
        self.assertEqual(message.priority, MessagePriority.NoPriority, "Failed: priority")
        self.assertEqual(message.length, MessageLength.Byte9, "Failed: length")
        self.assertEqual(message.direction, MessageDirection.FromMaster, "Failed: direction")

        result = message.encode()

        byte0 = result[0]
        byte1 = result[1]
        byte2 = result[2]

        byte3 = result[3]
        byte4 = result[4]
        byte5 = result[5]

        byte6 = result[6]
        byte7 = result[7]
        byte8 = result[8]

        self.assertIs(byte0, 0xfc, "Failed: byte0: " + hex(byte0))
        self.assertIs(byte1, 0xf4, "Failed: byte1: " + hex(byte1))
        self.assertIs(byte2, 0xd5, "Failed: byte2: " + hex(byte2))

        self.assertIs(byte3, 0x35, "Failed: byte3: " + hex(byte3))
        self.assertIs(byte4, 0x00, "Failed: byte4: " + hex(byte4))
        self.assertIs(byte5, 0x47, "Failed: byte5: " + hex(byte5))

        self.assertIs(byte6, 0x35, "Failed: byte6: " + hex(byte6))
        self.assertIs(byte7, 0x00, "Failed: byte7: " + hex(byte7))
        self.assertIs(byte8, 0x47, "Failed: byte8: " + hex(byte8))
        return

    def test_encode_5(self):
        message = easyb.message.Message(address=3, code=0xf, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte6, direction=MessageDirection.FromMaster,
                                        command=[0xca])

        self.assertRaises(easyb.message.ExceptionEncodeByte6, message.encode)
        return

    def test_encode_6(self):
        message = easyb.message.Message(address=3, code=0xf, priority=MessagePriority.NoPriority,
                                        length=MessageLength.Byte9, direction=MessageDirection.FromMaster,
                                        command=[0xca])

        self.assertRaises(easyb.message.ExceptionEncodeByte9, message.encode)
        return
