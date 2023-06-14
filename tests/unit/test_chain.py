import unittest

import numpy as np

from markov_chain.chain import MarkovChain


class TestMarkovChain(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(ValueError):
            MarkovChain([[]])
        with self.assertRaises(ValueError):
            MarkovChain([[0.2, 0.8], [0.5, 0.3]])
        with self.assertRaises(ValueError):
            MarkovChain([[0.2, 0.3]], [0.2, 0.8])

    def test_renorm_eigvectors(self):
        vectors = np.array([[3, -2], [1, 1]])
        renormed = MarkovChain._renorm_eigvectors(vectors)
        np.testing.assert_array_almost_equal(renormed, np.array([[1, -2 / 3], [1, 1]]))

    def test_state_at_time(self):
        mc = MarkovChain([[0.9, 0.5], [0.1, 0.5]], [0.2, 0.8])
        state = mc.state_at_time(2)
        np.testing.assert_array_almost_equal(state, np.array([0.732, 0.268]))

    def test_stationary_state(self):
        mc = MarkovChain([[0.9, 0.5], [0.1, 0.5]], [0.2, 0.8])
        stationary_state = mc.stationary_state()
        np.testing.assert_array_almost_equal(stationary_state, np.array([5 / 6, 1 / 6]))
