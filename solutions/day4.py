#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 4
blackstream-x’ solution
"""


import collections
import helpers


READER = helpers.Reader()

Position = collections.namedtuple('Position', ('row', 'col'))


class Bingo(Exception):

    ...


class CardComplete(Exception):

    ...


class Card:

    nb_rows = nb_cols = 5

    def __init__(self):
        self.row = 0
        self.unmarked = {}
        self.marked = {}

    def add_row(self, line):
        for col, item in enumerate(line.split()):
            self.unmarked[int(item)] = Position(self.row, col)
        #
        self.row += 1
        if self.row >= self.nb_rows:
            raise CardComplete
        #

    def mark(self, number):
        try:
            self.marked[number] = self.unmarked.pop(number)
        except KeyError:
            return
        #
        # Determine Bingo
        pos = self.marked[number]
        if self.full_row(pos.row) or self.full_col(pos.col):
            raise Bingo
        #

    def full_row(self, row):
        all_in_row = [pos for pos in self.marked.values() if pos.row == row]
        return len(all_in_row) == self.nb_cols

    def full_col(self, col):
        all_in_col = [pos for pos in self.marked.values() if pos.col == col]
        return len(all_in_col) == self.nb_rows


def build_game():
    drawn_numbers = []
    cards = []
    current_card = None
    for line in READER.lines(skip_empty=False):
        if drawn_numbers:
            if line:
                try:
                    current_card.add_row(line)
                except CardComplete:
                    cards.append(current_card)
                    current_card = None
                #
            else:
                current_card = Card()
            #
        else:
            drawn_numbers = [int(item) for item in line.split(',')]
        #
    #
    return drawn_numbers, cards


@helpers.timer
def part1():
    drawn_numbers, cards = build_game()
    for number in drawn_numbers:
        for card in cards:
            try:
                card.mark(number)
            except Bingo:
                return number * sum(card.unmarked.keys())
            #
        #
    #


@helpers.timer
def part2():
    drawn_numbers, cards = build_game()
    had_bingo = set()
    for number in drawn_numbers:
        for card in cards:
            try:
                card.mark(number)
            except Bingo:
                if card in had_bingo:
                    continue
                #
                had_bingo.add(card)
                if not set(cards) - had_bingo:
                    return number * sum(card.unmarked.keys())
                #
            #
        #
    #


if __name__ == "__main__":
    print(part1())
    print(part2())


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
