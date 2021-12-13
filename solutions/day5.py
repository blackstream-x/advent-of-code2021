#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 5
blackstream-x’ solution
"""


# import logging

import helpers


def count(start, end):
    """Yield all numbers from start and end (1-dimensional)"""
    try:
        step = (end - start) // abs(end - start)
    except ZeroDivisionError:
        raise StopIteration
    #
    for current in range(start, end + step, step):
        yield current
    #


def count_diag(start, end):
    """Yield number tuples (diagonally) from start and end"""
    step = [0, 0]
    for index in (0, 1):
        route = end[index] - start[index]
        if route:
            step[index] = route // abs(route)
        #
    #
    cur_x, cur_y = start
    while True:
        yield (cur_x, cur_y)
        if cur_x == end[0] and cur_y == end[1]:
            break
        #
        cur_x += step[0]
        cur_y += step[1]
    #


def positions_on_line(definition, enable_diagonal=False):
    """Yield all positions on the line"""
    line_ends = definition.split("->")
    [[start_x, start_y], [end_x, end_y]] = [
        [int(item.strip()) for item in current_end.split(",")]
        for current_end in line_ends
    ]
    if start_x == end_x:
        for current_y in count(start_y, end_y):
            yield helpers.Position(start_x, current_y)
        #
    elif start_y == end_y:
        for current_x in count(start_x, end_x):
            yield helpers.Position(current_x, start_y)
        #
    elif enable_diagonal:
        for pos in count_diag((start_x, start_y), (end_x, end_y)):
            yield helpers.Position(*pos)
        #
    #


def draw(vents_map):
    """Return a list of lines representing the map"""
    max_x = max(position.x for position in vents_map)
    max_y = max(position.y for position in vents_map)
    for row in range(max_x + 1):
        current_line = []
        for col in range(max_y + 1):
            try:
                nb_lines = vents_map[helpers.Position(col, row)]
            except KeyError:
                current_line.append(".")
            else:
                if nb_lines < 10:
                    current_line.append(str(nb_lines))
                else:
                    current_line.append("#")
                #
            #
        #
        yield "".join(current_line)
    #


@helpers.timer
def part1(reader):
    """Part 1"""
    vents_map = {}
    crossings = set()
    for line in reader.lines():
        for position in positions_on_line(line):
            vents_map[position] = vents_map.get(position, 0) + 1
            if vents_map[position] > 1:
                crossings.add(position)
        #
    #
    # for line in draw(vents_map):
    #     logging.debug(line)
    #
    return len(crossings)


@helpers.timer
def part2(reader):
    """Part 2"""
    vents_map = {}
    crossings = set()
    for line in reader.lines():
        for position in positions_on_line(line, enable_diagonal=True):
            vents_map[position] = vents_map.get(position, 0) + 1
            if vents_map[position] > 1:
                crossings.add(position)
        #
    #
    # for line in draw(vents_map):
    #     logging.debug(line)
    #
    return len(crossings)


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
