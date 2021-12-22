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



class Cuboid:

    """Represents a cuboit of cubes"""

    axes = "xyz"

    def __init__(self, **kwargs):
        """Initialize cuboid dimensions"""
        self.dimensions = {}
        for axis in self.axes:
            start, end = kwargs[axis]
            # Swap coordinates if necessary
            if start > end:
                start, end = end, start
            #
            self.dimensions[axis] = (start, end)
        #

    @classmethod
    def from_string(cls, coordinates, limits=None):
        """Parse coordinates and return a cuboid instance"""
        limits = limits or {}
        # Evaluate coordinates
        dimensions = {}
        for dimension in coordinates.split(","):
            axis, values = dimension.split("=", 1)
            min_limit, max_limit = limits.get(axis, (None, None))
            start_coord, end_coord = [int(item) for item in values.split("..")]
            # Swap coordinates if necessary
            if start_coord > end_coord:
                start_coord, end_coord = end_coord, start_coord
            #
            if min_limit is not None and start_coord < min_limit:
                start_coord = min_limit
            #
            if max_limit is not None and end_coord > max_limit:
                end_coord = max_limit
            #
            if start_coord > end_coord:
                raise ValueError("Limits exceeded")
            #
            dimensions[axis] = (start_coord, end_coord)
        #
        return cls(**dimensions)

    @property
    def width(self):
        """Return width (x dimension)"""
        return self.x[1] + 1 - self.x[0]

    @property
    def height(self):
        """Return height (y dimension)"""
        return self.y[1] + 1 - self.y[0]

    @property
    def depth(self):
        """Return depth (z dimension)"""
        return self.z[1] + 1 - self.z[0]

    def __getitem__(self, name):
        """Return the dimensions"""
        return self.dimensions[name]

    def __getattr__(self, name):
        """Return the dimensions"""
        return self[name]

    def all_cubes(self):
        """Return an iterator over all cubes in the cuboid"""
        dimension_ranges = []
        for axis in self.axes:
            minimum, maximum = self.dimensions[axis]
            dimension_ranges.append(range(minimum, maximum + 1))
        #
        return itertools.product(*dimension_ranges)

    def volume(self):
        """Return the volume of the cuboid"""
        return self.width * self.height * self.depth

    def intersection(self, other):
        """Return the cuboid intersecting between self and other,
        or None if there is no intersection
        """
        intersect = {}
        for axis, my_coord in self.dimensions.items():
            your_coord = other[axis]
            if any(
                (
                    my_coord[0] > your_coord[1],
                    my_coord[1] > your_coord[0],
                )
            ):
                # No intersection
                logging.debug("No intersection")
                return None
            #
            intersect[axis] = (
                max(my_coord[0], your_coord[0]),
                min(my_coord[1], your_coord[1]),
            )
        #
        return Cuboid(**intersect)

    def split(self, **kwargs):
        """Return a list of non-overlapping cuboids,
        split at the given coordiates,
        oriented to the smaller side:
        a cuboid(x=(2,5), y=(6,7), z=(0,1))
        split at x=(3,4) would be splitted into 3 cuboids:
        one (x=2,2, y=(6,7), z=(0,1))
        one (x=3,3, y=(6,7), z=(0,1))
        and one (x=4,5, y=(6,7), z=(0,1))
        """
        split_cuboids = [self]
        for axis in self.axes:
            try:
                split_at = kwargs[axis]
            except KeyError:
                continue
            #
            for coord in split_at:
                new_cuboids = []
                for cuboid in split_cuboids:
                    work_dims = dict(cuboid.dimensions)
                    minor_1 = cuboid[axis][0]
                    major_2 = cuboid[axis][1]
                    if minor_1 - 1 <= coord <= major_2:
                        major_1 = coord
                        minor_2 = major_1 - 1
                        work_dims.update({axis: (minor_1, minor_2)})
                        new_cuboids.append(Cuboid(**work_dims))
                        work_dims.update({axis: (major_1, major_2)})
                        new_cuboids.append(Cuboid(**work_dims))
                    else:
                        new_cuboids.append(cuboid)
                    #
                #
                split_cuboids = new_cuboids
            #
        #
        return split_cuboids

    def __eq__(self, other):
        """Equality test"""
        for axis in self.axes:
            if self[axis] != other[axis]:
                return False
            #
        #
        return True

    def __ne__(self, other):
        """Inequality test"""
        for axis in self.axes:
            if self[axis] == other[axis]:
                return False
            #
        #
        return True

    def __add__(self, other):
        """Add self and another cuboid.
        Returns a list of non-overlapping cuboids that,
        put together, exactly use the room of both cuboids
        """
        return (self - other) + [other]

    def __sub__(self, other):
        """Subtract other from self"""
        intersected = self.intersection(other)
        if not intersected:
            return [self]
        #
        logging.debug("Subtracting %s from %s", other, self)
        split_coordinates = {}
        for axis in self.axes:
            start, end = intersected[axis]
            split_coordinates[axis] = (start, end + 1)
        #
        non_overlapping = [
            cuboid for cuboid in self.split(**split_coordinates)
            if cuboid != intersected
        ]
        return non_overlapping


def cubes_in_cuboid(coordinates, limits=None):
    """Return an iterator over all cubes in the cuboid"""
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
def part0(reader):
    """Part 0"""
    reactor = set()
    for line in reader.lines():
        instruction, coordinates = line.split(None, 1)
        logging.debug("%s => %s cubes", coordinates, len(list(cubes_in_cuboid(coordinates, limits=PART_1_LIMITS))))
        OPERATIONS[instruction](reactor, cubes_in_cuboid(coordinates, limits=PART_1_LIMITS))
    #
    return len(reactor)


@helpers.timer
def part1(reader):
    """Part 1"""
    reactor = []
    for line in reader.lines():
        instruction, coordinates = line.split(None, 1)
        try:
            new_cuboid = Cuboid.from_string(coordinates, limits=PART_1_LIMITS)
        except ValueError as error:
            logging.warning(error)
            continue
        #
        logging.debug("%s => %s cubes", new_cuboid.dimensions, new_cuboid.volume())
        new_reactor = []
        while reactor:
            current_cuboid = reactor.pop()
            new_reactor.extend(current_cuboid - new_cuboid)
        #
        if instruction == "on":
            new_reactor.append(new_cuboid)
        #
        reactor = new_reactor
    #
    return sum(cuboid.volume() for cuboid in reactor)


@helpers.timer
def part2(reader):
    """Part 2"""
    # TODO: cuboid addition and subtraction algorithm
    result = None
    for line in reader.lines():
        ...
    #
    return result


if __name__ == "__main__":
    helpers.solve_puzzle(part0, part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
