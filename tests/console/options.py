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

__all__ = [
    "TestOptions"
]


class TestOptions(object):

    def __init__(self):
        self.verbose = 2
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
        self.verbose = 2
        return

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
        self.command = 22

    def test_6(self):
        self.list = True

    def test_7(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = ""
        self.verbose = 2

    def test_8(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 2
        self.read = True

    def test_9(self):
        self.list = True
        self.command = 0
        self.port = ""
        self.verbose = 2
        self.read = False

    def test_10(self):
        self.device = "GMH 3710"
        self.list = True
        self.command = 0
        self.port = ""
        self.verbose = 2
        self.read = False

    def test_11(self):
        self.device = "GMH 3720"
        self.list = True
        self.command = 0
        self.port = ""
        self.verbose = 2
        self.read = False

    def test_12(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 2
        self.read = True

    def test_13(self):
        self.device = "GMH 3710"
        self.output = "excel"
        self.filename = "TEST"
        self.command = 0
        self.port = "TEST"
        self.verbose = 2
        self.read = True
