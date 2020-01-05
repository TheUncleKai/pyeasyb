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

from typing import List, Any

from enum import Enum
from abc import ABCMeta

__all__ = [
    "Type",
    "Column",
    "Info",
    "Row",
    "Collection",
    "Storage"
]


class Type(Enum):

    datetime = 0
    integer = 1
    float = 2
    string = 3
    bool = 4


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


class Info(object):

    name: str = ""
    type: Type = None
    value: Any = None

    def __init__(self, name: str, type: Type, value: Any):
        self.name = name
        self.type = type
        self.value = value
        return


class Row(object):

    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        return


class Collection(object):

    rows: List[Row] = []
    columns: List[Column] = []
    infos: List[Info] = []
    status: List[Info] = []
    filename: str = ""


class Storage(metaclass=ABCMeta):

    name: str = ""
    data: Collection = None

    def __init__(self, name: str, data: Collection):
        self.name = name
        self.data = data
        return

    @abc.abstractmethod
    def store(self) -> bool:
        return True
