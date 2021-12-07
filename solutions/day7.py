#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 7
blackstream-x’ solution
"""


import logging

import helpers


class CrabSwarm:

    def __init__(self, line):
        values = [int(item) for item in line.split(",")]
        self.sorted = sorted(values)
        self.number = len(values)

    @property
    def median(self):
        half_index, is_odd = divmod(self.number, 2)
        # Due to zero-based indexing,
        # half_index matches exactly for odd lengths
        # and is the upper central index for even lengths
        #
        if is_odd:
            return self.sorted[half_index]
        #
        return round(
            (self.sorted[half_index - 1] + self.sorted[half_index]) / 2
        )

    def single_distances(self, position):
        for value in self.sorted:
            yield abs(value - position)
        #

    def fuel_cost_to(self, position):
        return sum(self.single_distances(position))

    def is_better_than(self, old_pos, new_pos):
        return self.fuel_cost_to(new_pos) < self.fuel_cost_to(old_pos)


class UnderstoodCrabSwarm(CrabSwarm):

    def fuel_cost_to(self, position):
        return sum(
            int(distance / 2 * (distance + 1))
            for distance in self.single_distances(position)
        )


@helpers.timer
def part1(reader):
    """Part 1"""
    for line in reader.lines():
        positions = CrabSwarm(line)
        best_position = positions.median
        logging.debug("Assuming best position (median): %s", best_position)
        # Test lower and higher positions
        for delta in (-1, 1):
            current_pos = best_position
            while True:
                current_pos = current_pos + delta
                if positions.is_better_than(best_position, current_pos):
                    logging.debug("Found better position: %s", current_pos)
                    best_position = current_pos
                else:
                    break
                #
            #
        #
        return positions.fuel_cost_to(best_position)
    #


@helpers.timer
def part2(reader):
    """Part 2"""
    for line in reader.lines():
        positions = UnderstoodCrabSwarm(line)
        best_position = positions.median
        logging.debug("Assuming best position (median): %s", best_position)
        # Test lower and higher positions
        for delta in (-1, 1):
            current_pos = best_position
            while True:
                current_pos = current_pos + delta
                if positions.is_better_than(best_position, current_pos):
                    logging.debug("Found better position: %s", current_pos)
                    best_position = current_pos
                else:
                    break
                #
            #
        #
        return positions.fuel_cost_to(best_position)
    #


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
