#!/usr/bin/python3
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

import abc

from typing import List

from enum import Enum
from abc import ABCMeta

__all__ = [
    "Type",
    "Column",
    "Row"
]


class Type(Enum):

    datetime = 0
    integer = 1
    float = 2
    string = 3


class Column(object):

    index: int = 0
    name: str = ""
    description: str = ""
    type: Type = None

    def __init__(self, index: int, name: str, desc: str, column_type: Type):
        self.index = index
        self.name = name
        self.description = desc
        self.type = column_type
        return


class Row(object):

    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        return


class Storage(metaclass=ABCMeta):

    columns: List[Column] = None
    rows: List[Row] = None
    filename: str = ""

    def __init__(self, columns: List[Column], rows: List[Row], filename: str):
        self.columns = columns
        self.rows = rows
        self.filename = filename
        return

    @abc.abstractmethod
    def store(self) -> bool:
        return True
