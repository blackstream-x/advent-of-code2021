#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 3
blackstream-x’ solution
"""


import helpers


ONE = "1"
ZERO = "0"


def most_and_least_common(report_values):
    """Return most and least common values from the given report
    by index
    """
    most_common = []
    least_common = []
    for column in zip(*report_values):
        ones, zeroes = column.count(ONE), column.count(ZERO)
        if zeroes > ones:
            most, least = ZERO, ONE
        else:
            most, least = ONE, ZERO
        #
        most_common.append(most)
        least_common.append(least)
    #
    return (most_common, least_common)


def filter_values(report_values, index, keep):
    """Yield only the values where current_value[index] == keep"""
    for current_value in report_values:
        if current_value[index] == keep:
            yield current_value
        #
    #


def filter_from_report(reader, position):
    """Return the item matching the most (0) or least (1) common bits
    in each index
    """
    report_values = list(reader.lines())
    diag_length = len(report_values[0])
    for index in range(diag_length):
        commons = most_and_least_common(report_values)
        report_values = list(
            filter_values(report_values, index, commons[position][index])
        )
        if len(report_values) > 1:
            continue
        #
        return "".join(report_values.pop())
    #
    raise ValueError(
        f"#{position} not found, remaining values: {report_values!r}!"
    )


@helpers.timer
def part1(reader):
    """Part 1"""
    [gamma, epsilon] = [
        "".join(values)
        for values in most_and_least_common(list(reader.lines()))
    ]
    gamma_dec, epsilon_dec = int(gamma, 2), int(epsilon, 2)
    print(f"Gamma: {gamma} => {gamma_dec}")
    print(f"Epsilon: {epsilon} => {epsilon_dec}")
    return gamma_dec * epsilon_dec


@helpers.timer
def part2(reader):
    """Part 2"""
    [oxy_gen, co2_scrub] = [
        filter_from_report(reader, position) for position in range(2)
    ]
    oxy_gen_dec, co2_scrub_dec = int(oxy_gen, 2), int(co2_scrub, 2)
    print(f"Oxygen genrator: {oxy_gen} => {oxy_gen_dec}")
    print(f"CO2 scrubber: {co2_scrub} => {co2_scrub_dec}")
    return oxy_gen_dec * co2_scrub_dec


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
