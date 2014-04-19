"""Unit-tests for blackjack/score.py module."""

import unittest

import blackjack.card
import blackjack.score


class TestValuesFromCard(unittest.TestCase):

    def test_numbered_card(self):
        card = blackjack.card.Card('Spade', '2')
        values = blackjack.score.values_from_card(card)
        self.assertEqual(values, [2])

    def test_Jack(self):
        card = blackjack.card.Card('Diamond', 'Jack')
        values = blackjack.score.values_from_card(card)
        self.assertEqual(values, [10])

    def test_Queen(self):
        card = blackjack.card.Card('Heart', 'Queen')
        values = blackjack.score.values_from_card(card)
        self.assertEqual(values, [10])

    def test_King(self):
        card = blackjack.card.Card('Spike', 'King')
        values = blackjack.score.values_from_card(card)
        self.assertEqual(values, [10])

    def test_Ace(self):
        card = blackjack.card.Card('Spade', 'Ace')
        values = blackjack.score.values_from_card(card)
        self.assertEqual(values, [1, 11])

    def test_Jocker(self):
        card = blackjack.card.Card('Spade', 'Jocker')
        with self.assertRaises(Exception):
            values = blackjack.score.values_from_card(card)

