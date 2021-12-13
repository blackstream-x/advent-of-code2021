# -*- coding: utf-8 -*-

"""
Test Advent of Code solutions for day 4
"""

import unittest

import helpers
import day4 as proposed_solution


DAY = 4

PART_1_EXAMPLE_RESULT = 4512
PART_2_EXAMPLE_RESULT = 1924

PART_1_PUZZLE_RESULT = 58374
PART_2_PUZZLE_RESULT = 11377


class TestExample(unittest.TestCase):

    """Test solutions using the example"""

    example_reader = helpers.Reader(file_name=f"inputs/{DAY}.example")

    def test_part_1_example(self):
        """Test part 1 with example data"""
        self.assertEqual(
            proposed_solution.part1(self.example_reader), PART_1_EXAMPLE_RESULT
        )

    def test_part_2_example(self):
        """Test part 2 with example data"""
        if PART_2_EXAMPLE_RESULT is None:
            self.skipTest("Expected result not specified")
        #
        self.assertEqual(
            proposed_solution.part2(self.example_reader), PART_2_EXAMPLE_RESULT
        )


class TestPuzzle(unittest.TestCase):

    """Test solutions using the puzzle"""

    puzzle_reader = helpers.Reader(file_name=f"inputs/{DAY}.txt")

    def test_part_1_puzzle(self):
        """Test part 1 with puzzle data"""
        if PART_1_PUZZLE_RESULT is None:
            self.skipTest("Expected result not specified")
        #
        self.assertEqual(
            proposed_solution.part1(self.puzzle_reader), PART_1_PUZZLE_RESULT
        )

    def test_part_2_puzzle(self):
        """Test part 2 with puzzle data"""
        if PART_2_PUZZLE_RESULT is None:
            self.skipTest("Expected result not specified")
        #
        self.assertEqual(
            proposed_solution.part2(self.puzzle_reader), PART_2_PUZZLE_RESULT
        )
