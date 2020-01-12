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
import unittest.mock as mock

from easyb.console import Console
from serial import SerialException

mock_serial = mock.Mock()
mock_serial_2 = mock.Mock()


class TestOptions(object):

    def __init__(self):
        self.verbose = 0
        self.read = False
        self.list = False
        self.interval = 2.0

        self.device = ""
        self.command = 0

        self.port = ""
        self.baudrate = 4800
        self.timeout = 2
        self.writetimeout = 2

        self.output = "none"
        self.filename = "measurement"
        return


    def test_1(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 0

    def test_2(self):
        self.port = "TEST"

    def test_3(self):
        self.port = "TEST"
        self.device = "GMH"

    def test_4(self):
        self.port = "TEST"
        self.device = "GMH 3710"
        self.command = None

    def test_5(self):
        self.port = "TEST"
        self.device = "GMH 3710"
        self.command = 12

    def test_6(self):
        self.list = True

    def test_7(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = ""
        self.verbose = 0

    def test_8(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 0
        self.read = True


# noinspection DuplicatedCode
class TestConsole(unittest.TestCase):
    """Testing class for message coding and decoding module."""

    def setUp(self):
        """set up test.
        """
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_constructor(self):
        """tear down test.
        """
        console = Console()

        self.assertIsNone(console.device)
        self.assertIsNone(console.options)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_1(self):
        options = TestOptions()
        options.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertTrue(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_2(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (None, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_3(self):
        """tear down test.
        """
        options = TestOptions()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_4(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_2()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_5(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_3()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_6(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_4()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_7(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_5()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_8(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_6()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertTrue(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_9(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_7()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial.open', new=mock.Mock(side_effect=SerialException('Attempting to use a port that is not open')))
    def test_prepare_10(self):
        options = TestOptions()
        options.test_1()

        # mock_serial_2.open = mock.Mock(side_effect=SerialException('Attempting to use a port that is not open'))

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertFalse(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_11(self):
        options = TestOptions()
        options.test_8()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertTrue(check)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_run_1(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check1 = console.prepare()
        check2 = console.run()

        self.assertTrue(check1)
        self.assertTrue(check2)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_run_2(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_6()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check1 = console.prepare()
        check2 = console.run()

        self.assertTrue(check1)
        self.assertTrue(check2)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_close_1(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check1 = console.prepare()
        check2 = console.run()
        check3 = console.close()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertTrue(check3)
        return
