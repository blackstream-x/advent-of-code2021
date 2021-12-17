#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 12
blackstream-x’ solution
"""


# import logging

import helpers


class CaveNavigator:

    """Find paths through caves"""

    def __init__(self):
        """Initialize base data structure"""
        self.caves = {}

    def add_connection(self, line):
        """Add a connection"""
        cave_1, cave_2 = line.split("-", 1)
        self.caves.setdefault(cave_1, set()).add(cave_2)
        self.caves.setdefault(cave_2, set()).add(cave_1)

    def find_paths(self, allow_one_double_visit=False):
        """Yield all unique paths from start to end,
        visiting small caves only once.
        Allow one double visit of a small cave if specified so.
        """
        for found_path in self.__recursive_path_finder(
            "start", visited_twice=not allow_one_double_visit
        ):
            yield found_path
        #

    def __recursive_path_finder(self, *visited_caves, visited_twice=False):
        """Yield all paths starting with visited_caves
        and ending in "end"
        """
        for possible_next in self.caves[visited_caves[-1]]:
            this_cave_visited_twice = visited_twice
            if possible_next.islower():
                if possible_next in visited_caves:
                    if possible_next in ("start", "end"):
                        continue
                    #
                    if this_cave_visited_twice:
                        continue
                    #
                    this_cave_visited_twice = True
                #
            #
            if possible_next == "end":
                yield tuple(visited_caves) + ("end",)
                continue
            #
            for found_path in self.__recursive_path_finder(
                *visited_caves,
                possible_next,
                visited_twice=this_cave_visited_twice,
            ):
                yield found_path
            #
        #


@helpers.timer
def part1(reader):
    """Part 1"""
    navigator = CaveNavigator()
    for line in reader.lines():
        navigator.add_connection(line)
    #
    paths = list(navigator.find_paths())
    return len(paths)


@helpers.timer
def part2(reader):
    """Part 2"""
    navigator = CaveNavigator()
    for line in reader.lines():
        navigator.add_connection(line)
    #
    paths = list(navigator.find_paths(allow_one_double_visit=True))
    return len(paths)


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
