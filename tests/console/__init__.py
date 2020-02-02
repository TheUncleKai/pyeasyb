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

import easyb
from easyb.logging import SerialLogging

from tests.console.options import TestOptions

__all__ = [
    "options",
    "serial",

    "TestConsole"
]

from tests.console.serial import TestserialPrepare11, TestserialRun1, TestserialClose1

mock_serial = mock.Mock()
mock_serial_2 = mock.Mock()

old_logging = easyb.log
new_logging = SerialLogging()
new_logging.setup(app="Device", level=2)
cons = new_logging.get_writer("console")
cons.index.append("SERIAL")

# noinspection PyUnresolvedReferences
cons.add_style("SERIAL", "BRIGHT", "YELLOW", "")
cons.setup(text_space=15, error_index=["ERROR", "EXCEPTION"])
new_logging.register(cons)
new_logging.open()


# noinspection DuplicatedCode
class TestConsole(unittest.TestCase):

    def setUp(self):
        easyb.set_logging(new_logging)
        return

    def tearDown(self):
        easyb.set_logging(old_logging)
        return

    def test_constructor(self):
        console = Console()

        self.assertIsNone(console.device)
        self.assertIsNone(console.options)
        return

    @mock.patch('easyb.device.Serial', new=mock_serial)
    def test_prepare_1(self):
        option = TestOptions()
        option.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (option, None)

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

    @mock.patch('easyb.device.Serial', new=TestserialPrepare11)
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

    @mock.patch('easyb.device.Serial', new=TestserialRun1)
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

    @mock.patch('easyb.device.Serial', new=TestserialClose1)
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
