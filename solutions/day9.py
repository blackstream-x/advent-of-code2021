#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 9
blackstream-x’ solution
"""


import logging

import helpers


class LowestPoint(Exception):

    """Exception raised at lowest points"""

    ...


class OutOfMap(Exception):

    """Exception raised if trying to access a point outside the map"""

    ...


class HeightMap:

    """Height map of the submarine floor"""

    def __init__(self, lines_sequence):
        """Store lines"""
        self.lines = tuple(
            tuple(int(character) for character in line)
            for line in lines_sequence
        )
        self.max_y = len(self.lines) - 1
        self.basins = {}
        self.basins_lookup = {}

    def get_height(self, x_pos, y_pos):
        """Get the height at the indicated position"""
        if y_pos > self.max_y:
            raise OutOfMap
        #
        max_x = len(self.lines[y_pos]) - 1
        if x_pos < 0 or y_pos < 0 or x_pos > max_x:
            raise OutOfMap
        #
        return self.lines[y_pos][x_pos]

    def smallest_neighbor(self, x_pos, y_pos):
        """Return the smallest neighbor’s coordinates"""
        own_height = self.get_height(x_pos, y_pos)
        lowest_height = own_height
        lowest_coords = (x_pos, y_pos)
        for (n_x, n_y) in (
            (x_pos - 1, y_pos),
            (x_pos + 1, y_pos),
            (x_pos, y_pos - 1),
            (x_pos, y_pos + 1)
        ):
            try:
                neighbor_height = self.get_height(n_x, n_y)
            except OutOfMap:
                continue
            #
            if neighbor_height <= lowest_height:
                lowest_coords = (n_x, n_y)
                lowest_height = neighbor_height
            #
        #
        if lowest_coords == (x_pos, y_pos):
            raise LowestPoint
        #
        return lowest_coords

    def find_low_point_coordinates(self):
        """Yield (x,y) of all low points"""
        for y_index, row in enumerate(self.lines):
            for x_index in range(len(row)):
                try:
                    self.smallest_neighbor(x_index, y_index)
                except LowestPoint:
                    logging.debug(
                        "Found lowest point at x: %s / y: %s", x_index, y_index
                    )
                    yield (x_index, y_index)
                #
            #
        #

    def find_low_points(self):
        """Yield all low point values"""
        for (x_pos, y_pos) in self.find_low_point_coordinates():
            yield self.get_height(x_pos, y_pos)
        #

    def add_to_basin(self, lowest_point, *positions):
        """Add all positions to the basin.
        If only the lowest point was given, create a new basin.
        """
        if not positions:
            self.basins[lowest_point] = {lowest_point}
            self.basins_lookup[lowest_point] = lowest_point
        #
        for position in positions:
            self.basins_lookup[position] = lowest_point
            self.basins[lowest_point].add(position)
        #

    def find_basins(self):
        """Find all basins"""
        for (x_pos, y_pos) in self.find_low_point_coordinates():
            self.add_to_basin((x_pos, y_pos))
        #
        for y_index, row in enumerate(self.lines):
            for x_index, point in enumerate(row):
                if (x_index, y_index) in self.basins_lookup:
                    continue
                current_height = int(point)
                if current_height == 9:
                    continue
                #
                # Move in the direction of the mallest neighbor
                x_pos = x_index
                y_pos = y_index
                visited_positions = [(x_pos, y_pos)]
                while True:
                    (x_pos, y_pos) = self.smallest_neighbor(x_pos, y_pos)
                    try:
                        basin_id = self.basins_lookup[(x_pos, y_pos)]
                    except KeyError:
                        visited_positions.append((x_pos, y_pos))
                        continue
                    #
                    self.add_to_basin(basin_id, *visited_positions)
                    break
                #
            #
        #


@helpers.timer
def part1(reader):
    """Part 1"""
    height_map = HeightMap(reader.lines())
    result = sum(height + 1 for height in height_map.find_low_points())
    return result


@helpers.timer
def part2(reader):
    """Part 2"""
    height_map = HeightMap(reader.lines())
    height_map.find_basins()
    basins_by_size = sorted(
        [len(positions) for positions in height_map.basins.values()]
    )
    biggest_basins = basins_by_size[-3:]
    logging.debug("Biggest basin sizes: %r", biggest_basins)
    result = 1
    while True:
        try:
            result = result * biggest_basins.pop()
        except IndexError:
            return result
        #
    #


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
