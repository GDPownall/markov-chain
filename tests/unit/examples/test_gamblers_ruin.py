import unittest

from markov_chain.chain import MarkovChain
from markov_chain.examples.gamblers_ruin import gamblers_ruin


class TestGamblersRuin(unittest.TestCase):
    def test_defaults(self):
        result = gamblers_ruin()
        self.assertIsInstance(result, MarkovChain)
        self.assertAlmostEqual(result.n_states, 201)
        self.assertTrue(result._initial_state[100])
        self.assertAlmostEqual(result._probability_matrix[0][0], 1.0)
        self.assertAlmostEqual(result._probability_matrix[200][200], 1.0)
        self.assertAlmostEqual(result._probability_matrix[101][100], 0.5)
        self.assertAlmostEqual(result._probability_matrix[99][100], 0.5)

    def test_custom_params(self):
        result = gamblers_ruin(initial_position=50, prob_up=0.7, upper_limit=100, lower_limit=10)
        self.assertIsInstance(result, MarkovChain)
        self.assertAlmostEqual(result.n_states, 91)
        self.assertTrue(result._initial_state[50])
        self.assertAlmostEqual(result._probability_matrix[0][0], 1.0)
        self.assertAlmostEqual(result._probability_matrix[90][90], 1.0)
        self.assertAlmostEqual(result._probability_matrix[41][40], 0.7)
        self.assertAlmostEqual(result._probability_matrix[39][40], 0.3)
