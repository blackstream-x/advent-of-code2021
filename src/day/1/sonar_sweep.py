#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Advent of code 2021, day 1:
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


def get_input_numbers():
    """Generator function: yield numerical input data, line per line"""
    input_data = sys.stdin.read()
    for line in input_data.splitlines():
        line = line.strip()
        if not line:
            continue
        #
        try:
            yield int(line)
        except ValueError as error:
            logging.warning(
                "Failed to convert line %r into a number: %s",
                line,
                error,
            )
        #
    #


def get_times_increased(input_numbers):
    """Determine how many times the depth has increased"""
    times_increased = 0
    for current_index, current_value in enumerate(input_numbers):
        try:
            if input_numbers[current_index + 1] > current_value:
                times_increased += 1
            #
        except IndexError:
            break
        #
    #
    return times_increased


def get_moving_window_increased(input_numbers, size):
    """Determine how many times a moving window of size size
    has increased
    """
    moving_window_sizes = []
    for current_index in range(len(input_numbers)):
        current_window = input_numbers[current_index:current_index + size]
        if len(current_window) < size:
            break
        #
        current_window_size = sum(current_window)
        logging.debug(
            "Moving window starting at %s: %r, sum: %s",
            current_index,
            current_window,
            current_window_size,
        )
        moving_window_sizes.append(current_window_size)
    #
    return get_times_increased(moving_window_sizes)


#
# Main
#


def main():
    """Parse arguments and execute the required function(s)"""
    main_parser = argparse.ArgumentParser(
        description="Advent of Code day 1: sonar sweep",
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
    input_numbers = list(get_input_numbers())
    logging.info(
        "Depth increased %s times",
        get_times_increased(input_numbers),
    )
    moving_window_size = 3
    logging.info(
        "Moving window of size %s increased %s times",
        moving_window_size,
        get_moving_window_increased(input_numbers, moving_window_size),
    )
    return RETURNCODE_OK


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
