#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 25
blackstream-x’ solution
"""


import logging

import helpers


class SeaCucumberMap:

    """Map of Sea cucumber swarms"""

    herd_symbols = ">v"

    def __init__(self):
        """Initialize the map"""
        self.herds = {">": set(), "v": set()}
        self.width = 0
        self.height = 0

    def add_line(self, line):
        """Add a line"""
        self.width = max(len(line), self.width)
        for index, symbol in enumerate(line):
            if symbol in self.herd_symbols:
                self.herds[symbol].add((index, self.height))
            #
        #
        self.height += 1

    def step(self):
        """Move both herds and return the numberof cucumbers that moved"""
        moved_cucumbers = 0
        for herd_id in self.herd_symbols:
            selector = self.herd_symbols.index(herd_id)
            old_positions = set()
            new_positions = set()
            for position in self.herds[herd_id]:
                test_pos = list(position)
                test_pos[selector] = test_pos[selector] + 1
                if selector:
                    if test_pos[1] >= self.height:
                        test_pos[1] = 0
                    #
                else:
                    if test_pos[0] >= self.width:
                        test_pos[0] = 0
                    #
                #
                test_pos = tuple(test_pos)
                if any(test_pos in self.herds[symbol] for symbol in self.herd_symbols):
                    continue
                #
                old_positions.add(position)
                new_positions.add(test_pos)
            #
            self.herds[herd_id].difference_update(old_positions)
            self.herds[herd_id].update(new_positions)
            moved_cucumbers += len(new_positions)
        #
        return moved_cucumbers



@helpers.timer
def part1(reader):
    """Part 1"""
    scm = SeaCucumberMap()
    for line in reader.lines():
        scm.add_line(line)
    #
    steps = 0
    while True:
        steps += 1
        moved_scs = scm.step()
        if not moved_scs:
            return steps
        #
    #
    #return result


@helpers.timer
def part2(reader):
    """Part 2"""
    result = None
    for line in reader.lines():
        ...
    #
    return result


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
