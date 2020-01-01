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

from easyb.device import Device
from easyb.command import Command
from serial import SerialException

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from easyb.definitions import Direction, Length, Priority


class TestDevice(Device):

    def __init__(self, **kwargs):
        self._address = 1

        item = kwargs.get("address", 1)
        if item is not None:
            self._address = item

        Device.__init__(self, "TEST-DEVICE", 0.1)
        return

    def read_measurement(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        easyb.log.inform("VALUE", str(message.value))
        return True

    def init_commands(self):

        command = Command(name="Messwert lesen", number=0, address=self._address, code=0,
                          func_call=self.read_measurement)
        self.commands.append(command)
        return


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
        device = TestDevice()
        device.port = "TEST"

        self.assertNotEqual(device, None)
        self.assertEqual(device.name, "TEST-DEVICE")
        self.assertEqual(device.port, "TEST")
        self.assertEqual(device.wait_time, 0.1)
        self.assertIsNone(device.ser)
        return

    def test_setup(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"
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

    def test_open_1(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._ser = mock_serial
        mock_serial.open = mock.Mock()

        check = device.open()
        self.assertTrue(check)
        self.assertTrue(mock_serial.open.called, 'Serial open method not called')
        return

    def test_open_2(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._ser = mock_serial
        mock_serial.open = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))

        check = device.open()
        self.assertFalse(check)
        self.assertTrue(mock_serial.open.called, 'Serial open method not called')
        return

    def test_open_3(self):
        """Test constructor.
        """

        device = TestDevice()

        mock_serial = mock.Mock()

        device._ser = mock_serial

        check = device.open()
        self.assertFalse(check)
        self.assertFalse(mock_serial.open.called, 'Serial open method not called')
        return

    def test_get_command_1(self):
        """Test constructor.
        """

        device = TestDevice()

        command = device.get_command(0)

        self.assertIsNotNone(command)
        self.assertEqual(command.name, "Messwert lesen")
        self.assertEqual(command.number, 0)
        self.assertEqual(command.address, 1)
        self.assertEqual(command.code, 0)
        return

    def test_get_command_2(self):
        """Test constructor.
        """

        device = TestDevice()

        command = device.get_command(1)

        self.assertIsNone(command)
        return

    def test_write(self):
        device = TestDevice()

        mock_serial = mock.Mock()

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

    def test_read(self):
        device = TestDevice()

        mock_serial = mock.Mock()

        test_read = TestRead()

        device._ser = mock_serial
        mock_serial.read = test_read.test_read_1

        message = device.receive()

        self.assertIsNotNone(message)
        self.assertEqual(message.address, 1, 'Failed: address')
        self.assertEqual(message.length, Length.Byte9, 'Failed: length')
        self.assertEqual(message.direction, Direction.FromSlave, 'Failed: direction')
        self.assertEqual(message.priority, Priority.Priority, 'Failed: priority')
        self.assertTrue(message.success, 'Failed: success')
        self.assertEqual(message.value, -0.04)
        return
