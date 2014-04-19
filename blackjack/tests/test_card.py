"""Unit-tests for blackjack/card.py module."""

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

