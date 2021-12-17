#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 16
blackstream-x’ solution
"""


import functools
import logging
import operator

import helpers


AGGREGATES = (
    sum,
    operator.mul,
    min,
    max,
    None,
    operator.gt,
    operator.lt,
    operator.eq,
)

TYPE_SUM = 0
TYPE_PRODUCT = 1
TYPES_MINMAX = (2, 3)
TYPE_DATA = 4
TYPES_COMPARISON = (5, 6, 7)


class Packet:

    """Packet base class"""

    allowed_type_ids = ()
    expect_bits = 0

    def __init__(self, version, type_id):
        """Check if the given type ID matches the package type"""
        if type_id not in self.allowed_type_ids:
            raise ValueError(
                f"Type ID {type_id} not allowed for {self.__class__.__name__}!"
            )
        #
        self.version = version
        self.type_id = type_id
        logging.debug("Initialized %r", self)

    def check_input(self, bits):
        """Check input if the expected number of bits was supplied"""
        if self.expect_bits is not None and len(bits) != self.expect_bits:
            raise ValueError(f"Expecting exactly {self.expect_bits} bits!")
        #
        if not bits:
            raise ValueError("Empty input!")
        #
        logging.debug("Processing bit(s): %r", bits)

    def get_versions_sum(self):
        """Return the version number"""
        return self.version

    def __repr__(self):
        """String representation"""
        return (
            f"{self.__class__.__name__}(version={self.version},"
            f" type_id={self.type_id})"
        )


class DataPacket(Packet):

    """Data packet"""

    allowed_type_ids = (TYPE_DATA,)
    expect_bits = 5

    def __init__(self, version, type_id):
        """Store hex and decimal values"""
        super().__init__(version, type_id)
        self.hex_value = ""
        self.literal_value = None

    @property
    def value(self):
        """Return the literal value"""
        return self.literal_value

    def parse(self, bits):
        """Parse exactly 5 bits and return the number of
        remaining unparsed bits (always zero)
        """
        self.check_input(bits)
        self.hex_value += bits2hex(bits[1:])
        if bits[0] == "0":
            self.literal_value = int(self.hex_value, 16)
            logging.debug(
                "Literal value: %r -> %s",
                self.hex_value,
                self.literal_value,
            )
            self.expect_bits = 0
        #
        return 0


class OperatorPacket(Packet):

    """Operator packet"""

    allowed_type_ids = (
        TYPE_SUM,
        TYPE_PRODUCT,
        *TYPES_MINMAX,
        *TYPES_COMPARISON,
    )
    expect_bits = 1

    def __init__(self, version, type_id):
        """Store subpackets and control parameters"""
        super().__init__(version, type_id)
        self.length_type_id = None
        self.subpackets_length = None
        self.subpackets_number = None
        self.subpackets = []

    @property
    def value(self):
        """Return the value computed from the subpackets"""
        subpacket_values = [subpacket.value for subpacket in self.subpackets]
        func = AGGREGATES[self.type_id]
        if self.type_id == TYPE_PRODUCT:
            # Chain multiplication
            return functools.reduce(func, subpacket_values, 1)
        #
        if self.type_id in TYPES_COMPARISON:
            return int(func(*subpacket_values))
        #
        # Remaining types: sum, min and max
        return func(subpacket_values)

    def get_versions_sum(self):
        """Return the own version number,
        plus the version sums of all subpackets
        """
        return self.version + sum(
            subpacket.get_versions_sum() for subpacket in self.subpackets
        )

    def parse(self, bits):
        """Parse bits and return the number of
        remaining unparsed bits (only relevant
        if the number of bits to parse is undetermined,
        ie. when a certain number of subpackets is expected).
        """
        self.check_input(bits)
        if self.length_type_id is None:
            self.length_type_id = bits2dec(bits[0])
            if self.length_type_id:
                self.expect_bits = 11
            else:
                self.expect_bits = 15
            #
        elif self.subpackets_length:
            for remaining_bits, packet in parse_substring(bits):
                self.subpackets.append(packet)
            #
            self.expect_bits = 0
        elif self.subpackets_number:
            unparsed_bits = 0
            for remaining_bits, packet in parse_substring(
                bits, max_packets=self.subpackets_number - len(self.subpackets)
            ):
                self.subpackets.append(packet)
                unparsed_bits = remaining_bits
            #
            self.expect_bits = 0
            return unparsed_bits
        else:
            number = int(bits, 2)
            if len(bits) == 11:
                self.subpackets_number = number
                self.expect_bits = None
                logging.debug("Expecting %s subpackets", number)
            elif len(bits) == 15:
                self.subpackets_length = number
                self.expect_bits = number
                logging.debug("Expecting %s bits of subpacket data", number)
            #
        #
        return 0


def bits2dec(bits):
    """Bits to decimal"""
    return int(bits, 2)


def bits2hex(bits):
    """Bits to hex"""
    return hex(bits2dec(bits))[2:]


def hex2bits(hexdigit):
    """return hexdigit converted to a string representation
    of 4 bits binary, left-padded with zeros
    """
    return f"{bin(int(hexdigit, 16))[2:]:>04s}"


def parse_substring(bits, max_packets=None):
    """parse the bit string. Yield maximum max_packets."""
    packets = 0
    index = 0
    while True:
        if len(bits[index:index + 6]) < 6:
            logging.debug("End of stream, no more data to read.")
            break
        #
        version = bits2dec(bits[index:index + 3])
        type_id = bits2dec(bits[index + 3:index + 6])
        if type_id == TYPE_DATA:
            packet = DataPacket(version, type_id)
        else:
            packet = OperatorPacket(version, type_id)
        #
        index = index + 6
        digits = packet.expect_bits
        while digits or digits is None:
            if digits is None:
                unparsed_bits = packet.parse(bits[index:])
                index = len(bits) - unparsed_bits
            else:
                packet.parse(bits[index:index + digits])
                index = index + digits
            #
            digits = packet.expect_bits
        #
        yield (len(bits) - index, packet)
        packets += 1
        if max_packets is None:
            continue
        #
        if packets >= max_packets:
            break
        #
    #


def parse(transmission):
    """Parse an encoded string.
    Return the outermost packet.
    """
    logging.debug("=" * 70)
    logging.debug(transmission)
    bits = ""
    for hexdigit in transmission:
        bits += hex2bits(hexdigit)
    #
    logging.debug("-" * 70)
    logging.debug(bits)
    logging.debug("-" * 70)
    for remaining_bits, packet in parse_substring(bits, max_packets=1):
        if remaining_bits:
            logging.debug("Remaining bits at end: %r", bits[-remaining_bits:])
        #
        return packet
    #


@helpers.timer
def part1(reader):
    """Part 1"""
    result = 0
    for line in reader.lines():
        packet = parse(line)
        versions_sum = packet.get_versions_sum()
        logging.debug("Versions sum: %r", versions_sum)
        result += versions_sum
    #
    return result


@helpers.timer
def part2(reader):
    """Part 2"""
    for line in reader.lines():
        packet = parse(line)
        return packet.value
    #


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
