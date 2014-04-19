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


class TestScoreFromHand(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()

    def test_numbered_cars(self):
        hand = blackjack.card.Hand(self.deck[1:4])  # cards 2, 3, 4
        score = blackjack.score.score_from_hand(hand)
        self.assertEqual(score, 9)

    def test_soft_Ace(self):
        hand = blackjack.card.Hand(self.deck[:3])  # cards Ace, 2, 3
        score = blackjack.score.score_from_hand(hand)
        self.assertEqual(score, 16)

    def test_hard_Ace(self):
        hand = blackjack.card.Hand(self.deck[:5])  # cards Ace, 2, 3, 4, 5
        score = blackjack.score.score_from_hand(hand)
        self.assertEqual(score, 15)


class TestSafeOperations(unittest.TestCase):

    def test_safe_min(self):
        self.assertEqual(blackjack.score.safe_min([2, 4, 1, 3]), 1)

    def test_safe_min_on_empty_sequence(self):
        self.assertEqual(blackjack.score.safe_min([]), None)

    def test_safe_max(self):
        self.assertEqual(blackjack.score.safe_max([2, 4, 1, 3]), 4)

    def test_safe_max_on_empty_sequence(self):
        self.assertEqual(blackjack.score.safe_max([]), None)

