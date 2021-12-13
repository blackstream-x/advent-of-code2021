# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 12
"""

import unittest

import helpers
import day12 as current_day


DAY = 12

EXAMPLE_RESULTS = 10, 36
EXAMPLE2_RESULTS = 19, 103
EXAMPLE3_RESULTS = 226, 3509
PUZZLE_RESULTS = 3495, 94849

TESTED_FUNCTIONS = current_day.part1, current_day.part2

EXAMPLE_FILE = f"inputs/{DAY}.example"
EXAMPLE2_FILE = f"inputs/{DAY}.example2"
EXAMPLE3_FILE = f"inputs/{DAY}.example3"
PUZZLE_FILE = f"inputs/{DAY}.txt"


class TestExample(unittest.TestCase, helpers.TestMixin):

    """Day 12: Test solutions using the example"""

    reader = helpers.Reader(file_name=EXAMPLE_FILE)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 12: Test part 1 with example data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 12: Test part 2 with example data"""
        self.do_equality_test(1)


class TestExample2(TestExample):

    """Day 12: Test solutions using the example #2"""

    reader = helpers.Reader(file_name=EXAMPLE2_FILE)
    results = EXAMPLE2_RESULTS


class TestExample3(TestExample):

    """Day 12: Test solutions using the example #3"""

    reader = helpers.Reader(file_name=EXAMPLE3_FILE)
    results = EXAMPLE3_RESULTS


class TestPuzzle(unittest.TestCase, helpers.TestMixin):

    """Day 12: Test solutions using the puzzle"""

    reader = helpers.Reader(file_name=PUZZLE_FILE)
    results = PUZZLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 12: Test part 1 with puzzle data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 12: Test part 2 with puzzle data"""
        self.do_equality_test(1)
