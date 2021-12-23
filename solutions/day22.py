#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 22
blackstream-x’ solution
"""


import logging

import helpers


MINI_TEST_DATA = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

EXPECTED_MINI_TEST_RESULT = 39

INITIALIZATION_AREA = dict(x=(-50, 50), y=(-50, 50), z=(-50, 50))

SEPARATOR_LINE = "-" * 70


class LimitsExceeded(Exception):

    """Raised by the factory method when limits were exceeeded"""

    ...


class Cuboid:

    """Represents a cuboid"""

    axes = "xyz"

    def __init__(self, **kwargs):
        """Initialize cuboid dimensions"""
        self.dimensions = {}
        for axis in self.axes:
            start, end = kwargs[axis]
            if start > end:
                raise ValueError(
                    f"Invalid coordinates {kwargs}; all start coordinates must"
                    " be less or equal to their respective end coordinate!"
                )
            #
            self.dimensions[axis] = (start, end)
        #

    @classmethod
    def from_string(cls, coordinates, limits=None):
        """Factory method: Parse coordinates and return a cuboid instance"""
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
                raise LimitsExceeded
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
        """Return an iterator over all cubes
        (ie. (x, y, z) positions tuples) in the cuboid"""
        dimension_ranges = {}
        for axis in self.axes:
            minimum, maximum = self.dimensions[axis]
            dimension_ranges[axis] = range(minimum, maximum + 1)
        #
        for x_pos in dimension_ranges["x"]:
            for y_pos in dimension_ranges["y"]:
                for z_pos in dimension_ranges["z"]:
                    yield (x_pos, y_pos, z_pos)
                #
            #
        #

    def volume(self):
        """Return the volume of the cuboid"""
        return self.width * self.height * self.depth

    def intersection(self, other):
        """Return the cuboid intersecting between self and other,
        or None if there is no intersection
        """
        intersect_data = {}
        for axis, my_coord in self.dimensions.items():
            your_coord = other[axis]
            if any(
                (
                    my_coord[0] > your_coord[1],
                    my_coord[1] < your_coord[0],
                )
            ):
                # No intersection
                return None
            #
            intersect_data[axis] = (
                max(my_coord[0], your_coord[0]),
                min(my_coord[1], your_coord[1]),
            )
        #
        intersect_cuboid = Cuboid(**intersect_data)
        logging.debug(
            "[intersect] Intersection of %s and %s => %s",
            self,
            other,
            intersect_cuboid,
        )
        return intersect_cuboid

    def split(self, **kwargs):
        """Return a list of non-overlapping cuboids,
        split at the given coordiates,
        oriented to the smaller side:
        a cuboid with (x=(2,5), y=(6,7), z=(0,1))
        split at x=(3,4) would be splitted into 3 cuboids:
        one with (x=2,2, y=(6,7), z=(0,1))
        one with (x=3,3, y=(6,7), z=(0,1))
        and one with (x=4,5, y=(6,7), z=(0,1))
        """
        logging.debug("[split] Splitting %s at %s ...", self, kwargs)
        split_cuboids = set([self])
        for axis in self.axes:
            try:
                split_at = kwargs[axis]
            except KeyError:
                continue
            #
            for coord in split_at:
                new_cuboids = set()
                for cuboid in split_cuboids:
                    work_dims = dict(cuboid.dimensions)
                    minor_1 = cuboid[axis][0]
                    major_2 = cuboid[axis][1]
                    if minor_1 + 1 <= coord <= major_2:
                        logging.debug(
                            "[split] * Splitting %s at %s=%s into:",
                            cuboid,
                            axis,
                            coord,
                        )
                        major_1 = coord
                        minor_2 = major_1 - 1
                        work_dims.update({axis: (minor_1, minor_2)})
                        result1 = Cuboid(**work_dims)
                        work_dims.update({axis: (major_1, major_2)})
                        result2 = Cuboid(**work_dims)
                        logging.debug("[split]    - %s", result1)
                        logging.debug("[split]    - %s", result2)
                        new_cuboids.update((result1, result2))
                    else:
                        new_cuboids.add(cuboid)
                    #
                #
                split_cuboids = new_cuboids
                logging.debug(
                    "[split] * after %s=%s split: %s cuboids",
                    axis,
                    coord,
                    len(split_cuboids),
                )
            #
        #
        logging.debug(
            "[split] Split resulted in %s cuboids", len(split_cuboids)
        )
        return list(split_cuboids)

    def __hash__(self):
        """hash value"""
        return hash(str(self))

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
            if self[axis] != other[axis]:
                return True
            #
        #
        return False

    def __str__(self):
        """String representation"""
        dims = []
        for axis in self.axes:
            start, end = self[axis]
            dims.append(f"{axis}=({start},{end})")
        #
        return f"{self.__class__.__name__}({','.join(dims)})"

    def __sub__(self, other):
        """Subtract other from self"""
        intersected = self.intersection(other)
        if not intersected:
            return [self]
        #
        split_coordinates = {}
        for axis in self.axes:
            start, end = intersected[axis]
            split_coordinates[axis] = (start, end + 1)
        #
        non_overlapping = [
            cuboid
            for cuboid in self.split(**split_coordinates)
            if cuboid != intersected
        ]
        logging.debug(
            "[sub] Subtracting %s from %s resulted in %s cuboids:",
            other,
            self,
            len(non_overlapping),
        )
        for cuboid in non_overlapping:
            logging.debug("[sub] %s", cuboid)
        #
        return non_overlapping


def operate_reactor(line_generator, expected_result=None, limits=None):
    """Operate the reactor.
    Adding a cuboid turns all cubes in the cuboid on,
    subtracting it turns all of them off.
    Before adding a cuboid, it is subtracted from all
    existing cuboids in the reactor, thus guaranteeing
    that no cuboids overlap.
    """
    reactor = set()
    processed_lines = 0
    skipped_lines = 0
    try:
        for line in line_generator():
            instruction, coordinates = line.split(None, 1)
            try:
                new_cuboid = Cuboid.from_string(coordinates, limits=limits)
            except LimitsExceeded:
                skipped_lines += 1
                continue
            except ValueError as error:
                logging.error(error)
                continue
            #
            new_reactor = set()
            while reactor:
                current_cuboid = reactor.pop()
                new_reactor.update(current_cuboid - new_cuboid)
            #
            if instruction == "on":
                new_reactor.add(new_cuboid)
                logging.info("Switched on %s", new_cuboid)
            else:
                logging.info("Switched off %s", new_cuboid)
            #
            reactor = new_reactor
            processed_lines += 1
        #
    except KeyboardInterrupt:
        pass
    else:
        processed_lines = f"all {processed_lines}"
    #
    total_volume = sum(cuboid.volume() for cuboid in reactor)
    logging.info(
        "After processing %s lines, the reactor contains %s"
        " non-overlapping cuboids with a total volume of %s cubes.",
        processed_lines,
        len(reactor),
        total_volume,
    )
    if skipped_lines:
        logging.info(
            "Skipped %s lines due to the limits of %s.", skipped_lines, limits
        )
    #
    if expected_result:
        if total_volume == expected_result:
            logging.info("This matches the expected result.")
        else:
            logging.error("This does NOT match the expected result!")
        #
    #
    return total_volume


@helpers.timer
def part0(*unused_reader):
    """Part 0"""
    return operate_reactor(
        MINI_TEST_DATA.splitlines, expected_result=EXPECTED_MINI_TEST_RESULT
    )


@helpers.timer
def part1(reader):
    """Part 1"""
    return operate_reactor(reader.lines, limits=INITIALIZATION_AREA)


@helpers.timer
def part2(reader):
    """Part 2"""
    return operate_reactor(reader.lines)


if __name__ == "__main__":
    helpers.solve_puzzle(part0, part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
