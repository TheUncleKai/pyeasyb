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
from tests import TestSerial


class TestserialPrepare11(TestSerial):

    def __init__(self, **kwargs):
        TestSerial.__init__(self)
        self.read_data = [
            [0xfe, 0x33, 0xa4],
            [0xff, 0x00, 0x28],
            [0xfe, 0xc5, 0x68],
            [0xcd, 0x40, 0x3c, 0x8f, 0x08, 0xb2],
            [0xfe, 0xf5, 0xf8],
            [0x35, 0x00, 0x47, 0xff, 0x01, 0x2f]
        ]
        return


class TestserialRun1(TestSerial):

    def __init__(self, **kwargs):
        TestSerial.__init__(self)
        self.read_data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf9, 0x9e, 0x85]
        ]
        return


class TestserialClose1(TestSerial):

    def __init__(self, **kwargs):
        TestSerial.__init__(self)
        self.read_data = [
            [0xfe, 0x05, 0x26],
            [0x71, 0x00, 0x48, 0xf9, 0x9e, 0x85]
        ]
        return
