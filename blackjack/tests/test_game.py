"""Unit-tests for blackjack/game.py module."""

import itertools
import unittest
import unittest.mock

from unittest.mock import DEFAULT, call, patch

import blackjack.card
import blackjack.player
import blackjack.game
import blackjack.ui


class BaseTestGame(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.shoe = blackjack.card.Shoe(self.deck)
        self.dealer = blackjack.player.Dealer()
        self.dealer.hand = blackjack.card.Hand()
        self.player = blackjack.player.Player('John', 20)
        self.player.hands.append(blackjack.card.Hand())
        self.table = blackjack.player.Table(self.shoe, self.dealer, [self.player])
        self.ruleset = blackjack.game.AmericanRuleset()
        self.game = blackjack.game.Game(self.ruleset)


class TestGameRun(BaseTestGame):

    @patch.multiple('blackjack.game.Game', _play_new_round=DEFAULT)
    def test_stop_if_everyone_is_broke(self, *args, **kwargs):
        self.player.chip_count = 0
        self.game.run(self.table)
        self.assertFalse(self.game._play_new_round.called)

    @patch.multiple('blackjack.game.Game', _play_new_round=DEFAULT)
    def test_stop_if_no_player_interested(self, *args, **kwargs):
        self.game._play_new_round.return_value = 0
        self.game.run(self.table)
        self.assertEqual(self.game._play_new_round.call_count, 1)

    @patch.multiple('blackjack.game.Game', _play_new_round=DEFAULT)
    def test_run_indefinitely_otherwise(self, *args, **kwargs):
        self.game._play_new_round.side_effect = [1, 1, 1, 1, 0]
        self.game.run(self.table)
        self.assertEqual(self.game._play_new_round.call_count, 5)


class TestGamePlayNewRound(BaseTestGame):

    @patch.multiple('blackjack.game.Game', _collect_wagers=DEFAULT,
        _deal_initial_cards=DEFAULT, _interact_with_player=DEFAULT,
        _interact_with_dealer=DEFAULT, _pay_gains=DEFAULT, _cleanup=DEFAULT)
    def test_stop_if_no_player(self, *args, **kwargs):
        self.game._collect_wagers.return_value = []
        active_player_count = self.game._play_new_round(self.table)
        self.assertEqual(active_player_count, 0)
        self.assertFalse(self.game._deal_initial_cards.called)
        self.assertFalse(self.game._interact_with_player.called)
        self.assertFalse(self.game._interact_with_dealer.called)
        self.assertFalse(self.game._pay_gains.called)
        self.assertFalse(self.game._cleanup.called)

    @patch.multiple('blackjack.game.Game', _collect_wagers=DEFAULT,
        _deal_initial_cards=DEFAULT, _interact_with_player=DEFAULT,
        _interact_with_dealer=DEFAULT, _pay_gains=DEFAULT, _cleanup=DEFAULT)
    def test_play_with_one_player(self, *args, **kwargs):
        self.game._collect_wagers.return_value = self.table.players
        active_player_count = self.game._play_new_round(self.table)
        self.assertEqual(active_player_count, 1)
        self.assertListEqual(self.table.active_players, self.table.players)
        self.game._deal_initial_cards.assert_called_once_with(self.table)
        self.game._interact_with_player.assert_called_once_with(self.table, self.player)
        self.game._interact_with_dealer.assert_called_once_with(self.table, self.dealer)
        self.game._pay_gains.assert_called_once_with(self.table)
        self.game._cleanup.assert_called_once_with(self.table)


class TestGameCollectWagers(BaseTestGame):

    @patch('blackjack.ui.ask')
    def test_no_bet(self, *args, **kwargs):
        blackjack.ui.ask.return_value = 0
        active_players = self.game._collect_wagers(self.table)
        self.assertEqual(blackjack.ui.ask.call_count, 1)
        self.assertListEqual(active_players, [])

    @patch('blackjack.ui.ask')
    def test_bet_under_minimum(self, *args, **kwargs):
        min_wager = self.game.ruleset.MINIMUM_WAGER
        blackjack.ui.ask.side_effect = [min_wager - 1, min_wager, min_wager + 1]
        self.game._collect_wagers(self.table)
        self.assertEqual(blackjack.ui.ask.call_count, 2)

    @patch('blackjack.ui.ask')
    def test_bet_over_current_chip_count(self, *args, **kwargs):
        chip_count = self.player.chip_count
        blackjack.ui.ask.side_effect = [chip_count + 1, chip_count, chip_count - 1]
        self.game._collect_wagers(self.table)
        self.assertEqual(blackjack.ui.ask.call_count, 2)

    @patch('blackjack.ui.ask')
    def test_correct_bet(self, *args, **kwargs):
        self.player.chip_count = self.game.ruleset.MINIMUM_WAGER
        blackjack.ui.ask.return_value = self.game.ruleset.MINIMUM_WAGER
        active_players = self.game._collect_wagers(self.table)
        self.assertEqual(blackjack.ui.ask.call_count, 1)
        self.assertIsInstance(self.player.hands[0], blackjack.card.Hand)
        self.assertIsInstance(self.dealer.hand, blackjack.card.Hand)
        self.assertIn(self.player, active_players)


class TestGameDealInitialCards(BaseTestGame):

    def setUp(self):
        super(TestGameDealInitialCards, self).setUp()
        self.game.ruleset.AUTO_SHUFFLING_SHOE = True  # prevent first shuffling
        self.cards = [
            blackjack.card.Card('Spade', '2'),
            blackjack.card.Card('Spade', 'Ace'),
            blackjack.card.Card('Spade', '3'),
            blackjack.card.Card('Spade', 'Jack'),
        ]
        self.table.active_players = self.table.players

    @patch.multiple('blackjack.card.Shoe', __next__=DEFAULT)
    def test_dealer_has_no_hole_card(self, *args, **kwargs):
        self.game.ruleset.DEALER_RECEIVES_HOLE_CARD = False
        self.game.ruleset.DEALER_REVEALS_BLACKJACK_HAND = None
        self.shoe.__next__.side_effect = self.cards
        self.game._deal_initial_cards(self.table)
        self.assertListEqual(list(self.player.hands[0]), [self.cards[0], self.cards[2]])
        for card in self.player.hands[0]:
            self.assertTrue(card.visible)
        self.assertListEqual(self.dealer.hand, [self.cards[1]])
        self.assertTrue(self.dealer.hand[0].visible)

    @patch.multiple('blackjack.card.Shoe', __next__=DEFAULT)
    def test_dealer_does_not_reveal_on_blackjack(self, *args, **kwargs):
        self.game.ruleset.DEALER_RECEIVES_HOLE_CARD = True
        self.game.ruleset.DEALER_REVEALS_BLACKJACK_HAND = False
        self.shoe.__next__.side_effect = self.cards
        self.game._deal_initial_cards(self.table)
        self.assertListEqual(list(self.player.hands[0]), [self.cards[0], self.cards[2]])
        for card in self.player.hands[0]:
            self.assertTrue(card.visible)
        self.assertListEqual(self.dealer.hand, [self.cards[1], self.cards[3]])
        self.assertTrue(self.dealer.hand[0].visible)
        self.assertFalse(self.dealer.hand[1].visible)

    @patch.multiple('blackjack.card.Shoe', __next__=DEFAULT)
    def test_dealer_reveals_on_blackjack(self, *args, **kwargs):
        self.game.ruleset.DEALER_RECEIVES_HOLE_CARD = True
        self.game.ruleset.DEALER_REVEALS_BLACKJACK_HAND = True
        self.shoe.__next__.side_effect = self.cards
        self.game._deal_initial_cards(self.table)
        self.assertListEqual(list(self.player.hands[0]), [self.cards[0], self.cards[2]])
        for card in self.player.hands[0]:
            self.assertTrue(card.visible)
        self.assertListEqual(self.dealer.hand, [self.cards[1], self.cards[3]])
        self.assertTrue(self.dealer.hand[0].visible)
        self.assertTrue(self.dealer.hand[1].visible)

    @patch.multiple('blackjack.card.Shoe', shuffle=DEFAULT)
    def test_shuffle_non_auto_shuffling_shoe(self, *args, **kwargs):
        self.game.ruleset.AUTO_SHUFFLING_SHOE = False
        self.game._deal_initial_cards(self.table)
        self.shoe.shuffle.assert_called_once_with()


class TestGameInteractWithPlayer(BaseTestGame):

    @patch('blackjack.ui.ask')
    @patch.multiple('blackjack.card.Hand', add_card=DEFAULT, score=DEFAULT)
    def test_player_busted_right_away(self, *args, **kwargs):
        self.player.hands[0].score = blackjack.score.TARGET_SCORE + 1
        self.game._interact_with_player(self.table, self.player)
        self.assertFalse(blackjack.ui.ask.called)
        self.assertFalse(self.player.hands[0].add_card.called)

    @patch('blackjack.ui.ask')
    @patch.multiple('blackjack.card.Hand', score=DEFAULT)
    def test_player_stands(self, *args, **kwargs):
        self.player.hands[0].score = 2
        blackjack.ui.ask.return_value = 's'
        card_count_before = len(self.player.hands[0])
        self.game._interact_with_player(self.table, self.player)
        self.assertTrue(blackjack.ui.ask.called)
        self.assertEqual(len(self.player.hands[0]), card_count_before)

    @patch('blackjack.ui.ask')
    @patch.multiple('blackjack.card.Hand', score=DEFAULT)
    def test_player_hits(self, *args, **kwargs):
        self.player.hands[0].score = 2
        blackjack.ui.ask.side_effect = ['h', 's']
        card_count_before = len(self.player.hands[0])
        self.game._interact_with_player(self.table, self.player)
        self.assertEqual(len(self.player.hands[0]), card_count_before + 1)


class TestGameInteractWithDealer(BaseTestGame):

    def setUp(self):
        super(TestGameInteractWithDealer, self).setUp()
        self.ruleset.DEALER_RECEIVES_HOLE_CARD = True

    @patch.multiple('blackjack.card.Hand', score=DEFAULT)
    def test_dealer_receives_hole_card(self, *args, **kwargs):
        self.ruleset.DEALER_RECEIVES_HOLE_CARD = False
        self.dealer.hand.score = blackjack.score.TARGET_SCORE + 1
        card_count_before = len(self.dealer.hand)
        self.game._interact_with_dealer(self.table, self.dealer)
        self.assertEqual(len(self.dealer.hand), card_count_before + 1)

    @patch('blackjack.ui.ask')
    @patch.multiple('blackjack.card.Hand', score=DEFAULT)
    def test_dealer_busted_right_away(self, *args, **kwargs):
        self.dealer.hand.score = blackjack.score.TARGET_SCORE + 1
        card_count_before = len(self.dealer.hand)
        self.game._interact_with_dealer(self.table, self.dealer)
        self.assertFalse(blackjack.ui.ask.called)
        self.assertEqual(len(self.dealer.hand), card_count_before)

    def test_dealer_stands(self, *args, **kwargs):
        self.dealer.hand.add_card(blackjack.card.Card('Heart', '10'))
        self.dealer.hand.add_card(blackjack.card.Card('Heart', '7'))
        card_count_before = len(self.dealer.hand)
        self.game._interact_with_dealer(self.table, self.dealer)
        self.assertEqual(len(self.dealer.hand), card_count_before)

    def test_dealer_hits(self, *args, **kwargs):
        self.dealer.hand.add_card(blackjack.card.Card('Heart', '10'))
        self.dealer.hand.add_card(blackjack.card.Card('Heart', '6'))
        card_count_before = len(self.dealer.hand)
        self.game._interact_with_dealer(self.table, self.dealer)
        self.assertEqual(len(self.dealer.hand), card_count_before + 1)


class TestGamePayGains(BaseTestGame):

    def setUp(self):
        super(TestGamePayGains, self).setUp()
        self.player.hands[0].wager = 5
        self.table.active_players = self.table.players

    @patch('blackjack.score.compare_hands')
    def test_pay_on_BUST(self, *args, **kwargs):
        blackjack.score.compare_hands.return_value = (blackjack.score.BUST, None)
        chip_count_before = self.player.chip_count
        self.game._pay_gains(self.table)
        self.assertEqual(self.player.chip_count, chip_count_before)

    @patch('blackjack.score.compare_hands')
    def test_pay_on_LOOSE(self, *args, **kwargs):
        blackjack.score.compare_hands.return_value = (blackjack.score.LOOSE, None)
        chip_count_before = self.player.chip_count
        self.game._pay_gains(self.table)
        self.assertEqual(self.player.chip_count, chip_count_before)

    @patch('blackjack.score.compare_hands')
    def test_pay_on_PUSH(self, *args, **kwargs):
        blackjack.score.compare_hands.return_value = (blackjack.score.PUSH, None)
        chip_count_before = self.player.chip_count
        self.game._pay_gains(self.table)
        expected_chip_count = chip_count_before + self.player.hands[0].wager
        self.assertEqual(self.player.chip_count, expected_chip_count)

    @patch('blackjack.score.compare_hands')
    def test_pay_on_WIN(self, *args, **kwargs):
        blackjack.score.compare_hands.return_value = (blackjack.score.WIN, None)
        chip_count_before = self.player.chip_count
        self.game._pay_gains(self.table)
        expected_chip_count = chip_count_before + 2 * self.player.hands[0].wager
        self.assertEqual(self.player.chip_count, expected_chip_count)

    @patch('blackjack.score.compare_hands')
    def test_pay_on_BLACKJACK(self, *args, **kwargs):
        blackjack.score.compare_hands.return_value = (blackjack.score.BLACKJACK, None)
        chip_count_before = self.player.chip_count
        self.game._pay_gains(self.table)
        ratio = 1 + self.ruleset.BLACKJACK_PAYOUT_RATIO
        expected_chip_count = chip_count_before + int(ratio * self.player.hands[0].wager)
        self.assertEqual(self.player.chip_count, expected_chip_count)


class TestGameCleanup(BaseTestGame):

    def setUp(self):
        super(TestGameCleanup, self).setUp()
        self.table.active_players = self.table.players

    def test_cleanup(self, *args, **kwargs):
        card_count_before = len(self.shoe)
        dealt_card = set(itertools.islice(self.shoe, len(self.shoe) - 3))
        self.assertEqual(len(self.shoe), 3)
        self.game._cleanup(self.table)
        self.assertListEqual(self.player.hands, [])
        self.assertEqual(self.dealer.hand, None)
        self.assertEqual(len(self.shoe), card_count_before)

