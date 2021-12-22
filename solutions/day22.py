#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 22
blackstream-x’ solution
"""


import itertools
import logging

import helpers


OPERATIONS = dict(on=set.update, off=set.difference_update)

PART_1_LIMITS = dict(x=(-50, 50), y=(-50, 50), z=(-50, 50))


def cuboid(coordinates, limits=None):
    """Return an iterator over all coordinates in the cuboid"""
    limits = limits or {}
    # Evaluate coordinates
    value_ranges = {}
    for dimension in coordinates.split(","):
        axis, values = dimension.split("=", 1)
        min_limit, max_limit = limits.get(axis, (None, None))
        minimum, maximum = [int(item) for item in values.split("..")]
        if min_limit is not None and minimum < min_limit:
            minimum = min_limit
        #
        if max_limit is not None and maximum > max_limit:
            maximum = max_limit
        #
        value_ranges[axis] = range(minimum, maximum + 1)
    #
    return itertools.product(*[value_ranges[axis] for axis in "xyz"])


@helpers.timer
def part1(reader):
    """Part 1"""
    reactor = set()
    for line in reader.lines():
        instruction, coordinates = line.split(None, 1)
        logging.debug("%s => %s cubes", coordinates, len(list(cuboid(coordinates, limits=PART_1_LIMITS))))
        OPERATIONS[instruction](reactor, cuboid(coordinates, limits=PART_1_LIMITS))
    #
    return len(reactor)


@helpers.timer
def part2(reader):
    """Part 2"""
    # TODO: cube addition and subtraction algorithm
    result = None
    for line in reader.lines():
        ...
    #
    return result


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
