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

import os
import time
import threading
import unittest.mock as mock

import unittest

import easyb

from serial import SerialException

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from easyb.definitions import Direction, Length, Priority
from easyb.command import Command
from tests import TestDevice, TestException, TestSerial
from easyb.logging import SerialLogging

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


class TestControl(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        """set up test.
        """
        easyb.set_logging(new_logging)
        return

    def tearDown(self):
        """tear down test.
        """
        easyb.set_logging(old_logging)
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
        self.assertEqual(len(device.command_list), 1)
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

        device.serial = mock_serial
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

        device.serial = mock_serial
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

        device.serial = mock_serial
        device.serial.is_open = True
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

        device.serial = mock_serial
        device.serial.is_open = False
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

        device.serial = mock_serial
        device.serial.is_open = True
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

    def test_send_1(self):
        device = TestDevice()

        mock_serial = mock.Mock()

        device.serial = mock_serial
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

    def test_send_2(self):
        device = TestDevice()

        mock_serial = mock.Mock()

        device.serial = mock_serial
        mock_serial.write = mock.Mock()
        mock_serial.write.return_value = 3

        message = easyb.message.Message(address=1, code=0, priority=Priority.NoPriority,
                                        length=Length.Byte6, direction=Direction.FromMaster)

        check = device.send(message)

        self.assertFalse(check)
        return

    def test_send_3(self):
        device = TestDevice()

        mock_serial = mock.Mock()

        device.serial = mock_serial
        mock_serial.write = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))
        mock_serial.write.return_value = 3

        message = easyb.message.Message(address=1, code=0, priority=Priority.NoPriority,
                                        length=Length.Byte3, direction=Direction.FromMaster)

        check = device.send(message)

        self.assertFalse(check)
        return

    def test_read_receive_1(self):
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]
        ]

        device = TestDevice()

        mock_serial = mock.Mock()

        read = TestSerial()
        read.read_data = data

        device.serial = mock_serial
        mock_serial.read = read.read

        message = device.receive()

        self.assertIsNotNone(message)
        self.assertEqual(message.address, 1, 'Failed: address')
        self.assertEqual(message.length, Length.Byte9, 'Failed: length')
        self.assertEqual(message.direction, Direction.FromSlave, 'Failed: direction')
        self.assertEqual(message.priority, Priority.Priority, 'Failed: priority')
        return

    def test_read_receive_2(self):
        device = TestDevice()

        mock_serial = mock.Mock()

        device.serial = mock_serial
        mock_serial.read = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_read_receive_3(self):
        data = [
            [0xfe, 0x3d, 0x1e],
            [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_read_receive_4(self):
        data = [
            [0xfe, 0x51, 0x8d]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_read_receive_5(self):
        data = [
            [254, 1, 58]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNotNone(message)
        return

    def test_read_receive_6(self):
        data = [
            [254, 3, 52],
            [0x72, 0xff, 0x84]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNotNone(message)
        self.assertEqual(message.address, 1)
        self.assertEqual(message.code, 0)
        self.assertEqual(message.length, Length.Byte6)
        self.assertEqual(message.direction, Direction.FromSlave)
        self.assertEqual(message.priority, Priority.NoPriority)
        self.assertEqual(message.stream.data, [254, 3, 52, 0x72, 0xff, 0x84])
        return

    def test_read_receive_7(self):
        data = [
            [254, 7, 40],
            [141],
            [255],
            [83],
            [141],
            [255],
            [83],
            [141],
            [255],
            [83],
            []
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNotNone(message)
        self.assertEqual(message.address, 1)
        self.assertEqual(message.code, 0)
        self.assertEqual(message.length, Length.Variable)
        self.assertEqual(message.direction, Direction.FromSlave)
        self.assertEqual(message.priority, Priority.NoPriority)
        self.assertEqual(message.stream.data, [254, 7, 40, 141, 255, 83, 141, 255, 83, 141, 255, 83])
        return

    def test_read_receive_8(self):
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data
        serial.read_exception = TestException(1, SerialException("Attempting to use a port that is not open"))

        device.serial = serial

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_read_receive_9(self):
        data = [
            [254, 7, 40],
            [141],
            [255],
            [83],
            [141],
            [255],
            [83],
            [141],
            [255],
            [83],
            []
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data
        serial.read_exception = TestException(1, SerialException("Attempting to use a port that is not open"))

        device.serial = serial

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_read_receive_10(self):
        data = [
            [0xfe, 0x0d, 0x1e],
            [0x72, 0xff, 0x84]
        ]

        device = TestDevice()

        serial = TestSerial()
        serial.read_data = data

        device.serial = serial

        message = device.receive()

        self.assertIsNone(message)
        return

    def test_status_1(self):
        device = TestDevice()

        status = 0x8000 | 0x0400

        count = device.set_status(status)

        states = device.get_status()

        self.assertEqual(count, 2)
        self.assertEqual(len(states), 2)
        self.assertEqual(states[0].bit, 0x0400)
        self.assertEqual(states[1].bit, 0x8000)
        return

    def test_execute_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        command = Command(name="Messwert lesen", code=0)

        message = device.execute(command)

        self.assertIsNotNone(message)
        self.assertEqual(len(message.stream.data), 9)
        return

    def test_execute_2(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data
        serial.write_exception = TestException(0, SerialException("Attempting to use a port that is not open"))

        device = TestDevice()
        device.serial = serial

        command = Command(name="Messwert lesen", code=0)

        message = device.execute(command)

        self.assertIsNone(message)
        return

    def test_execute_3(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data
        serial.read_exception = TestException(0, SerialException("Attempting to use a port that is not open"))

        device = TestDevice()
        device.serial = serial

        command = Command(name="Messwert lesen", code=0)

        message = device.execute(command)

        self.assertIsNone(message)
        return

    def test_run_command_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        check = device.run_command(0)
        message = device.message

        self.assertTrue(check)
        self.assertIsNotNone(message)
        self.assertEqual(len(message.stream.data), 9)
        return

    def test_run_command_2(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        check = device.run_command(1)
        self.assertFalse(check)
        return

    def test_run_command_3(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data
        serial.read_exception = TestException(0, SerialException("Attempting to use a port that is not open"))

        device = TestDevice()
        device.serial = serial

        check = device.run_command(0)
        self.assertFalse(check)
        return

    def test_add_command_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        command = Command(name="Messwert lesen", code=0, func_call=device.default_command)
        device.add_command(command)
        device.list_commands()

        check = device.run_command(1)
        self.assertTrue(check)
        self.assertEqual(len(device.commands), 2)
        return

    def test_run_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        command = Command(name="Messwert lesen 2", code=0, func_call=device.default_command)
        device.add_command(command)

        check1 = device.prepare()
        check2 = device.run()
        check3 = device.close()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertTrue(check3)
        return

    def test_run_loop_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        check1 = device.prepare()

        thread = threading.Thread(target=device.run_loop)
        thread.start()
        time.sleep(0.1)

        while True:
            check = device.active
            if check is False:
                break

            if device.interval_counter == 5:
                device.do_abort(None, None)

            time.sleep(0.01)

        check3 = device.close()

        self.assertTrue(check1)
        self.assertTrue(device.status)
        self.assertTrue(check3)
        return

    def test_run_loop_2(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        column = device.data.columns[0]
        column.type = None

        self.assertRaises(ValueError, device.run_loop)
        return

    def test_store_1(self):
        data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25],
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf8, 0x7b, 0x25]
        ]

        serial = TestSerial()
        serial.read_data = data

        device = TestDevice()
        device.serial = serial

        thread = threading.Thread(target=device.run_loop)
        thread.start()
        time.sleep(0.1)

        while True:
            check = device.active
            if check is False:
                break

            if device.interval_counter == 5:
                device.do_abort(None, None)

            time.sleep(0.01)

        check1 = device.store("EXCEL", "test")
        check2 = os.path.exists("test.xlsx")
        self.assertTrue(device.status)
        self.assertTrue(check1)
        self.assertTrue(check2)
        os.remove("test.xlsx")
        return
