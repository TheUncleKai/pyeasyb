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

import easyb.device
from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, SerialException, SerialTimeoutException


class TestControl(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        """set up test.
        """
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_constructor(self):
        """Test constructor.
        """
        control = easyb.device.Control("TEST")

        self.assertNotEqual(control, None, "Failed: test_constructor")
        self.assertIs(control.port, "TEST", "Failed: set port")
        self.assertIsNone(control.ser, "Failed: serial not None")
        return

    def test_setup(self):
        """Test constructor.
        """
        control = easyb.device.Control("TEST")
        control.setup()

        self.assertIsNotNone(control.ser, "Failed: serial is None")
        self.assertEqual(control.ser.bytesize, EIGHTBITS)
        self.assertEqual(control.ser.parity, PARITY_NONE)
        self.assertEqual(control.ser.stopbits, STOPBITS_ONE)
        self.assertEqual(control.ser.timeout, 3)
        self.assertEqual(control.ser.writeTimeout, 2)
        self.assertEqual(control.ser.rtscts, 0)
        self.assertEqual(control.ser.dsrdtr, 0)
        self.assertEqual(control.ser.xonxoff, 0)
        self.assertIsNone(control.ser.interCharTimeout)
        return
