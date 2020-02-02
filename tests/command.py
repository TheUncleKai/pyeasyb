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

from easyb.command import Command
from easyb.definitions import Length


# noinspection DuplicatedCode
class TestCommand(unittest.TestCase):

    def setUp(self):
        self._message = ""
        return

    def tearDown(self):
        self._message = ""
        return

    def messwert_lesen(self, message: str):
        self._message = message
        return

    def test_command_01(self):
        command = Command(name="Messwert lesen", number=0, address=0, code=255, length=Length.Byte9,
                          func_call=self.messwert_lesen)

        command.call("TEST")

        self.assertEqual(command.name, "Messwert lesen")
        self.assertEqual(command.number, 0)
        self.assertEqual(command.address, 0)
        self.assertEqual(command.code, 255)
        self.assertEqual(command.length, Length.Byte9)
        self.assertEqual(self._message, "TEST")
        return
