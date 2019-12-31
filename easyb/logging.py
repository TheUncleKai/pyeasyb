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

import colorama
import sys
import traceback


def _create_scheme(style="", fore="", back=""):
    scheme = ""

    text_style = None
    text_fore = None
    text_back = None

    if style != "":
        text_style = getattr(colorama.Style, style)

    if fore != "":
        text_fore = getattr(colorama.Fore, fore)

    if back != "":
        text_back = getattr(colorama.Back, back)

    if text_style is not None:
        scheme += text_style

    if text_fore is not None:
        scheme += text_fore

    if text_back is not None:
        scheme += text_back
    return scheme


def _write_stdout(content, raw=False):
    sys.stdout.write(content)
    if raw is True:
        return
    sys.stdout.write("\n")
    return


def _write_stderr(content, raw=False):
    sys.stderr.write(content)
    if raw is True:
        return
    sys.stderr.write("\n")
    return


class Log(object):

    reset = colorama.Style.RESET_ALL
    label_num = 15
    seperator = "| "
    level = 0

    def __init__(self):
        colorama.init()
        return

    @staticmethod
    def raw(content: str):
        _write_stdout(content)
        return

    def inform(self, tag, text):

        scheme = _create_scheme("BRIGHT", "GREEN")

        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stdout(content)
        return

    def debug1(self, tag, text):

        if self.level < 1:
            return

        scheme = _create_scheme("BRIGHT", "GREEN")
        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stdout(content)
        return

    def debug2(self, tag, text):

        if self.level < 2:
            return

        scheme = _create_scheme("BRIGHT", "GREEN")
        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stdout(content)
        return

    def debug3(self, tag, text):

        if self.level < 3:
            return

        scheme = _create_scheme("BRIGHT", "GREEN")

        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stdout(content)
        return

    def warn(self, tag, text):

        scheme = _create_scheme("BRIGHT", "MAGENTA")

        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stdout(content)
        return

    def error(self, text):

        scheme = _create_scheme("BRIGHT", "RED")
        tag = "ERROR"

        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stderr(content)
        return

    def log_traceback(self):
        ttype, value, tb = sys.exc_info()
        self.error("Uncaught exception")
        self.error("Type:      " + str(ttype))
        self.error("Value:     " + str(value))

        lines = traceback.format_tb(tb)
        for line in lines:
            _write_stderr(line, True)
        return

    def exception(self, e):

        scheme = _create_scheme("BRIGHT", "RED")
        tag = "EXCEPTION"
        text = str(e)

        content = self.reset + scheme + " " + tag.ljust(self.label_num) + self.seperator + self.reset + text
        _write_stderr(content)
        return
