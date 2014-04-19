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

