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

import time

from typing import List
from datetime import datetime

from easyb.command import Command
from easyb.device import Device


class Data:

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def value(self) -> float:
        return self._value

    def __init__(self, value: float):
        self._datetime = datetime.now()
        self._value = value
        return


class GMH3710(Device):

    @property
    def data(self) -> List[Data]:
        return self._data

    @property
    def system_state(self) -> int:
        return self._system_state

    @property
    def min_value(self) -> float:
        return self._min_value

    @property
    def max_value(self) -> float:
        return self._max_value

    @property
    def id_number(self) -> int:
        return self._id_number

    def __init__(self, **kwargs):
        self._address = 1
        self._data = []

        self._system_state = 0
        self._min_value = 0.0
        self._max_value = 0.0

        self._id_number = 0

        item = kwargs.get("address", 1)
        if item is not None:
            self._address = item

        Device.__init__(self, "GMH 3710", 0.1)
        return

    def read_measurement(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        self.data.append(Data(message.value))
        return True

    def read_system_state(self) -> bool:
        command = self.get_command(1)

        message = self.execute(command)
        if message is None:
            return False

        self._system_state = int(message.value)
        return True

    def read_min_value(self) -> bool:
        command = self.get_command(2)

        message = self.execute(command)
        if message is None:
            return False

        self._min_value = int(message.value)
        return True

    def read_max_value(self) -> bool:
        command = self.get_command(3)

        message = self.execute(command)
        if message is None:
            return False

        self._max_value = int(message.value)
        return True

    def read_id_number(self) -> bool:
        command = self.get_command(4)

        message = self.execute(command)
        if message is None:
            return False

        self._max_value = int(message.value)
        return True

    def init_commands(self):

        command = Command(name="Messwert lesen", number=0, address=self._address, code=0,
                          func_call=self.read_measurement)
        self.commands.append(command)

        command = Command(name="Systemstatus lesen", number=1, address=self._address, code=3,
                          func_call=self.read_system_state)
        self.commands.append(command)

        command = Command(name="Minwert lesen", number=2, address=self._address, code=6, func_call=self.read_min_value)
        self.commands.append(command)

        command = Command(name="Maxwert lesen", number=3, address=self._address, code=7, func_call=self.read_max_value)
        self.commands.append(command)

        command = Command(name="ID-Nummer lesen", number=4, address=self._address, code=12,
                          func_call=self.read_id_number)
        self.commands.append(command)
        return
