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


class TestOptions(object):

    device = ""
    command = 0
    port = ""
    verbose = 0

    def test_1(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 0


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
        self.assertIsNone(console.command)
        self.assertEqual(console.port, "")
        return

    def test_prepare_1(self):
        """tear down test.
        """
        options = TestOptions()
        options.test_1()

        console = Console()
        console._parser = mock.Mock()
        console._parser.parse_args = mock.Mock()
        console._parser.parse_args.return_value = (options, None)

        check = console.prepare()

        self.assertTrue(check)
        return

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
