#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 13
blackstream-x’ solution
"""


import logging

import helpers


class TransparentOrigami:

    """Transparent origami sheet"""

    def __init__(self):
        """Initialize the matrix"""
        self.grid = set()
        self.width = 0
        self.height = 0
        self.fold_instructions = []

    def add_line(self, line):
        """Add one line (point coordinates or fold instructions)"""
        if line.startswith("fold along"):
            self.fold_instructions.append(line.split()[2])
            return
        #
        [x_pos, y_pos] = [int(item) for item in line.split(",", 1)]
        self.grid.add((x_pos, y_pos))

    def fold(self):
        """Fold once"""
        instructions = self.fold_instructions.pop(0)
        logging.debug("Folding at %s", instructions)
        axis, fold_position = instructions.split("=", 1)
        fold_position = int(fold_position)
        if axis == "x":
            folded_index = 0
        elif axis == "y":
            folded_index = 1
        #
        folded = set()
        for position in self.grid:
            if position[folded_index] == fold_position:
                continue
            #
            if position[folded_index] > fold_position:
                mutable_pos = list(position)
                # logging.debug("%r =>", mutable_pos)
                mutable_pos[folded_index] = 2 * fold_position - mutable_pos[folded_index]
                # logging.debug("%r", mutable_pos)
                folded.add(tuple(mutable_pos))
            else:
                folded.add(position)
            #
        #
        self.grid.clear()
        self.grid.update(folded)
        return len(self.grid)

    def print(self):
        """Print the grid"""
        max_x = max(pos[0] for pos in self.grid)
        max_y = max(pos[1] for pos in self.grid)
        output = [
            ["." for x_pos in range(max_x + 1)]
            for y_pos in range(max_y + 1)
        ]
        for (x_pos, y_pos) in self.grid:
            output[y_pos][x_pos] = "#"
        #
        for line in output:
            print("".join(line))
        #


@helpers.timer
def part1(reader):
    """Part 1"""
    sheet = TransparentOrigami()
    for line in reader.lines():
        sheet.add_line(line)
    #
    return sheet.fold()


@helpers.timer
def part2(reader):
    """Part 2"""
    sheet = TransparentOrigami()
    for line in reader.lines():
        sheet.add_line(line)
    #
    while True:
        try:
            sheet.fold()
            # sheet.print()
        except IndexError:
            break
        #
    #
    sheet.print()
    return len(sheet.grid)


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
