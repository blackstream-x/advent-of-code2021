# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 16
"""

import unittest

import helpers
import day16 as current_day


DAY = 16

EXAMPLE_RESULTS = 9 + 14 + 16 + 12 + 23 + 31, None
EXAMPLE2_DATA = {
    "C200B40A82": 3,
    "04005AC33890": 54,
    "880086C3E88112": 7,
    "CE00C43D881120": 9,
    "D8005AC2A8F0": 1,
    "F600BC2D8F": 0,
    "9C005AC2F8F0": 0,
    "9C0141080250320F1802104A08": 1,
}

PUZZLE_RESULTS = 999, 3408662834145

TESTED_FUNCTIONS = current_day.part1, current_day.part2

EXAMPLE_FILE = f"inputs/{DAY}.example"
PUZZLE_FILE = f"inputs/{DAY}.txt"


class TestExample(unittest.TestCase, helpers.TestMixin):

    """Day 16: Test solutions using the example"""

    reader = helpers.Reader(file_name=EXAMPLE_FILE)
    results = EXAMPLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 16: Test part 1 with example data"""
        self.do_equality_test(0)


class TestExample2(unittest.TestCase):

    """Day 16: Test solutions using the examples for part 2"""

    tested_functions = TESTED_FUNCTIONS

    def test_2(self):
        """Day 16: Test part 2 with example data"""
        for data, expected_result in EXAMPLE2_DATA.items():
            self.assertEqual(
                expected_result, current_day.part2(helpers.Reader(text=data))
            )
        #


class TestPuzzle(unittest.TestCase, helpers.TestMixin):

    """Day 16: Test solutions using the puzzle"""

    reader = helpers.Reader(file_name=PUZZLE_FILE)
    results = PUZZLE_RESULTS
    tested_functions = TESTED_FUNCTIONS

    def test_1(self):
        """Day 16: Test part 1 with puzzle data"""
        self.do_equality_test(0)

    def test_2(self):
        """Day 16: Test part 2 with puzzle data"""
        self.do_equality_test(1)
