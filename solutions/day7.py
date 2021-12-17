#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 7
blackstream-x’ solution
"""


import logging

import helpers


class CrabSwarm:

    """Simple crab swarm (Solution part 1)"""

    def __init__(self, line):
        """Determine and sort values"""
        self.sorted = sorted(int(item) for item in line.split(","))

    @property
    def median_position(self):
        """Return median value.
        Due to zero-based indexing,
        half_index matches exactly for odd lengths
        and is the upper central index for even lengths
        """
        half_index, is_odd = divmod(len(self.sorted), 2)
        if is_odd:
            return self.sorted[half_index]
        #
        return round(
            (self.sorted[half_index - 1] + self.sorted[half_index]) / 2
        )

    def single_distances(self, position):
        """Yield distances to position"""
        for value in self.sorted:
            yield abs(value - position)
        #

    def fuel_cost_to(self, position):
        """Sum of fuel cost to position:
        fuel cost = distance
        """
        return sum(self.single_distances(position))

    def is_better_than(self, old_pos, new_pos):
        """True if new_pos has a lower fiuel cost than old_pos"""
        return self.fuel_cost_to(new_pos) < self.fuel_cost_to(old_pos)


class UnderstoodCrabSwarm(CrabSwarm):

    """Revised crab swarm after understanding crab mechanics
    (Solution part 2)
    """

    def fuel_cost_to(self, position):
        """Sum of fuel cost to position:
        fuel cost or the first step is 1 and increases
        by 1 for each step -> sum(1..n) = (n / 2) * (n + 1)
        """
        return sum(
            int(distance / 2 * (distance + 1))
            for distance in self.single_distances(position)
        )


@helpers.timer
def part1(reader):
    """Part 1"""
    for line in reader.lines():
        crab_swarm = CrabSwarm(line)
        best_position = crab_swarm.median_position
        logging.debug("Assuming best position (median): %s", best_position)
        # Test lower and higher positions
        for delta in (-1, 1):
            current_pos = best_position
            while True:
                current_pos = current_pos + delta
                if crab_swarm.is_better_than(best_position, current_pos):
                    logging.debug("Found better position: %s", current_pos)
                    best_position = current_pos
                else:
                    break
                #
            #
        #
        return crab_swarm.fuel_cost_to(best_position)
    #


@helpers.timer
def part2(reader):
    """Part 2"""
    for line in reader.lines():
        crab_swarm = UnderstoodCrabSwarm(line)
        best_position = crab_swarm.median_position
        logging.debug("Assuming best position (median): %s", best_position)
        # Test lower and higher positions
        for delta in (-1, 1):
            current_pos = best_position
            while True:
                current_pos = current_pos + delta
                if crab_swarm.is_better_than(best_position, current_pos):
                    logging.debug("Found better position: %s", current_pos)
                    best_position = current_pos
                else:
                    break
                #
            #
        #
        return crab_swarm.fuel_cost_to(best_position)
    #


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
