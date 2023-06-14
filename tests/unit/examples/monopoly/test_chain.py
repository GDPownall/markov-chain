import unittest

from markov_chain.examples.monopoly.chain import dice_roll_prob


class TestDiceRollProb(unittest.TestCase):
    def test_probabilities(self):
        expected_probabilities = {
            2: 1 / 36,
            3: 2 / 36,
            4: 3 / 36,
            5: 4 / 36,
            6: 5 / 36,
            7: 6 / 36,
            8: 5 / 36,
            9: 4 / 36,
            10: 3 / 36,
            11: 2 / 36,
            12: 1 / 36,
        }

        for n, expected in expected_probabilities.items():
            self.assertAlmostEqual(dice_roll_prob(n), expected, delta=0.0001)

    def test_out_of_bounds(self):
        self.assertEqual(dice_roll_prob(0), 0)
        self.assertEqual(dice_roll_prob(1), 0)
        self.assertEqual(dice_roll_prob(13), 0)
        self.assertEqual(dice_roll_prob(20), 0)
