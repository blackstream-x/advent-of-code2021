# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 11
"""

import unittest

import helpers
import day11 as current_day


DAY = 11

EXAMPLE_RESULTS = 1656, 195
PUZZLE_RESULTS = 1755, 212

TESTED_FUNCTIONS = current_day.part1, current_day.part2

EXAMPLE_FILE = f"inputs/{DAY}.example"
PUZZLE_FILE = f"inputs/{DAY}.txt"


class TestExample(unittest.TestCase, helpers.TestMixin):

    """Day 11: Test solutions using the example"""

    reader = helpers.Reader(file_name=EXAMPLE_FILE)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 11: Test part 1 with example data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 11: Test part 2 with example data"""
        self.do_equality_test(1)


class TestPuzzle(unittest.TestCase, helpers.TestMixin):

    """Day 11: Test solutions using the puzzle"""

    reader = helpers.Reader(file_name=PUZZLE_FILE)
    results = PUZZLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 11: Test part 1 with puzzle data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 11: Test part 2 with puzzle data"""
        self.do_equality_test(1)

