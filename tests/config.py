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

from easyb.config import Config
from easyb.definitions import Length


# noinspection DuplicatedCode
class TestConfig(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_config_01(self):
        config = Config()

        error1 = config.get_error(16365)
        error2 = config.get_error(1)

        unit1 = config.get_unit(1)
        unit2 = config.get_unit(0)

        self.assertIsNotNone(error1)
        self.assertIsNone(error2)

        self.assertIsNotNone(unit1)
        self.assertIsNone(unit2)

        self.assertEqual(error1.code, 16365)
        self.assertEqual(error1.text, "No sensor")

        self.assertEqual(unit1.value, "°C")
        return

    def test_config_02(self):
        config = Config()
        status_list = []

        config.create_status(status_list)

        self.assertEqual(len(status_list), 16)
        self.assertEqual(status_list[0].bit, 0x0001)
        self.assertEqual(status_list[0].text, "Max. alarm")
        return
