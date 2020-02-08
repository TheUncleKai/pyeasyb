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
from easyb.data.base import Type, Info
from easyb.data.text import TextStorage

__all__ = [
    "TestText"
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
class TestText(unittest.TestCase):

    def setUp(self):
        easyb.set_logging(new_logging)
        return

    def tearDown(self):
        easyb.set_logging(old_logging)
        return

    @staticmethod
    def _get_data() -> Data:
        item = Data()
        item.filename = "TEST"

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
        return item

    def test_constructor(self):
        data = self._get_data()

        item = TextStorage(data)
        self.assertEqual(item.name, "TEXT")
        self.assertIsNone(item.file)
        return

    def test_store(self):
        data = self._get_data()

        item = TextStorage(data)

        status = []

        easyb.conf.create_status(status)

        status[0].is_set = True

        data.infos.append(Info("Test1", Type.integer, 1))
        data.infos.append(Info("Test2", Type.float, 0.1))
        data.infos.append(Info("Test3", Type.bool, False))

        for _state in status:
            info = Info(_state.text, Type.bool, _state.is_set)
            data.status.append(info)

        check = item.store()
        self.assertTrue(check)

        check1 = os.path.exists("TEST.csv")
        self.assertTrue(check1)
        os.remove("TEST.csv")
        return
