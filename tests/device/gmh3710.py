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

import easyb

from tests import TestSerial
from easyb.devices.gmh3710 import GMH3710
from easyb.logging import SerialLogging

__all__ = [
    "TestGMH3710"
]


old_logging = easyb.log
new_logging = SerialLogging()
new_logging.setup(app="Device", level=0)
console = new_logging.get_writer("console")
console.index.append("SERIAL")

# noinspection PyUnresolvedReferences
console.add_style("SERIAL", "BRIGHT", "YELLOW", "")
console.setup(text_space=15, error_index=["ERROR", "EXCEPTION"])
new_logging.register(console)
new_logging.open()


class TestGMH3710(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        easyb.set_logging(new_logging)
        return

    def tearDown(self):
        """tear down test.
        """
        easyb.set_logging(old_logging)
        return

    def test_constructor_1(self):
        """Test constructor.
        """
        device = GMH3710()

        self.assertNotEqual(device, None)
        self.assertEqual(device.name, "GMH 3710")
        self.assertEqual(device.port, "")
        self.assertEqual(device.baudrate, 4800)
        self.assertEqual(device.address, 0)
        self.assertEqual(device.write_timeout, 2)
        self.assertEqual(device.timeout, 2)
        self.assertEqual(device.wait_time, 0.1)
        self.assertIsNone(device.serial)
        return

    def test_constructor_2(self):
        """Test constructor.
        """
        device = GMH3710(port="TEST", baudrate=2400, address=2, write_timeout=3, timeout=60, wait_time=0.2)

        self.assertEqual(device.name, "GMH 3710")
        self.assertEqual(device.port, "TEST")
        self.assertEqual(device.baudrate, 2400)
        self.assertEqual(device.address, 2)
        self.assertEqual(device.write_timeout, 3)
        self.assertEqual(device.timeout, 60)
        self.assertEqual(device.wait_time, 0.2)
        self.assertIsNone(device.serial)
        return

    def test_command_01(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(0)
        self.assertTrue(check)
        return

    def test_command_02(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x70, 0xf6, 0x91, 0xdf, 0xed, 0x0b],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(0)
        self.assertFalse(check)
        return

    def test_command_03(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x3b, 0x9c],
            [0xfb, 0x00, 0x7c],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        status = device.device_status[10]

        check = device.run_command(1)
        self.assertTrue(check)
        self.assertEqual(status.bit, 0x0400)
        self.assertEqual(status.is_set, True)
        self.assertEqual(status.text, "Sensor error")
        return

    def test_command_04(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(1)
        self.assertTrue(check)
        return

    def test_command_05(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(2)
        self.assertTrue(check)
        self.assertEqual(device.min_value, 19.15)
        return

    def test_command_06(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x70, 0xf6, 0x91, 0xdf, 0xed, 0x0b],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(2)
        self.assertFalse(check)
        self.assertEqual(device.min_value, 0.0)
        return

    def test_command_07(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(3)
        self.assertTrue(check)
        self.assertEqual(device.max_value, 19.15)
        return

    def test_command_08(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x70, 0xf6, 0x91, 0xdf, 0xed, 0x0b],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(3)
        self.assertFalse(check)
        self.assertEqual(device.max_value, 0.0)
        return

    def test_command_09(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(4)
        id_number = "{0:x}".format(device.id_number)

        self.assertTrue(check)
        self.assertEqual(id_number, "32407008")
        return

    def test_command_10(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(12)

        self.assertTrue(check)
        self.assertEqual(device.unit, "°C")
        return

    def test_command_11(self):
        """Test constructor.
        """
        data = [
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x04, 0x34],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.run_command(12)

        self.assertFalse(check)
        self.assertEqual(device.unit, "")
        return

    def test_prepare_01(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.prepare()
        self.assertTrue(check)
        return

    def test_prepare_02(self):
        data = [
            [0xfe, 0x3b, 0x9c],
            [0xfb, 0x00, 0x7c],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.prepare()
        self.assertFalse(check)
        return

    def test_prepare_03(self):
        data = [
            [0xfe, 0x33, 0xa5]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.prepare()
        self.assertFalse(check)
        return

    def test_prepare_04(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x67]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.prepare()
        self.assertFalse(check)
        return

    def test_prepare_05(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x04, 0x34],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check = device.prepare()
        self.assertFalse(check)
        return

    def test_run_01(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check1 = device.prepare()
        check2 = device.run()

        self.assertTrue(check1)
        self.assertTrue(check2)
        return

    def test_run_02(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
            [0xfe, 0x05, 0x27]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check1 = device.prepare()
        check2 = device.run()

        self.assertTrue(check1)
        self.assertFalse(check2)
        return

    def test_run_03(self):
        data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f],
            [0xfe, 0x0d, 0x1e],
            [0x70, 0xf6, 0x91, 0xdf, 0xed, 0x0b],
        ]

        serial = TestSerial()
        serial.read_data = data

        device = GMH3710(port="TEST", baudrate=2400, address=1, write_timeout=3, timeout=60, wait_time=0.2)
        device.serial = serial

        check1 = device.prepare()
        check2 = device.run()

        self.assertTrue(check1)
        self.assertFalse(check2)
        return
