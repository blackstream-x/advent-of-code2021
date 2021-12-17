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
        """Keep the original template,
        create a (default-)dict of elements pairs’ frequencies
        and a rules dict
        """
        self.template = template
        self.frequencies = collections.defaultdict(int)
        self.rules = {}

    def add_rule(self, line):
        """Add a new rule parsed from the line"""
        raw_pair, raw_new_element = line.split("->")
        self.rules[tuple(raw_pair.strip())] = raw_new_element.strip()

    def step(self):
        """Execute one step.
        For each existing elements pair (first element, second element),
        insert a new element according to the rule for that pair.
        This will increase the frequency of
        (first element, new element) and (new element, second element)
        *each* by the previous frequency of (first element, second element).
        """
        new_frequencies = collections.defaultdict(int)
        for elements_pair, frequency in self.frequencies.items():
            try:
                new_element = self.rules[elements_pair]
            except KeyError:
                logging.debug("No rule for elements pair %r!", elements_pair)
                new_frequencies[elements_pair] += frequency
            else:
                element_before, element_after = elements_pair
                for new_pair in (
                    (element_before, new_element),
                    (new_element, element_after),
                ):
                    new_frequencies[new_pair] += frequency
                #
            #
        #
        self.frequencies = new_frequencies

    def execute_steps(self, number):
        """Initialize frequencies,
        Execute number steps and log the frequencies
        """
        for index, element in enumerate(self.template):
            if index:
                elements_pair = (self.template[index - 1], element)
                self.frequencies[elements_pair] += 1
            #
        #
        for step_no in range(1, number + 1):
            self.step()
            logging.debug("After step %s: %s", step_no, self.frequencies)
        #

    def get_elements_frequencies(self):
        """Return a dict with element frequencies.
        Double count frequencies first, then half the numbers.
        Add one to the first and last elements before counting
        as they are counted only once, in contrast to the
        elements which are in the middle of the chain,
        which are part of two combinationss each.
        """
        double_counted_frequencies = collections.defaultdict(int)
        for index in (0, -1):
            double_counted_frequencies[self.template[index]] = 1
        #
        for elements_pair, frequency in self.frequencies.items():
            for element in elements_pair:
                double_counted_frequencies[element] += frequency
            #
        #
        return {
            element: double_frequency // 2
            for element, double_frequency in double_counted_frequencies.items()
        }


def frequency_difference_after(number_of_steps, reader):
    """Return the frequency difference after number_of_steps"""
    for line in reader.lines():
        try:
            counter.add_rule(line)
        except NameError:
            counter = PolimerizationCounter(line)
        #
    #
    counter.execute_steps(number_of_steps)
    elements_frequencies = sorted(counter.get_elements_frequencies().values())
    return elements_frequencies[-1] - elements_frequencies[0]


@helpers.timer
def part1(reader):
    """Part 1"""
    return frequency_difference_after(10, reader)


@helpers.timer
def part2(reader):
    """Part 2"""
    return frequency_difference_after(40, reader)


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
