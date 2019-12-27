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

from enum import Enum

__all__ = [
    "MessageDirection",
    "MessagePriority",
    "MessageLength",
    "ErrorCodes"
]


class MessageDirection(Enum):

    FromSlave = 1
    FromMaster = 0


class MessagePriority(Enum):

    Priority = 1
    NoPriority = 0


class MessageLength(Enum):

    Byte3 = 0
    Byte6 = 1
    Byte9 = 2
    Variable = 3


class ErrorCodes(Enum):

    error_16352 = {"code": 16352, "text": "Value over measurement range"}

    error_16353 = {"code": 16353, "text": "Value under measurement range"}

    error_16362 = {"code": 16362, "text": "Calculation impossible"}

    error_16363 = {"code": 16363, "text": "System error"}

    error_16364 = {"code": 16364, "text": "Battery empty"}

    error_16365 = {"code": 16365, "text": "No sensor"}

    error_16366 = {"code": 16366, "text": "Recording error: EEPROM error"}

    error_16367 = {"code": 16367, "text": "EEPROM checksum invalid"}

    error_16368 = {"code": 16368, "text": "Recording error: error 6, system restart"}

    error_16369 = {"code": 16369, "text": "Recording error: data pointer"}

    error_16370 = {"code": 16370, "text": "Recording error: marker data invalid"}

    error_16371 = {"code": 16370, "text": "Data invalid"}

    error_unknown = {"code": 0, "text": "Unknown error"}


class StatusCodes(Enum):

    bit_0 = {"bit": 0x0001, "text": "Max. alarm"}

    bit_1 = {"bit": 0x0002, "text": "Max. alarm"}

    bit_2 = {"bit": 0x0004, "text": "Max. alarm"}

    bit_3 = {"bit": 0x0008, "text": "Max. alarm"}

    bit_4 = {"bit": 0x0010, "text": "Max. alarm"}

    bit_5 = {"bit": 0x0020, "text": "Max. alarm"}

    bit_6 = {"bit": 0x0040, "text": "Max. alarm"}

    bit_7 = {"bit": 0x0080, "text": "Max. alarm"}

    bit_8 = {"bit": 0x0100, "text": "Max. alarm"}

    bit_9 = {"bit": 0x0200, "text": "Max. alarm"}

    bit_10 = {"bit": 0x0400, "text": "Max. alarm"}

    bit_11 = {"bit": 0x0800, "text": "Max. alarm"}

    bit_12 = {"bit": 0x1000, "text": "Max. alarm"}

    bit_13 = {"bit": 0x2000, "text": "Max. alarm"}

    bit_14 = {"bit": 0x4000, "text": "Max. alarm"}

    bit_15 = {"bit": 0x8000, "text": "Max. alarm"}
