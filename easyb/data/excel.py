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

import os
import easyb
from typing import List

from easyb.data.base import Storage, Column, Row
import xlsxwriter

__all__ = [
    "ExportExcel"
]

storage = "EXCEL"
classname = "ExportExcel"


class ExportExcel(Storage):

    workbook: xlsxwriter.Workbook = None
    info: xlsxwriter.workbook.Worksheet = None
    data: xlsxwriter.workbook.Worksheet = None
    row: int = 0

    def __init__(self, columns: List[Column], rows: List[Row], filename: str):
        Storage.__init__(self, "EXCEL", columns, rows, filename)
        return

    def _prepare(self):

        self.filename = os.path.abspath(os.path.normpath(self.filename + ".xlsx"))
        easyb.log.inform(self.name, "Open {0:s}".format(self.filename))
        self.workbook = xlsxwriter.Workbook(self.filename, {'constant_memory': True})
        self.info = self.workbook.add_worksheet("Information")
        self.data = self.workbook.add_worksheet("Data")
        return

    def _create_header(self):
        cell_format = self.workbook.add_format()
        cell_format.set_bottom(5)
        cell_format.set_font_name("Arial")
        cell_format.set_font_size(10)
        cell_format.set_bold()

        for column in self.columns:
            self.data.write_string(self.row, column.index, column.description, cell_format)
        self.row += 1
        return

    def _close(self):
        if self.workbook is None:
            return
        self.workbook.close()
        return

    def store(self) -> bool:
        self._prepare()
        self._create_header()
        self._close()
        return True
