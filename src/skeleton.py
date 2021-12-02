#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Advent of code 2021, day x:
Rainer’s solution

"""


import argparse
import logging
import sys


#
# Constants
#


RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


#
# Functions
#


#
# Main
#


def main():
    """Parse arguments and execute the required function(s)"""
    main_parser = argparse.ArgumentParser(
        prog="file_manager_integration",
        description="Integrate a script in file managers",
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
    arguments = main_parser.parse_args()
    logging.basicConfig(
        level=arguments.loglevel,
        format="%(levelname)-8s | %(message)s",
    )


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
