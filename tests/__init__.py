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

from typing import List

from easyb.command import Command
from easyb.device import Device
from easyb.message import Message

__all__ = [
    "bit",
    "console",
    "device",
    "gmh3710",
    "message",
    "stream",

    "TestDevice",
    "TestException",
    "TestSerial"
]


class TestDevice(Device):

    def __init__(self, **kwargs):
        Device.__init__(self, name="TEST-DEVICE", wait_time=0.1, address=1, **kwargs)

        # noinspection PyTypeChecker
        self.message: Message = None
        return

    def init_commands(self):

        command = Command(name="Messwert lesen", code=0, func_call=self.read_messwert)
        self.commands.append(command)
        return

    def read_messwert(self, message: Message) -> bool:
        self.message = message
        return True

    def prepare(self):
        return

    def run(self):
        return

    def close(self):
        return


class TestException(object):

    def __init__(self, number: int, exception: Exception):
        self.run: int = number

        # noinspection PyTypeChecker
        self.exception: Exception = exception
        return


class TestSerial(object):

    def __init__(self):
        self.read_run: int = 0
        self.read_data: List[List[int]] = []

        self.write_run: int = 0
        self.write_data: List[List[int]] = []

        # noinspection PyTypeChecker
        self.read_exception: TestException = None

        # noinspection PyTypeChecker
        self.write_exception: TestException = None
        return

    def write(self, data: bytes):
        if self.read_exception is not None:
            if self.read_exception.run == self.read_run:
                raise self.read_exception.exception

        run_list = []
        for item in data:
            run_list.append(int(item))
        self.write_data.append(run_list)
        self.read_run += 1
        return

    # noinspection PyUnusedLocal
    def read(self, count: int = 0) -> bytes:
        if self.read_exception is not None:
            if self.read_exception.run == self.write_run:
                raise self.read_exception.exception

        data = self.read_data[self.write_run]
        result = bytes(data)
        self.write_run += 1
        return result
