#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 11
blackstream-x’ solution
"""


import logging

import helpers


class OctopusGrid:

    """Grid of flashing dumbo octopuses"""

    def __init__(self):
        """Initialize grid"""
        self.__grid = {}
        self.total_flashes = 0
        self.lines = 0
        self.__about_to_flash = set()

    @property
    def size(self):
        """Return grid size"""
        return len(self.__grid)

    def add_line(self, line):
        """Add a line to the grid"""
        for (index, level) in enumerate(line):
            self.__grid[(index, self.lines)] = int(level)
        #
        self.lines += 1

    def draw(self):
        """Draw the grid: yield all lines"""
        for y_pos in range(self.lines):
            current_line = []
            x_pos = 0
            while True:
                try:
                    current_line.append(str(self.__grid[(x_pos, y_pos)]))
                except KeyError:
                    yield "".join(current_line)
                    break
                #
                x_pos += 1
            #
        #

    def __increase_energy(self, position):
        """Increase energy level of the octopus at position by 1"""
        try:
            new_level = self.__grid[position] + 1
        except KeyError:
            return
        #
        self.__grid[position] = new_level
        if new_level > 9:
            self.__about_to_flash.add(position)
        #

    def __flash(self, position):
        """Increase energy level of all position’s neighbors"""
        pos_x, pos_y = position
        for x_index in range(pos_x - 1, pos_x +2):
            for y_index in range(pos_y -1, pos_y + 2):
                if x_index != pos_x or y_index != pos_y:
                    self.__increase_energy((x_index, y_index))
                #
            #
        #

    def step(self):
        """Increase energy levels of each octous in the grid"""
        for position in self.__grid:
            self.__increase_energy(position)
        #
        has_flashed = set()
        while True:
            new_flashes = False
            while self.__about_to_flash:
                position = self.__about_to_flash.pop()
                if position in has_flashed:
                    continue
                #
                self.__flash(position)
                has_flashed.add(position)
                new_flashes = True
            #
            if not new_flashes:
                break
            #
        #
        for position in has_flashed:
            self.__grid[position] = 0
        #
        self.total_flashes += len(has_flashed)
        return len(has_flashed)

    def total_flashes_after(self, total_steps):
        """Return the number of flashes after total_steps"""
        for dummy_step_number in range(total_steps):
            self.step()
        #
        logging.debug("Grid after %s steps:", total_steps)
        for line in self.draw():
            logging.debug(line)
        #
        return self.total_flashes


@helpers.timer
def part1(reader):
    """Part 1"""
    grid = OctopusGrid()
    for line in reader.lines():
        grid.add_line(line)
    #
    logging.debug("Grid at start time:")
    for line in grid.draw():
        logging.debug(line)
    #
    return grid.total_flashes_after(100)


@helpers.timer
def part2(reader):
    """Part 2"""
    grid = OctopusGrid()
    for line in reader.lines():
        grid.add_line(line)
    #
    logging.debug("Grid at start time:")
    for line in grid.draw():
        logging.debug(line)
    #
    step_number = 1
    while True:
        if grid.step() == grid.size:
            break
        #
        step_number += 1
    #
    logging.debug("Grid after %s steps:", step_number)
    for line in grid.draw():
        logging.debug(line)
    #
    return step_number


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
