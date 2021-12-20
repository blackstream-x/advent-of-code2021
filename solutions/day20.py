#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 20
blackstream-x’ solution
"""


import logging

import helpers


INPUT2BIN = str.maketrans({".": "0", "#": "1"})
BIN2OUTPUT = str.maketrans({"0": ".", "1": "#"})

SEPARATOR = "=" * 70


class InputImage:

    """Input image"""

    def __init__(self, enhancement_algorithm):
        """Initialize grid"""
        self.matrix = {}
        self.height = 0
        self.width = 0
        self.min_x = 0
        self.min_y = 0
        self.enhancement_algorithm = enhancement_algorithm
        self.dark_values = 0

    def add_line(self, line):
        """Add a line to the map"""
        if not line:
            return
        #
        for (index, pixel) in enumerate(line):
            # if int(pixel.translate(INPUT2BIN)):
            self.matrix[(index, self.height)] = int(pixel.translate(INPUT2BIN))
            #
        #
        self.width = max(self.width, len(line))
        self.height += 1

    def get_enhancement_index(self, position):
        """Return the enhancement index"""
        index = []
        x_pos, y_pos = position
        for y_index in range(y_pos - 1, y_pos + 2):
            for x_index in range(x_pos - 1, x_pos + 2):
                index.append(
                    str(self.matrix.get((x_index, y_index), self.dark_values))
                )
            #
        #
        return int("".join(index), 2)

    def enhance(self):
        """Enhance the image"""
        output = {}
        self.min_x -= 1
        self.min_y -= 1
        self.width += 2
        self.height += 2
        max_x = self.min_x + self.width
        max_y = self.min_y + self.height
        for x_index in range(self.min_x, max_x):
            for y_index in range(self.min_y, max_y):
                position = (x_index, y_index)
                enh_index = self.get_enhancement_index(position)
                # if self.enhancement_algorithm & 1 << (enh_index):
                output[position] = int(
                    bool(self.enhancement_algorithm & 1 << (enh_index))
                )
                #
                #
            #
        #
        if self.enhancement_algorithm & 1:
            self.dark_values = self.dark_values ^ 1
        #
        self.matrix = output

    def draw(self):
        """Draw the current matrix"""
        max_x = self.min_x + self.width
        max_y = self.min_y + self.height
        for y_index in range(self.min_y, max_y):
            line = []
            for x_index in range(self.min_x, max_x):
                line.append(str(self.matrix.get((x_index, y_index), 0)))
            #
            logging.info("".join(line).translate(BIN2OUTPUT))
        #


def parse_input(reader):
    """Return the image enhancement algorithm
    and the input image as a tuple
    """
    enhancement_algorithm = None
    image = None
    for line in reader.lines():
        if enhancement_algorithm is None:
            if len(line) != 512:
                raise ValueError("Image enhancement algorithm incomplete!")
            #
            enhancement_algorithm = int(line.translate(INPUT2BIN)[::-1], 2)
            continue
        #
        if image is None:
            image = InputImage(enhancement_algorithm)
        #
        image.add_line(line)
    #
    return image


@helpers.timer
def part1(reader):
    """Part 1"""
    image = parse_input(reader)
    logging.info(image.enhancement_algorithm)
    image.draw()
    logging.info(SEPARATOR)
    image.enhance()
    image.draw()
    logging.info(SEPARATOR)
    image.enhance()
    image.draw()
    logging.info(SEPARATOR)
    return sum(image.matrix.values())


@helpers.timer
def part2(reader):
    """Part 2"""
    image = parse_input(reader)
    logging.info(image.enhancement_algorithm)
    image.draw()
    logging.info(SEPARATOR)
    logging.info("50 enhancements later ...")
    for _ in range(50):
        image.enhance()
    #
    image.draw()
    logging.info(SEPARATOR)
    return sum(image.matrix.values())


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
