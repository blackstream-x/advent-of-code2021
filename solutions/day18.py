#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 18
blackstream-x’ solution
"""


import logging
import math

import helpers


FIRST = 0
SECOND = 1

EXPLODE_TESTS = {
    "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
    "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
}

MAGNITUDE_TESTS = {
    "[[1,2],[[3,4],5]]": 143,
    "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]": 1384,
    "[[[[1,1],[2,2]],[3,3]],[4,4]]": 445,
    "[[[[3,0],[5,3]],[4,4]],[5,5]]": 791,
    "[[[[5,0],[7,4]],[5,5]],[6,6]]": 1137,
    "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]": 3488,
}


class Pair:

    """Pair of any combination of regular numbers or pairs"""

    def __init__(self, first, second):
        """Set the pair"""
        self.__pair = [first, second]

    def __getitem__(self, index):
        """Return first or second"""
        if index not in (FIRST, SECOND):
            raise IndexError
        #
        return self.__pair[index]

    def __mul__(self, other):
        """Return the own magnitude multiblied with other"""
        return self.magnitude * other

    __rmul__ = __mul__

    def __setitem__(self, index, value):
        """Set first or second"""
        if index not in (FIRST, SECOND):
            raise IndexError
        #
        self.__pair[index] = value

    def __str__(self):
        """Return the string representation"""
        return f"[{str(self[FIRST])},{str(self[SECOND])}]"

    @classmethod
    def from_string(cls, source):
        """Generate a pair from the source string"""
        first = None
        second = None
        collected = ""
        level = 0
        if source[0] == "[" and source[-1] == "]":
            for char in source[1:-1]:
                if char == "," and not level:
                    try:
                        first = int(collected)
                    except ValueError:
                        first = cls.from_string(collected)
                    #
                    collected = ""
                    continue
                #
                collected += char
                if char == "[":
                    level += 1
                elif char == "]":
                    level -= 1
                #
            #
            try:
                second = int(collected)
            except ValueError:
                second = cls.from_string(collected)
            #
            return cls(first, second)
        #
        raise ValueError(f"Cannot determine a pair from {source!r}!")

    @property
    def magnitude(self):
        """Return the pair’s magnitude:
        3 * the first plus 2 * the second itme’s magnitude
        """
        return self[FIRST] * 3 + self[SECOND] * 2

    def copy(self):
        """Return a copy of the tree"""
        copied = []
        for index in [FIRST, SECOND]:
            item = self[index]
            if isinstance(item, Pair):
                copied.append(item.copy())
            else:
                copied.append(item)
            #
        #
        return Pair(copied[FIRST], copied[SECOND])

    def iter_pairs(self):
        """Iterate through all pairs"""
        for index in [FIRST, SECOND]:
            item = self[index]
            yield [index], item
            if isinstance(item, Pair):
                for (path, value) in item.iter_pairs():
                    yield [index] + path, value
                #
            #
        #


class SnailfishNumber:

    """Snailfish number"""

    def __init__(self, pair):
        """Set the root pair"""
        self.pair = pair

    def __str__(self):
        """Return the string representation"""
        return str(self.pair)

    def __add__(self, other):
        """Return a new number.
        Reduce both numbers before adding.
        Te resulting number still has to be reduced!
        """
        self.reduce()
        other.reduce()
        new_pair = Pair(self.pair.copy(), other.pair.copy())
        return SnailfishNumber(new_pair)

    @classmethod
    def from_string(cls, source):
        """Generate a SnailfishNumber from the source string"""
        return cls(Pair.from_string(source))

    @property
    def magnitude(self):
        """Return the pair’s magnitude"""
        return self.pair.magnitude

    def direct_access(self, path):
        """Walk down the tree using all items in path"""
        walk_path = list(path)
        result = self.pair
        while walk_path:
            result = result[walk_path.pop(0)]
        #
        return result

    def iter_pairs(self):
        """Iterate through all pairs"""
        for (path, value) in self.pair.iter_pairs():
            yield path, value
        #

    def get_explode_data(self):
        """Return a numbers sequence of (path, value) pairs
        and a flag explode_required
        """
        numbers = []
        explode_required = None
        for path, value in self.pair.iter_pairs():
            logging.debug("%r: %s", path, value)
            if isinstance(value, int):
                numbers.append((path, value))
            elif len(path) > 3 and not explode_required:
                explode_required = path
                logging.debug("Explode required: %r", path)
            #
        #
        return numbers, explode_required

    @staticmethod
    def get_last_number(numbers, exploded_path):
        """Return the path and value of the last number
        or raise an IndexError
        """
        previous_numbers = [
            (path, value) for (path, value) in numbers if path < exploded_path
        ]
        return previous_numbers[-1]

    @staticmethod
    def get_next_number(numbers, exploded_path):
        """Return the path and value of the next number
        or raise an IndexError
        """
        next_numbers = [
            (path, value)
            for (path, value) in numbers
            if path > exploded_path
            and path[: len(exploded_path)] != exploded_path
        ]
        return next_numbers[0]

    def reduce(self):
        """Reduce the number: explode pairs if required,
        split big numbers if required
        """
        numbers, explode_required = self.get_explode_data()
        exploded = True
        splitted = False
        while exploded or splitted:
            exploded = False
            splitted = False
            if explode_required:
                exploded_pair = self.direct_access(explode_required)
                logging.debug(
                    "Exploding %s (%s)", explode_required, exploded_pair
                )
                parent_path = explode_required[:-1]
                last_index = explode_required[-1]
                # propagate first item backwards
                try:
                    last_number_path, value = self.get_last_number(
                        numbers, explode_required
                    )
                except IndexError:
                    logging.debug("No previous regular number")
                else:
                    logging.debug(
                        "Propagating backward to %s", last_number_path
                    )
                    ln_index = last_number_path[-1]
                    self.direct_access(last_number_path[:-1])[ln_index] = (
                        value + exploded_pair[FIRST]
                    )
                #
                # propagate second item forwards
                try:
                    next_number_path, value = self.get_next_number(
                        numbers, explode_required
                    )
                except IndexError:
                    logging.debug("No followup regular number")
                else:
                    logging.debug(
                        "Propagating forward to %s", next_number_path
                    )
                    nn_index = next_number_path[-1]
                    self.direct_access(next_number_path[:-1])[nn_index] = (
                        value + exploded_pair[SECOND]
                    )
                #
                self.direct_access(parent_path)[last_index] = 0
                exploded = True
                numbers, explode_required = self.get_explode_data()
                continue
            #
            for (path, value) in numbers:
                if value > 9:
                    logging.debug("Splitting %s...", path)
                    last_index = path[-1]
                    self.direct_access(path[:-1])[last_index] = Pair(
                        value // 2, math.ceil(value / 2)
                    )
                    splitted = True
                    numbers, explode_required = self.get_explode_data()
                    break
                #
            #
        #


@helpers.timer
def part1(reader):
    """Part 1"""
    result = None
    for line in reader.lines():
        if result is None:
            result = SnailfishNumber.from_string(line)
        else:
            result = result + SnailfishNumber.from_string(line)
    #
    result.reduce()
    return result.magnitude


@helpers.timer
def part2(reader):
    """Part 2"""
    result = 0
    sfns = []
    for line in reader.lines():
        csfn = SnailfishNumber.from_string(line)
        sfns.append(csfn)
    #
    for index1, sfn1 in enumerate(sfns):
        for index2, sfn2 in enumerate(sfns):
            if index1 == index2:
                continue
            #
            sum_of_two = sfn1 + sfn2
            sum_of_two.reduce()
            sot_magnitude = sum_of_two.magnitude
            if sot_magnitude > result:
                result = sot_magnitude
            #
            result = max(result, sum_of_two.magnitude)
        #
    #
    return result


@helpers.timer
def reduction_tests():
    """Test SnailfishNumber reductions"""
    print("Testing Reductions")
    for (sfn, expected_result) in EXPLODE_TESTS.items():
        s_number = SnailfishNumber.from_string(sfn)
        s_number.reduce()
        if str(s_number) == expected_result:
            state = "✔"
        else:
            state = "✘"
        #
        print(f"{state} {sfn} => {s_number}")
    #


@helpers.timer
def magnitude_tests():
    """Test magnitude calculation"""
    print("Testing Magnitude calcuation…")
    for (sfn, expected_magnitude) in MAGNITUDE_TESTS.items():
        s_number = SnailfishNumber.from_string(sfn)
        if s_number.magnitude == expected_magnitude:
            state = "✔"
        else:
            state = "✘"
        #
        print(f"{state} {s_number}: {s_number.magnitude}")
    #


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
