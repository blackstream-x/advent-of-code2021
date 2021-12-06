#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day x
blackstream-x’ solution
"""


import logging

import helpers


SPAWN_PERIOD = 7
NEW_FISH = 8


def spawn_days(initial_count, days):
    """Return a list of days when a fish with initial_count spawns,
    zero-based
    """
    return list(range(initial_count + 1, days + 1, SPAWN_PERIOD))


def population_after(days, fishes):
    """Return the population count after {days} days"""
    population = len(fishes)
    spawn_events = [None] + [0] * days
    for fish in fishes:
        for day in spawn_days(fish, days):
            spawn_events[day] += 1
        #
    #
    for day in range(1, days + 1):
        new_fish = spawn_events[day]
        logging.debug("Day #%s: %s spawned", day, new_fish)
        new_spawns = spawn_days(NEW_FISH, days - day)
        for new_day in new_spawns:
            future_day = day + new_day
            spawn_events[future_day] += new_fish
        #
        population += new_fish
    #
    return population


@helpers.timer
def part1(reader):
    """Part 1"""
    test_days = 18
    days = 80
    for line in reader.lines():
        fishes = [int(item) for item in line.split(",")]
        logging.debug(
            "Population after %s days: %s",
            test_days,
            population_after(test_days, fishes),
        )
        return population_after(days, fishes)
    #


@helpers.timer
def part2(reader):
    """Part 2"""
    test_days = 18
    days = 256
    for line in reader.lines():
        fishes = [int(item) for item in line.split(",")]
        logging.debug(
            "Population after %s days: %s",
            test_days,
            population_after(test_days, fishes),
        )
        return population_after(days, fishes)
    #


if __name__ == "__main__":
    READER = helpers.initialize_puzzle()
    print(part1(READER))
    print(part2(READER))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
