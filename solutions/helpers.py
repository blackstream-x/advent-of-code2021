# -*- coding: utf-8 -*-

"""
Advent of code 2021 helpers
for blackstream-x’ solutions
"""


import argparse
import collections
import logging
import sys
import time


#
# Classes
#


Position = collections.namedtuple("Position", ("x", "y"))


class Reader:

    """Read an open text file (by preference: stdin)
    and provide generator methods yielding lines or line parts
    """

    def __init__(self, file_name=None, text=None):
        """Read the file and keep its contents"""
        if text:
            self.file_contents = text
        elif file_name:
            with open(file_name, mode="rt", encoding="utf-8") as input_file:
                self.file_contents = input_file.read()
            #
        else:
            self.file_contents = sys.stdin.read()
        #

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


class TestMixin:

    """Mixin for unit tests preventing code duplication"""

    def do_equality_test(self, index):
        """Test for equality"""
        if self.results[index] is None:
            self.skipTest("No expected result provided")
        #
        self.assertEqual(
            self.results[index], self.tested_functions[index](self.reader)
        )


#
# Functions
#


def initialize_puzzle():
    """Initialize a puzze: initialize logging,
    and return a Reader object
    """
    main_parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Advent of Code puzzle solver",
    )
    main_parser.set_defaults(loglevel=logging.INFO)
    main_parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.DEBUG,
        dest="loglevel",
        help="output all messages including debug level",
    )
    main_parser.add_argument(
        "input_file_name",
        nargs="?",
        help="read data from a file (default: read from stdin)",
    )
    arguments = main_parser.parse_args()
    logging.basicConfig(
        level=arguments.loglevel,
        format="%(levelname)-8s | %(message)s",
    )
    return Reader(arguments.input_file_name)


def timer(func):
    """Decorator to get execution time,
    shamelessly ripped off aocutils.py from
    <https://github.com/DeXtroTip/advent-of-code-2021>
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        func_output = func(*args, **kwargs)
        end = time.time()
        msec = 1000 * (end - start)
        logging.info(
            "Executed %r in %.3f msec (%.1f µsec)",
            func.__doc__,
            msec,
            1000 * msec,
        )
        return func_output

    return wrapper


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
