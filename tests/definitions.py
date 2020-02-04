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



# noinspection DuplicatedCode
class TestDefinitions(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_direction(self):
        item1 = easyb.definitions.get_direction(1)
        item2 = easyb.definitions.get_direction(0)
        item3 = easyb.definitions.get_direction(3)

        self.assertEqual(item1, easyb.definitions.Direction.FromSlave)
        self.assertEqual(item2, easyb.definitions.Direction.FromMaster)
        self.assertIsNone(item3)
        return

    def test_priority(self):
        item1 = easyb.definitions.get_priority(1)
        item2 = easyb.definitions.get_priority(0)
        item3 = easyb.definitions.get_priority(2)

        self.assertEqual(item1, easyb.definitions.Priority.Priority)
        self.assertEqual(item2, easyb.definitions.Priority.NoPriority)
        self.assertIsNone(item3)
        return

    def test_length(self):
        item1 = easyb.definitions.get_length(0)
        item2 = easyb.definitions.get_length(1)
        item3 = easyb.definitions.get_length(2)
        item4 = easyb.definitions.get_length(3)
        item5 = easyb.definitions.get_length(4)

        self.assertEqual(item1, easyb.definitions.Length.Byte3)
        self.assertEqual(item2, easyb.definitions.Length.Byte6)
        self.assertEqual(item3, easyb.definitions.Length.Byte9)
        self.assertEqual(item4, easyb.definitions.Length.Variable)
        self.assertIsNone(item5)
        return

    def test_error(self):
        config1 = {
            "code": 16352,
            "text": "Value over measurement range"
        }

        config2 = {
            "text": "Value over measurement range"
        }

        error1 = easyb.definitions.Error(config1)
        self.assertRaises(ValueError, easyb.definitions.Error, config2)

        self.assertEqual(error1.text, "Value over measurement range")
        self.assertEqual(error1.code, 16352)
        return

    def test_status(self):
        config1 = {
            "bit": 0x0001,
            "text": "Max. alarm"
        }

        config2 = {
            "text": "Max. alarm"
        }

        error1 = easyb.definitions.Status(config1)
        self.assertRaises(ValueError, easyb.definitions.Status, config2)

        self.assertEqual(error1.text, "Max. alarm")
        self.assertEqual(error1.bit, 0x0001)
        return

    def test_unit(self):
        config1 = {
            "code": 1,
            "value": "°C"
        }

        config2 = {
            "value": "°C"
        }

        error1 = easyb.definitions.Unit(config1)
        self.assertRaises(ValueError, easyb.definitions.Unit, config2)

        self.assertEqual(error1.code, 1)
        self.assertEqual(error1.value, "°C")
        return
