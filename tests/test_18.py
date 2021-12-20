# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 18
"""

import unittest

import helpers
import day18 as current_day


DAY = 18

EXAMPLE_RESULTS = 4140, 3993
PUZZLE_RESULTS = 4057, 4683

TESTED_FUNCTIONS = current_day.part1, current_day.part2

EXAMPLE_FILE = f"inputs/{DAY}.example"
PUZZLE_FILE = f"inputs/{DAY}.txt"


class TestExample(unittest.TestCase, helpers.TestMixin):

    """Day 18: Test solutions using the example"""

    reader = helpers.Reader(file_name=EXAMPLE_FILE)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 18: Test part 1 with example data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 18: Test part 2 with example data"""
        self.do_equality_test(1)


class TestFunctions(unittest.TestCase):

    """Day 18: Test partial functionality"""

    def test_reduce(self):
        """Day 18: Test snailfish number reductions"""
        for (sfn, expected_sfn) in current_day.EXPLODE_TESTS.items():
            sf_number = current_day.SnailfishNumber.from_string(sfn)
            sf_number.reduce()
            self.assertEqual(str(sf_number), expected_sfn)
        #

    def test_magnitude(self):
        """Day 18: Test snailfish number magnitudes"""
        for (sfn, expected_magnitude) in current_day.MAGNITUDE_TESTS.items():
            self.assertEqual(
                current_day.SnailfishNumber.from_string(sfn).magnitude,
                expected_magnitude,
            )
        #


class TestPuzzle(unittest.TestCase, helpers.TestMixin):

    """Day 18: Test solutions using the puzzle"""

    reader = helpers.Reader(file_name=PUZZLE_FILE)
    results = PUZZLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 18: Test part 1 with puzzle data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 18: Test part 2 with puzzle data"""
        self.do_equality_test(1)
