#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 4
blackstream-x’ solution
"""


import helpers


class Bingo(Exception):

    """Raised if a board detects 'Bingo!'"""

    ...


class Board:

    """A Bingo board"""

    size = 5
    index_row, index_col = 0, 1

    def __init__(self):
        """Initialize the board"""
        self.lines = []
        self.unmarked = {}
        self.marked = {}

    def add_row(self, line):
        """Add a row to the board"""
        row = len(self.lines)
        if row > self.size:
            raise ValueError("Trying to append an extra row failed!")
        #
        for col, item in enumerate(line.split()):
            self.unmarked[int(item)] = (row, col)
        #
        self.lines.append(line)

    def mark(self, number):
        """Mark the number and check for Bingo"""
        try:
            position = self.unmarked.pop(number)
        except KeyError:
            return
        #
        self.marked[position] = number
        self.check_full(position, self.index_row)
        self.check_full(position, self.index_col)

    def check_full(self, position, index):
        """Raise Bingo if the row (index == 0)
        or the column (index == 1) including the position
        is fully marked
        """
        for counter in range(self.size):
            search = [counter, counter]
            search[index] = position[index]
            if tuple(search) not in self.marked:
                break
            #
        else:
            raise Bingo
        #


def build_game(reader):
    """Build the game:
    Return the list of drawn numbers and the list of Bingo boards
    """
    drawn_numbers = []
    boards = []
    current_board = None
    for line in reader.lines(skip_empty=False):
        if drawn_numbers:
            if line:
                current_board.add_row(line)
                if len(current_board.lines) == Board.size:
                    boards.append(current_board)
                    current_board = None
                #
            else:
                current_board = Board()
            #
        else:
            drawn_numbers = [int(item) for item in line.split(',')]
        #
    #
    return drawn_numbers, boards


@helpers.timer
def part1(reader):
    """Part 1"""
    drawn_numbers, boards = build_game(reader)
    for number in drawn_numbers:
        for current_board in boards:
            try:
                current_board.mark(number)
            except Bingo:
                return number * sum(current_board.unmarked)
            #
        #
    #


@helpers.timer
def part2(reader):
    """Part 2"""
    drawn_numbers, boards = build_game(reader)
    all_boards = set(boards)
    had_bingo = set()
    for number in drawn_numbers:
        for current_board in boards:
            if current_board in had_bingo:
                continue
            #
            try:
                current_board.mark(number)
            except Bingo:
                had_bingo.add(current_board)
                if all_boards == had_bingo:
                    return number * sum(current_board.unmarked)
                #
            #
        #
    #


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
