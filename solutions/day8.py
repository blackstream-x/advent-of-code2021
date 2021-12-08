#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 8
blackstream-x’ solution
"""


import logging

import helpers


def all_combinations(letter_sequences):
    """Return all possible combinations of the sequences
    as a list of strings
    """
    sequences = list(letter_sequences)
    output = []
    while sequences:
        combination = sequences.pop(0)
        if output:
            previous_output = output
        else:
            previous_output = [""]
        #
        output = [
            f"{stub}{letter}"
            for letter in combination
            for stub in previous_output
        ]
    #
    return output


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
        """Initalize lookup collections"""
        self.digits = {}
        self.target_wires = []
        for (index, wires) in enumerate(self.regular_display):
            self.digits[wires] = index
            split_wire = frozenset(wires)
            self.target_wires.append(split_wire)
        #
        self.translation_table = {}

    def learn(self, mixed_up_wires):
        """Learn how mixed up wires have to be reconnected"""
        logging.debug("--- Learning... ---")
        translation_table = {}
        possible_results = {}
        possible_translations = {}
        for wires in mixed_up_wires:
            candidates = [
                target for target in self.regular_display
                if len(target) == len(wires)
            ]
            possible_results[wires] = set(candidates)
        #
        found_matches = {}
        for wires, results in possible_results.items():
            if len(results) == 1:
                found_result = results.pop()
                for wire_id in wires:
                    possible_translations[wire_id] = set(found_result)
                #
                found_matches[wires] = found_result
            #
        #
        knowledge_increased = bool(found_matches)
        while knowledge_increased:
            logging.debug("--- Starting a new cycle")
            knowledge_increased = False
            safe_translations = set()
            # reduce possible translations
            for (wire_id, translations) in possible_translations.items():
                if len(translations) < 2:
                    continue
                #
                # Match against found_matches
                for wires, results in found_matches.items():
                    for translated_id in list(translations):
                        if (wire_id in wires) != (translated_id in results):
                            translations.remove(translated_id)
                        #
                    #
                #
                if len(translations) == 1:
                    translated_value = list(translations)[0]
                    translation_table[wire_id] = translated_value
                    knowledge_increased = True
                    logging.debug(
                        "Found translation: %r => %r!",
                        wire_id, translated_value
                    )
                #
            #
            # Try to find new matches using the translation table
            for wires, results in possible_results.items():
                #
                # Try all possible translations
                result_li = []
                for wire_id in wires:
                    result_li.append(possible_translations[wire_id])
                #
                all_possible_combinations = [
                    frozenset(combination)
                    for combination in all_combinations(result_li)
                    if frozenset(combination) in self.target_wires
                ]
                for s_result in set(results):
                    if frozenset(s_result) not in all_possible_combinations:
                        results.remove(s_result)
                    #
                #
                if len(results) == 1:
                    found_matches[wires] = results.pop()
                    knowledge_increased = True
                    safe_translations.add(wires)
                    logging.debug(
                        "Found translation: %r => %r!",
                        wires, found_matches[wires]
                    )
                #

            #
            for safe_t in safe_translations:
                possible_results.pop(safe_t, None)
            #
        #
        self.translation_table = str.maketrans(
            {key: value.pop() for key, value in possible_translations.items()}
        )

    def translate(self, item):
        """Return a digit as str"""
        return str(
            self.digits[
                "".join(
                    sorted(frozenset(item.translate(self.translation_table)))
                )
            ]
        )


@helpers.timer
def part1(reader):
    """Part 1"""
    result = 0
    wire_mapper = WireMapper()
    requested_digit_lengths = [
        len(wires) for wires, index in wire_mapper.digits.items()
        if index in (1, 4, 7, 8)
    ]
    for line in reader.lines():
        rules, display = line.split("|", 1)
        result += len(
            [
                digit for digit in display.split()
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
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
