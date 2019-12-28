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

from typing import Union
from enum import Enum

__all__ = [
    "MessageDirection",
    "get_direction",

    "MessagePriority",
    "get_priority",

    "MessageLength",
    "get_length"
]


class MessageDirection(Enum):

    FromSlave = 1
    FromMaster = 0


def get_direction(value: int) -> Union[None, MessageDirection]:
    for item in MessageDirection:
        if item.value == value:
            return item
    return None


class MessagePriority(Enum):

    Priority = 1
    NoPriority = 0


def get_priority(value: int) -> Union[None, MessagePriority]:
    for item in MessagePriority:
        if item.value == value:
            return item
    return None


class MessageLength(Enum):

    Byte3 = 0
    Byte6 = 1
    Byte9 = 2
    Variable = 3


def get_length(value: int) -> Union[None, MessageLength]:
    for item in MessageLength:
        if item.value == value:
            return item
    return None
