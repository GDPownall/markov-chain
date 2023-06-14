from functools import lru_cache
from typing import Optional

import numpy as np

from markov_chain.chain import MarkovChain
from markov_chain.examples.monopoly.utils import MonopolySettings
from markov_chain.examples.monopoly.utils import MonopolySimulationBase


@lru_cache(maxsize=12)
def dice_roll_prob(n: int) -> float:
    """
    Return probability of getting n when rolling two dice.

    LRU cache is used to store results.
    """
    if n < 2 or n > 12:
        return 0
    if n <= 7:
        p = n - 1
    else:
        p = 13 - n
    return p / 36


class MonopolyMarkovChain(MonopolySimulationBase):
    """
    Monopoly simulation based on a Markov Chain approach.

    Uses MonopolySettings class to define how the game is played.
    """

    def __init__(self, settings: Optional[MonopolySettings] = None) -> None:
        super().__init__(settings)

        initial_state = [1.0] + 39 * [0.0]
        # Set up probability matrix

        prob_mat = [[0.0] * 40 for i in range(40)]
        prob_three_doubles = 1 / 6**3

        for n in range(40):
            for m in range(2, 13):
                if n + m < 40:
                    prob_mat[n + m][n] = dice_roll_prob(m)
                else:
                    prob_mat[n + m - 40][n] = dice_roll_prob(m)

            # Roll three doubles (probability 1/6**3), go to jail
            if settings.three_doubles_jail:
                for m in range(40):
                    prob_mat[m][n] *= 1 - prob_three_doubles
                prob_mat[10][n] += prob_three_doubles

            # Go to jail square
            prob_mat[10][n] += prob_mat[30][n]
            prob_mat[30][n] = 0

            # Chance cards
            n_chance = settings.n_chance
            chance_locs = settings.chance_locs
            chance_advances = settings.chance_advances
            for chance in chance_locs:
                for advance in chance_advances:
                    p_advance_to = prob_mat[chance][n] / n_chance
                    prob_mat[advance][n] += p_advance_to
                    prob_mat[chance][n] = prob_mat[chance][n] * (1 - 1 / n_chance)

        self.initial_state = initial_state
        self.prob_matrix = prob_mat
        self.markov = MarkovChain(prob_mat, initial_state)

    def state_at_time(self, time: int) -> np.ndarray:
        """Return the state at time"""
        return self.markov.state_at_time(time)
