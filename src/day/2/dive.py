#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Advent of code 2021, day 2:
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


def get_input_instructions():
    """Generator function: yield direction and units to move,
    line per line
    """
    input_data = sys.stdin.read()
    for line in input_data.splitlines():
        line = line.strip()
        if not line:
            continue
        #
        direction, units_text = line.split(None, 1)
        try:
            yield (direction, int(units_text))
        except ValueError as error:
            logging.warning(
                "Failed to convert unit %r into a number: %s",
                units_text,
                error,
            )
        #
    #


def navigate(instructions, horizontal_position=0, depth=0):
    """Navigate using instructions from stdin.
    Return a tuple (horizontal_position, depth)
    """
    for (direction, units) in instructions:
        if direction == "forward":
            horizontal_position += units
        elif direction == "down":
            depth += units
        elif direction == "up":
            depth -= units
        else:
            logging.error("Unsupported direction %r!", direction)
        #
    #
    return(horizontal_position, depth)


def navigate_with_aim(instructions, horizontal_position=0, depth=0, aim=0):
    """Navigate using instructions from stdin.
    Return a tuple (horizontal_position, depth)
    """
    for (direction, units) in instructions:
        if direction == "forward":
            horizontal_position += units
            depth += aim * units
        elif direction == "down":
            aim += units
        elif direction == "up":
            aim -= units
        else:
            logging.error("Unsupported direction %r!", direction)
        #
    #
    return(horizontal_position, depth)


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
    instructions = list(get_input_instructions())
    horizontal_position, depth = navigate(instructions)
    logging.info("Horizontal position: %s", horizontal_position)
    logging.info("Depth: %s", depth)
    logging.info("Part 1 solution: %s", horizontal_position * depth)
    horizontal_position, depth = navigate_with_aim(instructions)
    logging.info("Horizontal position: %s", horizontal_position)
    logging.info("Depth: %s", depth)
    logging.info("Part 2 solution: %s", horizontal_position * depth)
    return RETURNCODE_OK


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
