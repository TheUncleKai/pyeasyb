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
import os

from datetime import datetime

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

    def test_get_column_01(self):
        item = Data()

        check1 = item.add_column("datetime", "Datetime", Type.datetime)

        column = item.get_column("datetime")

        self.assertTrue(check1)
        self.assertIsNotNone(column)
        self.assertEqual(column.name, "datetime")
        self.assertEqual(column.description, "Datetime")
        self.assertEqual(column.type, Type.datetime)
        self.assertEqual(column.index, 0)
        return

    def test_get_column_02(self):
        item = Data()

        self.assertRaises(ValueError, item.get_column, "datetime")
        return

    # noinspection PyUnresolvedReferences
    def test_create_row(self):
        item = Data()

        item.add_column("datetime", "Datetime", Type.datetime)
        item.add_column("checked", "Is checked", Type.bool)
        item.add_column("temp", "Temperature", Type.float)
        item.add_column("counter", "Counter", Type.integer)
        item.add_column("note", "Note", Type.string)

        _now = datetime.now()
        row = item.create_row()

        row.datetime = _now
        row.checked = False
        row.temp = 0.1
        row.counter = 2
        row.note = "Jo"

        self.assertEqual(item.len, 1)
        self.assertEqual(item.rows[0].datetime, _now)
        self.assertEqual(item.rows[0].checked, False)
        self.assertEqual(item.rows[0].temp, 0.1)
        self.assertEqual(item.rows[0].counter, 2)
        self.assertEqual(item.rows[0].note, "Jo")
        return

    def test_store_01(self):
        item = Data()

        item.add_column("datetime", "Datetime", Type.datetime)
        item.add_column("checked", "Is checked", Type.bool)
        item.add_column("temp", "Temperature", Type.float)
        item.add_column("counter", "Counter", Type.integer)
        item.add_column("note", "Note", Type.string)

        _now = datetime.now()
        row = item.create_row()

        row.datetime = _now
        row.checked = False
        row.temp = 0.1
        row.counter = 2
        row.note = "Jo"

        item.store("excel", "Test")

        check1 = os.path.exists("Test.xlsx")
        self.assertTrue(check1)
        os.remove("Test.xlsx")
        return

    def test_store_02(self):
        item = Data()

        self.assertRaises(ValueError, item.store, "excel", "")
        return

    def test_store_03(self):
        item = Data()

        check = item.store("unknown", "Test")
        self.assertFalse(check)
        return
