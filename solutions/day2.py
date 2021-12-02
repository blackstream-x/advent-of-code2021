#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Advent of code 2021, day 2
blackstream-x’ solution
(simplified version of src/day/2/dive.py using the helpers module)
"""


import helpers


READER = helpers.Reader()


def get_command():
    for fields in READER.splitted_lines():
        yield (fields[0], int(fields[1]))
    #


@helpers.timer
def part1():
    horizontal = depth = 0
    for (direction, units) in get_command():
        if direction == "forward":
            horizontal += units
        elif direction == "down":
            depth += units
        elif direction == "up":
            depth -= units
        else:
            print(f"Unsupported direction {direction}")
        #
    #
    return horizontal * depth


@helpers.timer
def part2():
    horizontal = depth = aim = 0
    for (direction, units) in get_command():
        if direction == "forward":
            horizontal += units
            depth += aim * units
        elif direction == "down":
            aim += units
        elif direction == "up":
            aim -= units
        else:
            print(f"Unsupported direction {direction}")
        #
    #
    return horizontal * depth


if __name__ == "__main__":
    print(part1())
    print(part2())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
