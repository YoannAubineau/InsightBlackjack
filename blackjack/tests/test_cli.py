"""Unit-tests for blackjack/cli.py module."""

import unittest
import unittest.mock
from unittest.mock import patch, DEFAULT

import blackjack.card
import blackjack.cli
import blackjack.game
import blackjack.player


class TestPlay(unittest.TestCase):

    def setUp(self):
        self.ruleset = blackjack.game.AmericanRuleset()
        self.player_infos = [('John', 5), ('Suzy', 13)]

    @patch.multiple('blackjack.player.Table', play=DEFAULT)
    def test(self, *args, **kwargs):
        table, game = blackjack.cli.play(self.ruleset, self.player_infos)
        table.play.assert_called_once_with(game)

    @patch.multiple('blackjack.player.Table', play=DEFAULT)
    def test_no_autoshuffling(self, *args, **kwargs):
        self.ruleset.AUTO_SHUFFLING_SHOE = False
        table, game = blackjack.cli.play(self.ruleset, self.player_infos)
        self.assertIsInstance(table.shoe, blackjack.card.Shoe)
        self.assertNotIsInstance(table.shoe, blackjack.card.ShufflingShoe)

    @patch.multiple('blackjack.player.Table', play=DEFAULT)
    def test_with_autoshuffling(self, *args, **kwargs):
        self.ruleset.AUTO_SHUFFLING_SHOE = True
        table, game = blackjack.cli.play(self.ruleset, self.player_infos)
        self.assertIsInstance(table.shoe, blackjack.card.ShufflingShoe)

