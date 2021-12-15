#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 13
blackstream-x’ solution

Requires pytesseract for OCRing the fold result
(pip install --user pytesseract)
"""


import logging
import pytesseract

from PIL import Image, ImageDraw
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
        self.width = max(x_pos, self.width)
        self.height = max(y_pos, self.height)

    def fold(self):
        """Fold once"""
        instructions = self.fold_instructions.pop(0)
        logging.debug("Folding at %s", instructions)
        axis, fold_position = instructions.split("=", 1)
        fold_position = int(fold_position)
        if axis == "x":
            folded_index = 0
            self.width = fold_position
        elif axis == "y":
            folded_index = 1
            self.height = fold_position
        #
        folded = set()
        for position in self.grid:
            if position[folded_index] == fold_position:
                continue
            #
            if position[folded_index] > fold_position:
                mutable_pos = list(position)
                mutable_pos[folded_index] = (
                    2 * fold_position - mutable_pos[folded_index]
                )
                folded.add(tuple(mutable_pos))
            else:
                folded.add(position)
            #
        #
        self.grid.clear()
        self.grid.update(folded)
        return len(self.grid)

    def display(self):
        """Print the grid using loglevel DEBUG"""
        logging.debug("Folded sheet:")
        for y_pos in range(self.height):
            line = []
            for x_pos in range(self.width):
                if (x_pos, y_pos) in self.grid:
                    line.append("#")
                else:
                    line.append(".")
                #
            #
            logging.debug("".join(line))
        #

    def get_image(self):
        """Return a grayscale image with a white background.
        Dots are drawn with an offset of 2 pixels
        because not leaving a border will produce
        incorrect results in the OCR
        """
        image = Image.new("L", (self.width + 4, self.height + 4), color=255)
        draw = ImageDraw.Draw(image)
        for (x_pos, y_pos) in self.grid:
            draw.point((x_pos + 2, y_pos + 2), fill=0)
        return image

    def get_secret_message(self):
        """Return the secret message from the folded sheet,
        determined by the Tesserat OCR.
        """
        return pytesseract.image_to_string(
            self.get_image(), config="--psm 7"
        ).strip()


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
    sheet.display()
    return sheet.get_secret_message()


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
