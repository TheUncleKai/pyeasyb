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
from easyb.device import Device
from easyb.command import Command
from serial import SerialException

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from easyb.definitions import Direction, Length, Priority


class TestDevice(Device):

    def __init__(self, **kwargs):
        Device.__init__(self, name="TEST-DEVICE", wait_time=0.1, address=1, **kwargs)
        return

    def init_commands(self):

        command = Command(name="Messwert lesen", code=0, func_call=self.default_command)
        self.commands.append(command)
        return

    def prepare(self):
        return

    def run(self):
        return

    def close(self):
        return


class TestRead(object):

    run = 0

    def test_read_1(self, count=0) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            data = [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]
        result = bytes(data)

        self.run += 1
        return result

    def test_read_2(self, count=0) -> bytes:
        result = bytes([])
        data = [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05, 0x00, 0xfc, 0x05]

        if self.run == 0:
            message = Message(code=0, address=1, priority=Priority.NoPriority, length=Length.Variable,
                              direction=Direction.FromMaster)

            result = message.encode()

        if (self.run > 0) and (self.run < 10):
            value = data[self.run - 1]
            result = bytes([value])

        if self.run > 9:
            result = bytes([])

        self.run += 1
        return result

    def test_read_3(self, count=0) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            raise SerialException('Attempting to use a port that is not open')
        result = bytes(data)

        self.run += 1
        return result

    def test_read_4(self, count=0) -> bytes:
        data = []

        if self.run == 0:
            data = [0xfe, 0x0d, 0x1e]
        if self.run == 1:
            data = [0x73, 0xff, 0x84, 0x00, 0xfc, 0x05]
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
        self.assertEqual(len(device.command_list), 0)
        self.assertIsNone(device.serial)
        return

    def test_setup(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"
        device.setup()

        self.assertIsNotNone(device.serial, "Failed: serial is None")
        self.assertEqual(device.serial.bytesize, EIGHTBITS)
        self.assertEqual(device.serial.parity, PARITY_NONE)
        self.assertEqual(device.serial.stopbits, STOPBITS_ONE)
        self.assertEqual(device.serial.timeout, 2)
        self.assertEqual(device.serial.writeTimeout, 2)
        self.assertEqual(device.serial.rtscts, 0)
        self.assertEqual(device.serial.dsrdtr, 0)
        self.assertEqual(device.serial.xonxoff, 0)
        self.assertIsNone(device.serial.interCharTimeout)
        return

    def test_connect_1(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._serial = mock_serial
        mock_serial.open = mock.Mock()

        check = device.connect()
        self.assertTrue(check)
        self.assertTrue(mock_serial.open.called, 'Serial open method not called')
        return

    def test_connect_2(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._serial = mock_serial
        mock_serial.open = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))

        check = device.connect()
        self.assertFalse(check)
        self.assertTrue(mock_serial.open.called, 'Serial open method not called')
        return

    def test_connect_3(self):
        """Test constructor.
        """

        device = TestDevice()

        mock_serial = mock.Mock()

        device._serial = mock_serial

        check = device.connect()
        self.assertFalse(check)
        self.assertFalse(mock_serial.open.called)
        return

    def test_connect_4(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        check = device.connect()
        self.assertFalse(check)
        return

    def test_disconnect_1(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._serial = mock_serial
        device._serial.is_open = True
        mock_serial.close = mock.Mock()

        check = device.disconnect()
        self.assertTrue(check)
        self.assertTrue(mock_serial.close.called, 'Serial close method not called')
        return

    def test_disconnect_2(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._serial = mock_serial
        device._serial.is_open = False
        mock_serial.close = mock.Mock()

        check = device.disconnect()
        self.assertFalse(check)
        self.assertFalse(mock_serial.close.called, 'Serial close method not called')
        return

    def test_disconnect_3(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        check = device.disconnect()
        self.assertFalse(check)
        return

    def test_disconnect_4(self):
        """Test constructor.
        """

        device = TestDevice()
        device.port = "TEST"

        mock_serial = mock.Mock()

        device._serial = mock_serial
        device._serial.is_open = True
        mock_serial.close = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))

        check = device.disconnect()
        self.assertFalse(check)
        self.assertTrue(mock_serial.close.called, 'Serial close method not called')
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

    # def test_send_1(self):
    #     device = TestDevice()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock()
    #     mock_serial.write.return_value = 3
    #
    #     message = easyb.message.Message(address=1, code=0, priority=Priority.NoPriority,
    #                                     length=Length.Byte3, direction=Direction.FromMaster)
    #
    #     check = device.send(message)
    #
    #     arg_check = bytes([254, 0, 61])
    #
    #     args, _ = mock_serial.write.call_args
    #
    #     self.assertTrue(check)
    #     self.assertTrue(mock_serial.write.called, 'Serial write method not called')
    #     self.assertEqual(args[0], arg_check)
    #     return
    #
    # def test_send_2(self):
    #     device = TestDevice()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))
    #
    #     message = easyb.message.Message(address=1, code=0, priority=Priority.NoPriority,
    #                                     length=Length.Byte3, direction=Direction.FromMaster)
    #
    #     check = device.send(message)
    #
    #     self.assertFalse(check)
    #     self.assertTrue(mock_serial.write.called)
    #     return
    #
    # def test_read_receive_1(self):
    #     device = TestDevice()
    #
    #     mock_serial = mock.Mock()
    #
    #     test_read = TestRead()
    #
    #     device._serial = mock_serial
    #     mock_serial.read = test_read.test_read_1
    #
    #     message = device.receive()
    #     message.value_32()
    #
    #     self.assertIsNotNone(message)
    #     self.assertEqual(message.address, 1, 'Failed: address')
    #     self.assertEqual(message.length, Length.Byte9, 'Failed: length')
    #     self.assertEqual(message.direction, Direction.FromSlave, 'Failed: direction')
    #     self.assertEqual(message.priority, Priority.Priority, 'Failed: priority')
    #     self.assertTrue(message.success, 'Failed: success')
    #     self.assertEqual(message.value, -0.04)
    #     return
    #
    # def test_read_receive_2(self):
    #     device = TestDevice()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.read = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))
    #
    #     message = device.receive()
    #
    #     self.assertIsNone(message)
    #     return
    #
    # def test_read_receive_3(self):
    #     device = TestDevice()
    #
    #     test_read = TestRead()
    #     test_read.run = 0
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.read = test_read.test_read_2
    #
    #     message = device.receive()
    #
    #     self.assertIsNotNone(message)
    #
    #     return
    #
    # def test_read_receive_4(self):
    #     device = TestDevice()
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.read = test_read.test_read_3
    #
    #     message = device.receive()
    #
    #     self.assertIsNone(message)
    #     return
    #
    # def test_execute_1(self):
    #     device = TestDevice()
    #     command = device.get_command(0)
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock()
    #     mock_serial.write.return_value = 3
    #     mock_serial.read = test_read.test_read_1
    #
    #     message = device.execute(command)
    #
    #     self.assertIsNotNone(message)
    #     return
    #
    # def test_execute_2(self):
    #     device = TestDevice()
    #     command = device.get_command(0)
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))
    #     mock_serial.read = test_read.test_read_1
    #
    #     message = device.execute(command)
    #
    #     self.assertIsNone(message)
    #     return
    #
    # def test_execute_3(self):
    #     device = TestDevice()
    #     command = device.get_command(0)
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock()
    #     mock_serial.write.return_value = 3
    #     mock_serial.read = test_read.test_read_2
    #
    #     message = device.execute(command)
    #
    #     self.assertIsNotNone(message)
    #     return
    #
    # def test_execute_4(self):
    #     device = TestDevice()
    #     command = device.get_command(0)
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock()
    #     mock_serial.write.return_value = 3
    #     mock_serial.read = test_read.test_read_4
    #
    #     message = device.execute(command)
    #
    #     self.assertIsNone(message)
    #     return
    #
    # def test_run_1(self):
    #     device = TestDevice()
    #
    #     test_read = TestRead()
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock()
    #     mock_serial.write.return_value = 3
    #     mock_serial.read = test_read.test_read_1
    #
    #     check = device.run_command(0)
    #     self.assertTrue(check)
    #     return
    #
    # def test_run_2(self):
    #     device = TestDevice()
    #
    #     test_read = TestRead()
    #
    #     mock_serial = mock.Mock()
    #
    #     device._serial = mock_serial
    #     mock_serial.write = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))
    #     mock_serial.read = test_read.test_read_1
    #
    #     check = device.run_command(0)
    #     self.assertFalse(check)
    #     return
    #
    # def test_run_3(self):
    #     device = TestDevice()
    #
    #     check = device.run_command(1)
    #     self.assertFalse(check)
    #     return
