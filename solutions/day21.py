#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advent of code 2021, day 21
blackstream-x’ solution
"""


import collections
import itertools
import logging
import random

import helpers


class BaseDie:

    """Abstract die class capable of counting all dice rolls"""

    def __init__(self):
        """Initialize counter"""
        self.__counter = 0

    @property
    def counter(self):
        """Counter readonly access"""
        return self.__counter

    def get_single_cast_result(self):
        """Return a single cast result"""
        raise NotImplementedError

    def cast(self, rolls=1):
        """Cast {rolls} times and return a list of cast values"""
        results = []
        for _ in range(rolls):
            self.__counter += 1
            results.append(self.get_single_cast_result())
        #
        return results


class StandardDie(BaseDie):

    """Standard 6-sided die casting random results"""

    def get_single_cast_result(self):
        """Return a single cast result"""
        return int(random.random() * 6) + 1


class DeterministicDie(BaseDie):

    """Die always casting 1, 2, 3, …,98, 99, 100, 1, 2, 3, …"""

    def get_single_cast_result(self):
        """Return a single cast result"""
        return helpers.based_mod(self.counter, 100, offset=1)


class DiracDie(BaseDie):

    """Die always splitting the universe and casting
    1 in the first, 2 in the second and 3 in the third
    universes
    """

    cast_result = (1, 2, 3)

    def get_single_cast_result(self):
        """Return a single cast result"""
        return self.cast_result


class DiracDiceGame:

    """Quantum-capable dice game"""

    def __init__(self, die=None, board_size=10):
        """Initialize values"""
        self.die = die
        self.board_size = board_size
        self.start_positions = {}
        self.cast_sums = {}
        self.game_states = {}
        self.players = []
        self.player_lookup = {}
        self.win_threshold = 0
        self.dice_rolls = 0
        self.possible_points = range(0)
        self.possible_positions = range(self.board_size)  # 0-based!

    def get_won_universes(self):
        """Return a dict containing the number of universes
        with won games per player
        """
        won_games = {0: 0, 1: 0}
        for state_index, universes in self.game_states.items():
            if not self.games_are_won(state_index):
                continue
            #
            already_won = False
            for player_index in (0, 1):
                if state_index[player_index] >= self.win_threshold:
                    if already_won:
                        logging.error(
                            "The other player has already won in these"
                            " %s universes!",
                            universes,
                        )
                    #
                    already_won = True
                    won_games[player_index] += universes
                #
            #
        #
        return won_games

    def get_player_scores(self):
        """Return a dict where the keys are composed of
        a player index and a score, and the values are
        the number of universes in which the player has that score.
        """
        all_scores = {}
        for state_index, universes in self.game_states.items():
            for player_index in (0, 1):
                player_score = state_index[player_index] // self.board_size
                score_index = (player_index, player_score)
                all_scores.setdefault(score_index, 0)
                all_scores[score_index] += universes
            #
        #
        return all_scores

    def add_player_from_line(self, line):
        """Add player from the given input line"""
        components = line.split()
        name = components[1]
        self.start_positions[name] = int(components[4])
        self.players.append(name)

    def address(self, score, position):
        """Return an axis address calculated from score and position"""
        return self.board_size * score + position

    def score_and_position(self, axis_address):
        """Return score and position from the axis address"""
        return divmod(axis_address, self.board_size)

    def games_are_won(self, state_index):
        """Return True if the games in {state_index} are won"""
        for player_index in (0, 1):
            if state_index[player_index] >= self.win_threshold:
                return True
            #
        #
        return False

    def do_deterministic_turn(self, name):
        """Cast the die {self.dice_rolls} times,
        no universe split
        """
        turn_player_idx = self.player_lookup[name]
        state_index, universe = self.game_states.popitem()
        if self.games_are_won(state_index):
            # transfer the already won game directly
            self.game_states[state_index] = universe
            return
        #
        score, position = self.score_and_position(state_index[turn_player_idx])
        cast_values = self.die.cast(rolls=self.dice_rolls)
        mutable_index = list(state_index)
        new_position = (position + sum(cast_values)) % self.board_size
        new_score = score + new_position + 1
        logging.debug(
            "Player %s rolls %s and moves to space %s"
            " for a total score of %s.",
            name,
            "+".join(str(value) for value in cast_values),
            new_position,
            new_score,
        )
        mutable_index[turn_player_idx] = self.address(new_score, new_position)
        next_index = tuple(mutable_index)
        self.game_states[next_index] = universe

    def do_quantum_turn(self, name):
        """Cast the die {self.dice_rolls} times
        with universe splits
        """
        turn_player_idx = self.player_lookup[name]
        next_state = {}
        for state_index, universes in self.game_states.items():
            if self.games_are_won(state_index):
                # transfer already won games directly
                next_state.setdefault(state_index, 0)
                next_state[state_index] += universes
                continue
            #
            score, position = self.score_and_position(
                state_index[turn_player_idx]
            )
            # Calculate the result of all {self.dice_rolls} casts
            for (total_steps, times) in self.cast_sums.items():
                mutable_index = list(state_index)
                new_position = (position + total_steps) % self.board_size
                new_score = score + new_position + 1
                mutable_index[turn_player_idx] = self.address(
                    new_score, new_position
                )
                next_index = tuple(mutable_index)
                next_state.setdefault(next_index, 0)
                next_state[next_index] += universes * times
            #
        #
        self.game_states = dict(next_state)

    def open_games(self):
        """Return True if there are still unfinished games"""
        for state_index in self.game_states:
            if not self.games_are_won(state_index):
                return True
            #
        #
        return False

    def play(self, until_score=21, dice_rolls=3):
        """Play until the games in all universes have ended.
        A game ends if one of the players reaches {until_score}.
        """
        logging.debug("=" * 70)
        logging.debug("Playing until a score of %s is reached", until_score)
        logging.debug("=" * 70)
        self.dice_rolls = dice_rolls
        self.win_threshold = self.address(until_score, 0)
        self.player_lookup = {
            player: index for (index, player) in enumerate(self.players)
        }
        if isinstance(self.die, DiracDie):
            self.cast_sums = collections.Counter(
                [
                    sum(casts)
                    for casts in itertools.product(
                        self.die.cast_result, repeat=self.dice_rolls
                    )
                ]
            )
            do_turn = self.do_quantum_turn
        else:
            do_turn = self.do_deterministic_turn
        #
        start_indices = [0, 0]
        for player in self.players:
            start_indices[self.player_lookup[player]] = self.address(
                0, self.start_positions[player] - 1
            )
        #
        # Always start in the known, single universe
        self.game_states = {tuple(start_indices): 1}
        while self.open_games():
            for player in self.players:
                do_turn(player)
            #
        #


@helpers.timer
def part1(reader):
    """Part 1"""
    game = DiracDiceGame(DeterministicDie())
    for line in reader.lines():
        game.add_player_from_line(line)
    #
    game.play(until_score=1000)
    won_universes = game.get_won_universes()
    final_scores = game.get_player_scores()
    loser_score = 0
    for (player_index, score) in final_scores:
        logging.info(
            "Player %s reached a total score of %s",
            game.players[player_index],
            score,
        )
        if not won_universes[player_index]:
            loser_score = score
        #
    #
    return loser_score * game.die.counter


@helpers.timer
def part2(reader):
    """Part 2"""
    game = DiracDiceGame(DiracDie())
    for line in reader.lines():
        game.add_player_from_line(line)
    #
    game.play(until_score=21)
    won_universes = game.get_won_universes()
    for player in game.players:
        logging.info(
            "Player %s has won in %s universes",
            player,
            won_universes[game.player_lookup[player]],
        )
    #
    return max(won_universes.values())


if __name__ == "__main__":
    helpers.solve_puzzle(part1, part2)


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
