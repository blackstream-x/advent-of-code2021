#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 15

I failed to manage it myself this time;
this solution is ripped off from
<https://github.com/macobo/aoc-2021/blob/master/day15.py>
"""


import logging

import helpers


class ChitonDensityMap:

    """Map of Chiton density"""

    start_point = (0, 0)

    def __init__(self):
        """Initialize grid"""
        self.__map = {}
        self.lines = 0
        self.columns = 0

    def add_line(self, line):
        """Add a line to the map"""
        for (index, density) in enumerate(line):
            self.__map[(index, self.lines)] = int(density)
        #
        self.columns = max(self.columns, index + 1)
        self.lines += 1

    def neighbors(self, position):
        """Yield all horizontal and vertical
        neighbor positions
        """
        x_pos, y_pos = position
        for index in (0, 1):
            pos_list = list(position)
            for relative_location in (-1, 1):
                pos_list[index] = pos_list[index] + relative_location
                neighbor_position = tuple(pos_list)
                if neighbor_position in self.__map:
                    yield neighbor_position
                #
            #
        #

    def get_minimum_path_cost(self):
        """Return minimum path cost"""
        # TODO: use heapq to get the minimum path cost
        ...


@helpers.timer
def part1(reader):
    """Part 1"""
    density_map = ChitonDensityMap()
    for line in reader.lines():
        density_map.add_line(line)
    #
    return density_map.get_minimum_path_cost()


@helpers.timer
def part2(reader):
    """Part 2"""
    result = None
    for line in reader.lines():
        ...
    #
    return result


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
