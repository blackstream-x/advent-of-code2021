# -*- coding: utf-8 -*-

"""
Advent of code 2021 helpers
for blackstream-x’ solutions
"""


import sys
import time


#
# Classes
#


class Reader:

    """Read an open text file (by preference: stdin)
    and provide generator methods yielding lines or line parts
    """

    def __init__(self, text_file=sys.stdin):
        """Read the file and keep its contents"""
        self.file_contents = text_file.read()

    def lines(self, rstrip=True, skip_empty=True):
        """Yield lines from the contents"""
        for line in self.file_contents.splitlines(keepends=True):
            if rstrip:
                line = line.rstrip()
            #
            if line or not skip_empty:
                yield line
            #
        #

    def splitted_lines(self, by_=None, rstrip=True, skip_empty=True):
        """Yield lines splitted"""
        for line in self.lines(rstrip=rstrip, skip_empty=skip_empty):
            yield line.split(by_)
        #


#
# Functions
#


def timer(func):
    """Decorator to get execution time,
    shamelessly ripped off aocutils.py from
    <https://github.com/DeXtroTip/advent-of-code-2021>
    """

    def wrapper(*args, **kwargs):
        start = time.time() * 1000
        func_output = func(*args, **kwargs)
        print(f'Executed in {time.time() * 1000 - start:.3f} msec:')
        return func_output

    return wrapper


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
