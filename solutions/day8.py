#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 8
blackstream-x’ solution
"""


import itertools
import logging

import helpers


class Reducer:

    """Keep a dict of sets.
    If a set contains only one entry,
    include it in a "complete_items" view
    """

    def __init__(self):
        """Initialize internal dict"""
        self.__unclear_data = {}
        self.__complete_data = {}

    def __getitem__(self, key):
        """Return self.__complete_data[key]"""
        return self.__complete_data[key]

    def __iter__(self):
        """Return an iterator over self.__complete_data"""
        return iter(self.__complete_data)

    def complete_items(self):
        """Return complete data items"""
        return self.__complete_data.items()

    def unclear_items(self):
        """Return data items"""
        return self.__unclear_data.items()

    def is_complete(self, key):
        """Return True if the value for key is unique"""
        return key in self.__complete_data

    def __check_completeness(self, key):
        """If there is only one value in key's set,
        move that to the complete_data dict as a scalar value.
        Remove the value form the other unclear sets as well.
        """
        if len(self.__unclear_data[key]) == 1:
            self.__complete_data[key] = self.__unclear_data[key].pop()
            del self.__unclear_data[key]
            for unclear_key in list(self.__unclear_data):
                try:
                    self.reduce(unclear_key, self.__complete_data[key])
                except KeyError:
                    continue
                #
            #
        #

    def update(self, key, *values):
        """Update key with values and check for completeness"""
        if key not in self.__unclear_data:
            self.__unclear_data[key] = self.__complete_data.pop(key, set())
        #
        self.__unclear_data[key].update(values)
        self.__check_completeness(key)

    def reduce(self, key, value):
        """Remove value from the key set and check for completeness"""
        self.__unclear_data[key].remove(value)
        self.__check_completeness(key)


class CharacterReducer(Reducer):

    """Character translation reduction class"""

    def all_matching(self, mixed_up, candidates):
        """Return a subset of candidates matching
        all possible translations using the current state
        """
        possible_characters = [
            value for key, value in self.complete_items() if key in mixed_up
        ] + [
            "".join(value)
            for key, value in self.unclear_items()
            if key in mixed_up
        ]
        combinations = 0
        result = set()
        for possible_match in itertools.product(*possible_characters):
            compare_value = "".join(
                letter for letter in sorted(possible_match)
            )
            combinations += 1
            if compare_value in candidates:
                result.add(compare_value)
            #
        #
        logging.debug(
            "%s matches from %s tried combinations", len(result), combinations
        )
        return result


class WireMapper:

    """Map mixed up wires to regular ones"""

    regular_display = (
        "abcefg",
        "cf",
        "acdeg",
        "acdfg",
        "bcdf",
        "abdfg",
        "abdefg",
        "acf",
        "abcdefg",
        "abcdfg",
    )

    def __init__(self):
        """Initalize lookup dict"""
        self.digits = {
            wires: index for (index, wires) in enumerate(self.regular_display)
        }
        self.translation_table = {}

    def learn(self, wiring_mess):
        """Learn how mixed up wires have to be reconnected.
        Set the internal translation table.
        """
        logging.debug("--- Learning... ---")
        wiring = Reducer()
        for mixed_up in wiring_mess:
            candidates = [
                candidate
                for candidate in self.regular_display
                if len(candidate) == len(mixed_up)
            ]
            wiring.update(mixed_up, *candidates)
        #
        translations = CharacterReducer()
        for mixed_up, regular in wiring.complete_items():
            for wire_id in mixed_up:
                translations.update(wire_id, *list(regular))
            #
        #
        while translations.unclear_items():
            logging.debug(" - Starting a new round")
            # reduce possible translations
            for (wire_id, tl_candidates) in list(translations.unclear_items()):
                # Match against completed wiring items
                for mixed_up, regular in wiring.complete_items():
                    for candidate_id in list(tl_candidates):
                        if (wire_id in mixed_up) != (candidate_id in regular):
                            translations.reduce(wire_id, candidate_id)
                        #
                    #
                #
                if translations.is_complete(wire_id):
                    logging.debug(
                        "Found character translation: %r => %r!",
                        wire_id,
                        translations[wire_id],
                    )
                #
            #
            # Try to find new matches using the translation table
            for mixed_up, candidates in list(wiring.unclear_items()):
                #
                if not wiring.is_complete(mixed_up):
                    # Try all possible translations
                    remaining = translations.all_matching(mixed_up, candidates)
                    for excluded_candidate in candidates - remaining:
                        wiring.reduce(mixed_up, excluded_candidate)
                    #
                #
                if wiring.is_complete(mixed_up):
                    logging.debug(
                        "Found wiring reconnection scheme: %r => %r!",
                        mixed_up,
                        wiring[mixed_up],
                    )
                #
            #
        #
        logging.debug("--- Finished learning ---")
        self.translation_table = str.maketrans(
            dict(translations.complete_items())
        )

    def translate(self, item):
        """Return a digit as str"""
        return str(
            self.digits[
                "".join(sorted(item.translate(self.translation_table)))
            ]
        )


@helpers.timer
def part1(reader):
    """Part 1"""
    result = 0
    wire_mapper = WireMapper()
    requested_digit_lengths = [
        len(wires)
        for wires, index in wire_mapper.digits.items()
        if index in (1, 4, 7, 8)
    ]
    for line in reader.lines():
        display = line.split("|", 1)[1]
        result += len(
            [
                digit
                for digit in display.split()
                if len(digit) in requested_digit_lengths
            ]
        )
    #
    return result


@helpers.timer
def part2(reader):
    """Part 2"""
    result = 0
    wire_mapper = WireMapper()
    for line in reader.lines():
        rules, display = line.split("|", 1)
        wire_mapper.learn(rules.split())
        displayed_value = "".join(
            wire_mapper.translate(item) for item in display.split()
        )
        logging.debug("Displayed value: %s", displayed_value)
        result += int(displayed_value, 10)
    #
    return result


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
