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
    "MessageLength"
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
