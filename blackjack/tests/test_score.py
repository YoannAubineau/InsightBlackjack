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


class TestCompareHands(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.BUST = blackjack.score.BUST
        self.LOOSE = blackjack.score.LOOSE
        self.PUSH = blackjack.score.PUSH
        self.WIN = blackjack.score.WIN
        self.BLACKJACK = blackjack.score.BLACKJACK

    def test_both_hand_busted(self):
        hand1 = blackjack.card.Hand(self.deck[-3:])  # cards Jack, Queen, King
        hand2 = blackjack.card.Hand(self.deck[-3:])  # cards Jack, Queen, King
        outcome = blackjack.score.compare_hands(hand1, hand1)
        self.assertEqual(outcome, (self.BUST, self.BUST))

    def test_right_hand_busted(self):
        hand1 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        hand2 = blackjack.card.Hand(self.deck[-3:])  # cards Jack, Queen, King
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.WIN, self.BUST))

    def test_left_hand_busted(self):
        hand1 = blackjack.card.Hand(self.deck[-3:])  # cards Jack, Queen, King
        hand2 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.BUST, self.WIN))

    def test_left_greater_than_right(self):
        hand1 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        hand2 = blackjack.card.Hand(self.deck[1:3])  # cards 2, 3
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.WIN, self.LOOSE))

    def test_right_greater_than_left(self):
        hand1 = blackjack.card.Hand(self.deck[1:3])  # cards 2, 3
        hand2 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.LOOSE, self.WIN))

    def test_left_does_blackjack(self):
        hand1 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        hand2 = blackjack.card.Hand(self.deck[1:3])  # cards 2, 3
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.BLACKJACK, self.LOOSE))

    def test_right_does_blackjack(self):
        hand1 = blackjack.card.Hand(self.deck[1:3])  # cards 2, 3
        hand2 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.LOOSE, self.BLACKJACK))

    def test_equal_hands(self):
        hand1 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        hand2 = blackjack.card.Hand(self.deck[:3])   # cards Ace, 2, 3
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.PUSH, self.PUSH))

    def test_equal_hands_with_left_blackjack(self):
        hand1 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        hand2 = blackjack.card.Hand(self.deck[:6])   # cards Ace, 2, 3, 4, 5, 6
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.BLACKJACK, self.LOOSE))

    def test_equal_hands_with_right_blackjack(self):
        hand1 = blackjack.card.Hand(self.deck[:6])   # cards Ace, 2, 3, 4, 5, 6
        hand2 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.LOOSE, self.BLACKJACK))

    def test_both_blackjack(self):
        hand1 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        hand2 = blackjack.card.Hand([self.deck[0], self.deck[-1]])  # cards Ace, King
        outcome = blackjack.score.compare_hands(hand1, hand2)
        self.assertEqual(outcome, (self.PUSH, self.PUSH))


class TestSafeOperations(unittest.TestCase):

    def test_safe_min(self):
        self.assertEqual(blackjack.score.safe_min([2, 4, 1, 3]), 1)

    def test_safe_min_on_empty_sequence(self):
        self.assertEqual(blackjack.score.safe_min([]), None)

    def test_safe_max(self):
        self.assertEqual(blackjack.score.safe_max([2, 4, 1, 3]), 4)

    def test_safe_max_on_empty_sequence(self):
        self.assertEqual(blackjack.score.safe_max([]), None)

