from typing import Optional

import numpy as np

from markov_chain.examples.monopoly.utils import MonopolySettings
from markov_chain.examples.monopoly.utils import MonopolySimulationBase


class MonopolyMonteCarlo(MonopolySimulationBase):
    """
    Simulate the monopoly game using Monte Carlo techniques

    Pass MonopolySetting to define the settings used for the game.
    The num_players parameter allows you to define the number of simulations to run to calculate the probability.
        This selection is a tradeoff between accuracy and processing time.
    """

    def __init__(self, settings: Optional[MonopolySettings] = None, num_players: int = 10) -> None:
        super().__init__(settings)
        self.num_players = num_players
        self.game_states = np.zeros((1, num_players), int)
        self.rolls1 = np.zeros((1, num_players), int)
        self.rolls2 = np.zeros((1, num_players), int)

    def advance(self) -> None:
        """Advance all of the players by simulating their next turn. Stack the result onto the game_states."""
        prev_turn = self.game_states[-1, :]

        roll_sample = np.random.choice([1, 2, 3, 4, 5, 6], size=(2, self.num_players))
        self.rolls1 = np.vstack([self.rolls1, roll_sample[0, :]])
        self.rolls2 = np.vstack([self.rolls2, roll_sample[1, :]])

        next_turn = prev_turn + roll_sample[0, :] + roll_sample[1, :]
        next_turn = self.replacements(next_turn)

        self.game_states = np.vstack([self.game_states, next_turn])

    def replacements(self, arr: np.ndarray) -> np.ndarray:
        """For a given array of positions, make replacements for go to jail, advance to ..., etc."""
        # Subtract 40 from those which have looped around the board
        arr2 = np.where(arr > 39, arr - 40, arr)
        # Go to jail square
        arr2 = np.where(arr2 == 30, 10, arr2)
        # Advance to x chance/comm chest
        choose_advance = np.random.choice(np.arange(0, self._settings.n_chance), size=(1, self.num_players)) < len(
            self._settings.chance_advances
        )
        advance_to_locs = np.random.choice(self._settings.chance_advances, size=(1, self.num_players))
        arr2 = np.where(
            np.isin(arr2, self._settings.chance_locs) * choose_advance,
            advance_to_locs,
            arr2,
        )
        # Roll three doubles jail
        if self._settings.three_doubles_jail and self.rolls1.shape[0] > 3:
            arr2 = np.where(
                np.all(self.rolls1[-3:, :] == self.rolls2[-3:, :], axis=0),
                10,
                arr2,
            )

        return arr2

    def state_at_time(self, t: int) -> np.ndarray:
        """Calculate the state at time t"""
        while self.game_states.shape[0] < t + 1:
            self.advance()

        state = self.game_states[t, :]
        counts = []
        for i in range(40):
            counts.append((state == i).sum())
        counts = counts / sum(counts)
        return counts
