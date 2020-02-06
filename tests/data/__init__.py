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

from easyb.logging import SerialLogging
from easyb.data import Data
from easyb.data.base import Type

__all__ = [
    "TestData"
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


# noinspection DuplicatedCode
class TestData(unittest.TestCase):

    def setUp(self):
        easyb.set_logging(new_logging)
        return

    def tearDown(self):
        easyb.set_logging(old_logging)
        return

    def test_constructor(self):
        item = Data()

        self.assertEqual(item.filename, "")
        self.assertEqual(item.counter, 0)
        self.assertEqual(len(item.rows), 0)
        self.assertEqual(len(item.columns), 0)
        self.assertEqual(len(item.infos), 0)
        self.assertEqual(len(item.status), 0)
        return

    def test_add_column_01(self):
        item = Data()

        check = item.add_column("datetime", "Datetime", Type.datetime)

        self.assertTrue(check)
        self.assertEqual(item.counter, 1)
        self.assertEqual(len(item.columns), 1)
        return

    def test_add_column_02(self):
        item = Data()

        check1 = item.add_column("datetime", "Datetime", Type.datetime)
        check2 = item.add_column("datetime", "Datetime2", Type.datetime)

        self.assertTrue(check1)
        self.assertFalse(check2)
        self.assertEqual(item.counter, 1)
        self.assertEqual(len(item.columns), 1)
        return
