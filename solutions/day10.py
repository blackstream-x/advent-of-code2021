#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 10
blackstream-x’ solution
"""


import logging

import helpers


OPENERS = "([{<"
CLOSERS = ")]}>"

EXPECTED_CLOSER = {
    opener: CLOSERS[index] for index, opener in enumerate(OPENERS)
}

ERROR_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

AUTOCOMPLETION_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

def first_error_char(line):
    """Return the first error character in the line"""
    stack = []
    for char in line:
        if char in OPENERS:
            stack.append(EXPECTED_CLOSER[char])
        elif char in CLOSERS:
            try:
                expected = stack.pop()
            except IndexError:
                logging.debug(
                    "Expected any of %r, but found %r instead",
                    OPENERS, char
                )
                return char
            #
            if char != expected:
                logging.debug(
                    "Expected %r, but found %r instead",
                    expected, char
                )
                return char
            #
        #
    #
    raise ValueError


def completion_score(line):
    """Return the completion score for an incomplete line"""
    stack = []
    for char in line:
        if char in OPENERS:
            stack.append(EXPECTED_CLOSER[char])
        elif char in CLOSERS:
            try:
                expected = stack.pop()
            except IndexError as error:
                logging.debug(
                    "Expected any of %r, but found %r instead",
                    OPENERS, char
                )
                raise ValueError from error
            #
            if char != expected:
                logging.debug(
                    "Expected %r, but found %r instead",
                    expected, char
                )
                raise ValueError
            #
        #
    #
    if not stack:
        # Complete line
        raise ValueError
    #
    score = 0
    logging.debug("Autocompleting: %s", "".join(reversed(stack)))
    while stack:
        score = score * 5 + AUTOCOMPLETION_SCORES[stack.pop()]
    #
    logging.debug("Score is %s", score)
    return score


@helpers.timer
def part1(reader):
    """Part 1"""
    errors = {}
    for line in reader.lines():
        try:
            error_char = first_error_char(line)
        except ValueError:
            continue
        #
        errors.setdefault(error_char, 0)
        errors[error_char] += 1
    #
    return sum(ERROR_SCORES[char] * count for char, count in errors.items())


@helpers.timer
def part2(reader):
    """Part 2"""
    scores = []
    for line in reader.lines():
        try:
            scores.append(completion_score(line))
        except ValueError:
            continue
        #
    #
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
