# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 22
"""

import unittest

import helpers
import day22 as current_day


DAY = 22

EXAMPLE_RESULTS = 590784, 2758514936282235
PUZZLE_RESULTS = 537042, None

TESTED_FUNCTIONS = current_day.part1, current_day.part2

EXAMPLE_FILE = f"inputs/{DAY}.example"
EXAMPLE_FILE_2 = f"inputs/{DAY}.example2"
PUZZLE_FILE = f"inputs/{DAY}.txt"


class TestExample1(unittest.TestCase, helpers.TestMixin):

    """Day 22: Test solutions using the example"""

    reader = helpers.Reader(file_name=EXAMPLE_FILE)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 22: Test part 1 with example data"""
        self.do_equality_test(0)


class TestExample2(unittest.TestCase, helpers.TestMixin):

    """Day 22: Test solutions using the example"""

    reader = helpers.Reader(ffile_name=EXAMPLE_FILE_2)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_2(self):
        """Day 22: Test part 2 with example data"""
        self.do_equality_test(1)


class TestPuzzle(unittest.TestCase, helpers.TestMixin):

    """Day 22: Test solutions using the puzzle"""

    reader = helpers.Reader(file_name=PUZZLE_FILE)
    results = PUZZLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 22: Test part 1 with puzzle data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 22: Test part 2 with puzzle data"""
        self.do_equality_test(1)
