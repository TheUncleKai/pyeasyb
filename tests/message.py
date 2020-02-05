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

import easyb.command
import easyb.message

from easyb.definitions import Direction, Length, Priority

__all__ = [
    "TestMessage"
]


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

        self.assertNotEqual(message, None)
        self.assertIs(message.address, 0)
        self.assertIs(message.code, 0)
        self.assertEqual(message.priority, Priority.NoPriority)
        self.assertEqual(message.length, Length.Byte3)
        self.assertEqual(message.direction, Direction.FromMaster)
        self.assertEqual(message.param, [])
        self.assertIsNone(message.stream)
        return

    def test_message_2(self):
        message = easyb.message.Message(address=1, code=1, priority=Priority.Priority,
                                        length=Length.Byte6, direction=Direction.FromSlave,
                                        param=[1, 0])

        self.assertNotEqual(message, None)
        self.assertIs(message.address, 1)
        self.assertIs(message.code, 1)
        self.assertEqual(message.priority, Priority.Priority)
        self.assertEqual(message.length, Length.Byte6)
        self.assertEqual(message.direction, Direction.FromSlave)
        self.assertEqual(message.param, [1, 0])
        self.assertIsNone(message.stream)
        return

    def test_command_1(self):
        message = easyb.message.Message()
        command = easyb.command.Command(name="Test", address=1, code=1, length=Length.Byte6, param=[2, 0])

        message.command(command)

        self.assertNotEqual(message, None)
        self.assertIs(message.address, 1)
        self.assertIs(message.code, 1)
        self.assertEqual(message.priority, Priority.NoPriority)
        self.assertEqual(message.length, Length.Byte6)
        self.assertEqual(message.direction, Direction.FromMaster)
        self.assertEqual(message.param, [2, 0])
        self.assertIsNone(message.stream)
        return

    def test_encode_1(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte6, direction=Direction.FromMaster,
                                        param=[202, 0])

        send = bytes([0xfe, 0xf2, 0xed, 0x35, 0x00, 0x47])

        check = message.encode()
        stream = message.stream
        self.assertTrue(check)
        self.assertEqual(stream.bytes, send)
        return

    def test_encode_2(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte3, direction=Direction.FromMaster)

        send = bytes([0xfe, 0xf0, 0xe3])

        check = message.encode()
        stream = message.stream
        self.assertTrue(check)
        self.assertEqual(stream.bytes, send)
        return

    def test_encode_3(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte6, direction=Direction.FromMaster,
                                        param=[202, 0, 0])

        check = message.encode()
        self.assertFalse(check)
        return

    def test_encode_4(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte6, direction=Direction.FromMaster,
                                        param=[202, 0, 0, 0])

        check = message.encode()
        self.assertFalse(check)
        return

    def test_encode_5(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte9, direction=Direction.FromMaster,
                                        param=[202, 0, 1, 0])

        send = bytes([254, 244, 255, 53, 0, 71, 254, 0, 61])

        check = message.encode()
        self.assertTrue(check)
        self.assertEqual(message.stream.bytes, send)
        return

    def test_encode_6(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Byte9, direction=Direction.FromMaster,
                                        param=[202, 0, 1, 0, 0, 0])

        check = message.encode()
        self.assertFalse(check)
        return

    def test_encode_7(self):
        message = easyb.message.Message(address=1, code=15, priority=Priority.NoPriority,
                                        length=Length.Variable, direction=Direction.FromMaster,
                                        param=[202, 0, 1, 0, 0, 0])

        check = message.encode()
        self.assertTrue(check)
        return

    def test_decode_1(self):
        header = [0xfe, 0xf5, 0xf8]

        message = easyb.message.Message()

        check = message.decode(bytes(header))

        message.info("TEST")

        self.assertTrue(check)
        self.assertEqual(message.address, 1)
        self.assertEqual(message.code, 15)
        self.assertEqual(message.priority, Priority.NoPriority)
        self.assertEqual(message.length, Length.Byte9)
        self.assertEqual(message.direction, Direction.FromSlave)
        return

    def test_decode_2(self):
        header = [0xfe, 0xf5, 0xfc]

        message = easyb.message.Message()

        check = message.decode(bytes(header))
        self.assertFalse(check)
        return

    def test_decode_3(self):
        header = [0xfe, 0xf5]

        message = easyb.message.Message()

        check = message.decode(bytes(header))
        self.assertFalse(check)
        return
