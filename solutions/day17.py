#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 17
blackstream-x’ solution
"""


import logging
import math

import helpers


class Missed(Exception):

    """Raised when a shot misses the target"""

    ...


class TooFar(Missed):

    """Raised when a shot went too far (past the target)"""

    ...


class TooSteep(Missed):

    """Raised when a shot went too steep down"""

    ...


class TrajectoryCalculator:

    """Calculate the trajectory for different
    initial velocity values
    """

    expected_prefix = "target area:"

    def __init__(self, line):
        """Parse the line to get the target area coordinates.
        Set the "x factor" to 1 or -1 for x movement calculation
        """
        if not line.startswith(self.expected_prefix):
            raise ValueError(
                f"Expected input starting with {self.expected_prefix!r},"
                f"but {line!r} does not match."
            )
        #
        data = line.split(":", 1)[1].strip()
        components = [item.strip().split("=") for item in data.split(",")]
        self.target_area = {
            axis: tuple(int(value) for value in range_data.split(".."))
            for (axis, range_data) in components
        }
        start_x, end_x = self.target_area["x"]
        if start_x == abs(start_x):
            self.x_factor = 1
        else:
            self.x_factor = -1
        #
        # Determine if start and end are on the same side.
        if end_x * self.x_factor < 0:
            raise ValueError("Target area crosses Y axis!")
        #

    def minimum_x_velocity(self):
        """Return the minimum x axis velocity
        required to reach the target area
        """
        abs_start_x, abs_end_x = [
            abs(value) for value in self.target_area["x"]
        ]
        x_target = min(abs_start_x, abs_end_x)
        #
        # sum(1..x) >= x_target
        # => (x**2 + x) / 2 = x_target
        # => x**2 + x - 2 * x_target = 0
        # => applying the quadratic formula
        #    (<https://en.wikipedia.org/wiki/Quadratic_formula>):
        # x 1,2 = (-1 +- sqrt(1 + 8 * x_target)) / 2
        min_x = (math.sqrt(1 + 8 * x_target) - 1) / 2
        return math.ceil(min_x) * self.x_factor

    def minimum_x_steps(self, x_velocity):
        """Return the minimum number of steps required to
        reach the target area using the given
        x velocity
        """
        abs_start_x, abs_end_x = [
            abs(value) for value in self.target_area["x"]
        ]
        velocity = x_velocity * self.x_factor
        remaining_distances = [min(abs_start_x, abs_end_x)]
        while remaining_distances[-1] > 0:
            remaining_distances.append(remaining_distances[-1] - velocity)
            if velocity > 0:
                velocity -= 1
            else:
                raise ValueError(
                    "Target area unreachable with an"
                    f" initial x velocity of {x_velocity}!"
                )
            #
        #
        return len(remaining_distances) - 1

    def maximum_x_steps(self, x_velocity):
        """Return the minimum number of steps required to
        shoot past the target area using the given
        x velocity
        """
        abs_start_x, abs_end_x = [
            abs(value) for value in self.target_area["x"]
        ]
        velocity = x_velocity * self.x_factor
        remaining_distances = [max(abs_start_x, abs_end_x) + 1]
        while remaining_distances[-1] > 0:
            remaining_distances.append(remaining_distances[-1] - velocity)
            if velocity > 0:
                velocity -= 1
            else:
                logging.debug(
                    "Cannot shoot past the target using an"
                    " initial x velocity of %s!",
                    x_velocity,
                )
                return None
            #
        #
        return len(remaining_distances) - 1

    def highest_vertex(self):
        """Return the highest vertex"""
        target_y = sorted(self.target_area["y"])
        if target_y[1] < 0:
            # max_y_impact_speed = -target_y_min
            # max y start speed: one less
            y_start_speed = -target_y[0] - 1
            # Return vertex height
            return vertex(y_start_speed)
        #
        raise ValueError("Too complicated!")

    def shoot_at_target(self, initial_x, initial_y):
        """Shoot at the target area.
        Return the point where it was hit, or raise
        Missed or a derived exception
        """
        abs_target_x = sorted(abs(value) for value in self.target_area["x"])
        target_x = sorted(self.target_area["x"])
        target_y = sorted(self.target_area["y"])
        x_speed, y_speed = initial_x, initial_y
        x_pos = y_pos = 0
        while True:
            x_pos += x_speed
            y_pos += y_speed
            logging.debug("Position: %s, %s", x_pos, y_pos)
            if x_pos * self.x_factor > abs_target_x[1]:
                raise TooFar
            #
            if y_pos < target_y[0]:
                if x_pos * self.x_factor < abs_target_x[0]:
                    raise TooSteep
                #
                raise Missed
            #
            if (
                target_x[0] <= x_pos <= target_x[1]
                and target_y[0] <= y_pos <= target_y[1]
            ):
                return (x_pos, y_pos)
            #
            # Drift
            if x_speed != 0:
                x_speed -= self.x_factor
            #
            # Gravity
            y_speed -= 1
        #
        raise Missed

    def sure_shots(self):
        """Yield all velocity combinations that hit the target area"""
        min_x_v = self.minimum_x_velocity()
        logging.debug(
            "Minimum initial x velocity to reach target area %r: %s",
            self.target_area,
            min_x_v,
        )
        target_y = sorted(self.target_area["y"])
        if target_y[1] > 0:
            raise ValueError("Too complicated!")
        #
        max_y_v = -target_y[0] - 1
        for initial_x in range(min_x_v, abs(max(self.target_area["x"])) + 1):
            min_steps = self.minimum_x_steps(initial_x)
            max_steps = self.maximum_x_steps(initial_x)
            logging.debug(
                "Minimum steps with initial x velocity of %s: %s",
                initial_x,
                min_steps,
            )
            logging.debug(
                "Steps to shoot past using an initial x velocity of %s: %s",
                initial_x,
                max_steps,
            )
            if max_steps == 1:
                break
            #
            if max_steps is not None and min_steps >= max_steps:
                continue
            #
            for initial_y in range(max_y_v, target_y[0] - 1, -1):
                logging.debug(
                    "Trying initial velocities x=%s, y=%s",
                    initial_x,
                    initial_y,
                )
                try:
                    logging.debug(
                        "Hit target area at %s",
                        self.shoot_at_target(initial_x, initial_y),
                    )
                except TooSteep:
                    logging.debug("Too steep!")
                    break
                except Missed:
                    continue
                #
                yield (initial_x, initial_y)
            #
        #


def vertex(y_speed):
    """Return the highest y reached with the given y speed"""
    if y_speed <= 0:
        return 0
    #
    return int((y_speed + 1) * (y_speed / 2))


@helpers.timer
def part1(reader):
    """Part 1"""
    result = None
    for line in reader.lines():
        calculator = TrajectoryCalculator(line)
        return calculator.highest_vertex()
    #
    return result


@helpers.timer
def part2(reader):
    """Part 2"""
    result = None
    for line in reader.lines():
        calculator = TrajectoryCalculator(line)
        hit_speeds = list(calculator.sure_shots())
        logging.debug(sorted(hit_speeds))
        return len(hit_speeds)
    #
    return result


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
