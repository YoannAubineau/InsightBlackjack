"""Unit-tests for blackjack/ui.py module."""

import unittest
import unittest.mock
import sys

import blackjack.card
import blackjack.player
import blackjack.ui


class TestPrint(unittest.TestCase):

    def setUp(self):
        unittest.mock.patch('sys.stdout').start()

    def tearDown(self):
        unittest.mock.patch.stopall()

    def test(self):
        blackjack.ui.print('test')


class TestDisplayPlayer(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.player = blackjack.player.Player('John', 5)
        self.player.hand = blackjack.card.Hand()
        unittest.mock.patch('sys.stdout').start()

    def tearDown(self):
        unittest.mock.patch.stopall()

    def test_display_player_with_no_hand(self):
        self.player.hand = None
        blackjack.ui.display_player(self.player)

    def test_display_player_with_no_card(self):
        blackjack.ui.display_player(self.player)

    def test_display_player_with_cards(self):
        self.player.hand.add_card(self.deck[0])
        blackjack.ui.display_player(self.player)


class TestDisplayDealer(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.dealer = blackjack.player.Dealer()
        self.dealer.hand = blackjack.card.Hand()
        unittest.mock.patch('sys.stdout').start()

    def tearDown(self):
        unittest.mock.patch.stopall()

    def test_display_player_with_no_hand(self):
        self.dealer.hand = None
        blackjack.ui.display_dealer(self.dealer)

    def test_display_player_with_no_card(self):
        blackjack.ui.display_dealer(self.dealer)

    def test_display_player_with_cards(self):
        self.dealer.hand.add_card(self.deck[0])
        blackjack.ui.display_dealer(self.dealer)


class TestAsk(unittest.TestCase):

    def setUp(self):
        unittest.mock.patch('sys.stdout').start()

    def tearDown(self):
        unittest.mock.patch.stopall()

    @unittest.mock.patch('builtins.input')
    def test_type_argument(self, input):
        input.side_effect = ['a', 'b', '3', '4']
        key = blackjack.ui.ask('', type=int)
        self.assertEqual(key, 3)
        self.assertEqual(input.call_count, 3)

    @unittest.mock.patch('builtins.input')
    def test_choices_argument(self, input):
        input.side_effect = ['a', 'b', 'c', 'd']
        key = blackjack.ui.ask('', choices=['c'])
        self.assertEqual(key, 'c')
        self.assertEqual(input.call_count, 3)

    @unittest.mock.patch('builtins.input')
    def test_default_argument(self, input):
        input.side_effect = ['', 'b']
        key = blackjack.ui.ask('', default='c')
        self.assertEqual(key, 'c')
        self.assertEqual(input.call_count, 1)

    @unittest.mock.patch('builtins.input')
    def test_inconsistent_default_and_type_arguments(self, input):
        with self.assertRaises(ValueError):
            blackjack.ui.ask('', type=int, default='c')

    @unittest.mock.patch('builtins.input')
    def test_inconsistent_default_and_choices_arguments(self, input):
        with self.assertRaises(ValueError):
            blackjack.ui.ask('', choices=['a', 'b'], default='c')

