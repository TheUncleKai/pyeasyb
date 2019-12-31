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

import easyb.device
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from easyb.definitions import Direction, Length, Priority

mock_serial = mock.Mock()


class TestControl(unittest.TestCase):
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

    def test_constructor(self):
        """Test constructor.
        """
        device = easyb.device.Device("TEST")

        self.assertNotEqual(device, None, "Failed: test_constructor")
        self.assertIs(device.port, "TEST", "Failed: set port")
        self.assertIsNone(device.ser, "Failed: serial not None")
        return

    def test_setup(self):
        """Test constructor.
        """
        device = easyb.device.Device("TEST")
        device.setup()

        self.assertIsNotNone(device.ser, "Failed: serial is None")
        self.assertEqual(device.ser.bytesize, EIGHTBITS)
        self.assertEqual(device.ser.parity, PARITY_NONE)
        self.assertEqual(device.ser.stopbits, STOPBITS_ONE)
        self.assertEqual(device.ser.timeout, 6)
        self.assertEqual(device.ser.writeTimeout, 2)
        self.assertEqual(device.ser.rtscts, 0)
        self.assertEqual(device.ser.dsrdtr, 0)
        self.assertEqual(device.ser.xonxoff, 0)
        self.assertIsNone(device.ser.interCharTimeout)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_write(self):
        device = easyb.device.Device("TEST")

        device._ser = mock_serial
        mock_serial.write = mock.Mock()
        mock_serial.write.return_value = 3

        message = easyb.message.Message(address=1, code=0, priority=Priority.NoPriority,
                                        length=Length.Byte3, direction=Direction.FromMaster)

        check = device.send(message)

        arg_check = bytes([254, 0, 61])

        args, _ = mock_serial.write.call_args

        self.assertTrue(check)
        self.assertTrue(mock_serial.write.called, 'Serial write method not called')
        self.assertEqual(args[0], arg_check)
        return
