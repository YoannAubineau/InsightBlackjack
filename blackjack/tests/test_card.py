"""Unit-tests for blackjack/card.py module."""

import itertools
import unittest

import blackjack.card


class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = blackjack.card.Card('Heart', 'Queen')

    def test_name(self):
        self.assertIn('Heart', self.card.name)
        self.assertIn('Queen', self.card.name)

    def test_str_visible(self):
        self.card.visible = True
        self.assertEqual(str(self.card), self.card.name)

    def test_str_hidden(self):
        self.card.visible = False
        self.assertEqual(str(self.card), '<hidden>')

    def test_values(self):
        self.assertTrue(self.card.values)

    def test_repr_face_up(self):
        self.card.visible = True
        self.assertIn('face up', repr(self.card))

    def test_repr_face_down(self):
        self.card.visible = False
        self.assertIn('face down', repr(self.card))


class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()

    def test_size(self):
        self.assertEqual(len(self.deck), 52)
        self.deck.pop()
        self.assertEqual(len(self.deck), 51)

    def test_unicity(self):
        self.assertEqual(len(set(self.deck)), len(self.deck))

    def test_repr(self):
        self.assertIn(str(len(self.deck)), repr(self.deck))


class TestShoe(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.shoe = blackjack.card.Shoe(self.deck)

    def test_size(self):
        self.assertEqual(len(self.shoe), len(self.deck))

    def test_drawn_card_is_hidden(self):
        card = self.shoe.draw_card(visible=False)
        self.assertFalse(card.visible)

    def test_drawn_card_is_visible(self):
        card = self.shoe.draw_card(visible=True)
        self.assertTrue(card.visible)

    def test_size_update(self):
        size_before = len(self.shoe)
        card = self.shoe.draw_card()
        self.assertEqual(len(self.shoe), size_before - 1)

    def test_constant_size_after_shuffling(self):
        size_before = len(self.shoe)
        self.shoe.shuffle()
        self.assertEqual(len(self.shoe), size_before)

    def test_suffling_not_bringing_back_dealt_cards(self):
        dealt_card = set(itertools.islice(self.shoe, len(self.shoe) - 3))
        self.shoe.shuffle()
        remaining_cards = set(self.shoe)
        intersection = set.intersection(dealt_card, remaining_cards)
        self.assertEqual(len(intersection), 0)

    def test_repr(self):
        self.assertIn(str(len(self.shoe)), repr(self.shoe))

