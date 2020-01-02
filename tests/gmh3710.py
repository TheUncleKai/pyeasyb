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

import unittest.mock as mock
import unittest

import easyb

from easyb.message import Message


from serial import SerialException

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from easyb.definitions import Direction, Length, Priority

from easyb.devices.gmh3710 import GMH3710


class TestRead(object):

    run = 0

    def test_read_1(self, count) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            data = [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]
        result = bytes(data)

        self.run += 1
        return result

    def test_read_2(self, count) -> bytes:

        message = Message(code=0, address=1, priority=Priority.NoPriority, length=Length.Variable,
                          direction=Direction.FromMaster)

        result = message.encode()
        return result

    def test_read_3(self, count) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            raise SerialException('Attempting to use a port that is not open')
        result = bytes(data)

        self.run += 1
        return result

    def test_read_4(self, count) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            data = [0x73, 0xff, 0x84, 0x00, 0xfc, 0x05]
        result = bytes(data)

        self.run += 1
        return result


class TestGMH3710(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        """set up test.
        """
        easyb.log.level = 2
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_constructor_1(self):
        """Test constructor.
        """
        device = GMH3710(port="TEST")

        self.assertNotEqual(device, None)
        self.assertEqual(device.name, "GMH 3710")
        self.assertEqual(device.port, "TEST")
        self.assertEqual(device.wait_time, 0.1)
        self.assertIsNone(device.ser)
        return

    def test_constructor_2(self):
        """Test constructor.
        """
        device = GMH3710(address=2)
        device.port = "TEST"

        self.assertNotEqual(device, None)
        self.assertEqual(device.name, "GMH 3710")
        self.assertEqual(device.port, "TEST")
        self.assertEqual(device.wait_time, 0.1)
        self.assertEqual(device.address, 2)
        self.assertIsNone(device.ser)
        return
