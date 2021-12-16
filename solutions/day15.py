#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 15

I failed to manage it myself this time;
solution part 1 is ripped off from
<https://github.com/macobo/aoc-2021/blob/master/day15.py>
"""


import heapq
import logging

import helpers


class ChitonDensityMap:

    """Map of Chiton density"""

    start_point = (0, 0)

    def __init__(self):
        """Initialize grid"""
        self.matrix = {}
        self.height = 0
        self.width = 0

    def add_line(self, line):
        """Add a line to the map"""
        for (index, density) in enumerate(line):
            self.matrix[(index, self.height)] = int(density)
        #
        self.width = max(self.width, len(line))
        self.height += 1

    def neighbors(self, position):
        """Yield all horizontal and vertical
        neighbor positions if inside the matrix
        """
        x_pos, y_pos = position
        # left neighbor
        if x_pos > 0:
            yield (x_pos - 1, y_pos)
        #
        # right neighbor
        if x_pos < self.width - 1:
            yield (x_pos + 1, y_pos)
        #
        # upper neighbor
        if y_pos > 0:
            yield (x_pos, y_pos - 1)
        #
        # lower neighbor
        if y_pos < self.height - 1:
            yield (x_pos, y_pos + 1)
        #

def get_heap_based_cost(matrix):
    """Return minimum path cost using a binary heap

    ================================================================
    Measured times with this algorithm:

    Running command: solutions/day15.py inputs/15.txt

    INFO     | Executed 'Part 1' in 80.100 msec (80100.3 µsec)
    652
    INFO     | Executed 'Part 2' in 2321.449 msec (2321448.6 µsec)
    2938
    ================================================================
    """
    end_point = (matrix.width - 1, matrix.height - 1)
    visited = set()
    work_heap = []
    heapq.heappush(work_heap, (0, matrix.start_point))
    while work_heap:
        cost, current_position = heapq.heappop(work_heap)
        if current_position in visited:
            continue
        #
        logging.debug("Visiting position %r ...", current_position)
        visited.add(current_position)
        if current_position == end_point:
            return cost
        #
        for neighbor_position in matrix.neighbors(current_position):
            # Never consider already visited psitions again
            if neighbor_position in visited:
                continue
            #
            heapq.heappush(
                work_heap,
                (cost + matrix.matrix[neighbor_position], neighbor_position),
            )
        #
    #


def get_set_based_cost(matrix):
    """Return minimum path cost using a set

    ====================================================================
    Measured times with this algorithm:

    Running command: solutions/day15.py inputs/15.txt

    INFO     | Executed 'Part 1' in 312.598 msec (312597.5 µsec)
    652
    INFO     | Executed 'Part 2' in 42630.289 msec (42630288.8 µsec)
    2938
    ====================================================================
    """
    end_point = (matrix.width - 1, matrix.height - 1)
    visited = set()
    work_area = set([(0, matrix.start_point)])
    while work_area:
        cheapest = min(work_area)
        work_area.remove(cheapest)
        cost, current_position = cheapest
        if current_position in visited:
            continue
        #
        logging.debug("Visiting position %r ...", current_position)
        visited.add(current_position)
        if current_position == end_point:
            return cost
        #
        for neighbor_position in matrix.neighbors(current_position):
            # Never consider already visited psitions again
            if neighbor_position in visited:
                continue
            #
            work_area.add(
                (cost + matrix.matrix[neighbor_position], neighbor_position)
            )
        #
    #


def blow_up(reader):
    """Yield blown-up lines as outlined in part2 description"""
    repeated_lines = []
    for line in reader.lines():
        repetitions = []
        for increase in range(9):
            repetitions.append([])
        #
        for (index, item) in enumerate(line):
            density = int(item)
            for increase in range(9):
                repetitions[increase].append((density - 1 + increase) % 9 + 1)
            #
        #
        repeated_lines.append(
            [
                "".join([format(density) for density in block])
                for block in repetitions
            ]
        )
    #
    for multiplied_height in range(5):
        for (line_number, blocks) in enumerate(repeated_lines):
            logging.debug(blocks)
            yield "".join(blocks[:5])
            blocks.pop(0)
        #
    #


@helpers.timer
def part1(reader):
    """Part 1"""
    density_map = ChitonDensityMap()
    for line in reader.lines():
        density_map.add_line(line)
    #
    return get_heap_based_cost(density_map)
    # return get_set_based_cost(density_map)


@helpers.timer
def part2(reader):
    """Part 2"""
    density_map = ChitonDensityMap()
    for line in blow_up(reader):
        density_map.add_line(line)
    #
    return get_heap_based_cost(density_map)
    # return get_set_based_cost(density_map)


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
