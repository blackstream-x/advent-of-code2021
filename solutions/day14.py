#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 14
blackstream-x’ solution
"""


import collections
import logging

import helpers


class PolimerizationCounter:

    """Count polimerizations"""

    def __init__(self, template):
        """Keep a dict of combination frequencies"""
        self.template = template
        self.frequencies = collections.defaultdict(int)
        self.rules = {}

    def add_rule(self, rule):
        """Add a new rule to the rules"""
        [element_pair, to_insert] = [item.strip() for item in rule.split("->")]
        self.rules[element_pair] = to_insert

    def step(self):
        """Execute one step"""
        new_frequencies = collections.defaultdict(int)
        for combination, frequency in self.frequencies.items():
            try:
                to_insert = self.rules[combination]
            except KeyError:
                logging.debug("No rule for comnination %r!", combination)
                new_frequencies[combination] += frequency
            else:
                [before, after] = list(combination)
                new_frequencies[f"{before}{to_insert}"] += frequency
                new_frequencies[f"{to_insert}{after}"] += frequency
            #
        #
        self.frequencies = new_frequencies

    def execute_steps(self, number):
        """Initialize frequencies,
        Execute number steps and log the frequencies
        """
        for index, element in enumerate(self.template):
            if index:
                elements_pair = self.template[index -1:index + 1]
                self.frequencies[elements_pair] += 1
            #
        #
        for step_no in range(1, number + 1):
            self.step()
            logging.debug(
                "After step %s: %s", step_no, self.frequencies
            )
        #

    def get_element_frequencies(self):
        """Return a dict with element frequencies"""
        # Double count frequencies first, then half the numbers.
        # Add one to the first and last element before halving
        # as they have been counted only once.
        dcf = collections.defaultdict(int)
        for index in (0, -1):
            dcf[self.template[index]] = 1
        #
        for elements_pair, frequency in self.frequencies.items():
            dcf[elements_pair[0]] += frequency
            dcf[elements_pair[1]] += frequency
        #
        element_frequencies = {}
        for element, double_frequency in dcf.items():
            element_frequencies[element] = double_frequency // 2
        #
        return element_frequencies



@helpers.timer
def part1(reader):
    """Part 1"""
    for line in reader.lines():
        try:
            counter.add_rule(line)
        except NameError:
            counter = PolimerizationCounter(line)
        #
    #
    counter.execute_steps(10)
    elements_frequencies = sorted(
        counter.get_element_frequencies().values()
    )
    return elements_frequencies[-1] - elements_frequencies[0]


@helpers.timer
def part2(reader):
    """Part 2"""
    for line in reader.lines():
        try:
            counter.add_rule(line)
        except NameError:
            counter = PolimerizationCounter(line)
        #
    #
    counter.execute_steps(40)
    elements_frequencies = sorted(
        counter.get_element_frequencies().values()
    )
    return elements_frequencies[-1] - elements_frequencies[0]


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
