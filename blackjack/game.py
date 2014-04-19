"""Rulesets and gameplay implementation."""

import blackjack.player
import blackjack.score
import blackjack.ui

from blackjack.ui import print


class Ruleset(object):
    """Parent type for all rulesets."""
    pass


class BasicRuleset(Ruleset):
    """The most simple set of rules."""

    MAXIMUM_PLAYER_COUNT = 1
    DECK_COUNT_IN_SHOE = 1
    AUTO_SHUFFLING_SHOE = False
    MINIMUM_WAGER = 1
    DEALER_RECEIVES_HOLE_CARD = False
    DEALER_REVEALS_BLACKJACK_HAND = None
    BLACKJACK_PAYOUT_RATIO = 2/1


class EuropeanRuleset(Ruleset):
    """The most common set of rules in Europe."""

    MAXIMUM_PLAYER_COUNT = 7
    DECK_COUNT_IN_SHOE = 6
    AUTO_SHUFFLING_SHOE = False
    MINIMUM_WAGER = 10
    DEALER_RECEIVES_HOLE_CARD = False
    DEALER_REVEALS_BLACKJACK_HAND = None
    BLACKJACK_PAYOUT_RATIO = 3/2


class AmericanRuleset(Ruleset):
    """The most common set of rules in the USA."""

    MAXIMUM_PLAYER_COUNT = 7
    DECK_COUNT_IN_SHOE = 8
    AUTO_SHUFFLING_SHOE = True
    MINIMUM_WAGER = 10
    DEALER_RECEIVES_HOLE_CARD = True
    DEALER_REVEALS_BLACKJACK_HAND = True
    BLACKJACK_PAYOUT_RATIO = 3/2


class InsightRuleset(AmericanRuleset):
    """The rules as defined by Insight Coding Challenge."""

    MAXIMUM_PLAYER_COUNT = 1
    MINIMUM_WAGER = 1


ruleset_map = {
    'basic': BasicRuleset,
    'european': EuropeanRuleset,
    'american': AmericanRuleset,
    'insight': InsightRuleset,
}


class Game(object):
    """Complete Blackjack gameplay implementation."""

    def __init__(self, ruleset):
        self.ruleset = ruleset
        self.running = None

    def run(self, table):
        """Run the game on given table while enough players."""
        self.running = True
        while self.running:
            print('Starting new round…')
            if not any(p.chip_count for p in table.players):
                print('Everyone is broke here! Bye-bye.')
                break
            player_count = self._play_new_round(table)
            if not player_count:
                print('No one wants to play anymore? Let\'s stop the game.')
                break

    def _play_new_round(self, table):
        """Play a single full game round."""
        active_players = self._collect_wagers(table)
        if not active_players:
            return 0
        table.active_players = active_players
        self._deal_initial_cards(table)
        for player in table.active_players:
            self._interact_with_player(table, player)
        self._interact_with_dealer(table, table.dealer)
        self._pay_gains(table)
        self._cleanup(table)
        player_count = len(active_players)
        return player_count

    def _collect_wagers(self, table):
        """Collect wagers around table and return active players."""
        print('Collecting wagers…')
        active_players = []
        for player in table.players:
            blackjack.ui.display_player(player)
            while True:
                chip_count = blackjack.ui.ask('How much would you like to bet for that round?',
                    type=int, default=self.ruleset.MINIMUM_WAGER)
                if not chip_count:
                    print('Player "{}" not playing this round.'.format(player))
                    break
                if chip_count < self.ruleset.MINIMUM_WAGER:
                    print('Minium bet is {}'.format(self.ruleset.MINIMUM_WAGER))
                    continue
                if chip_count > player.chip_count:
                    print('You do not have enough chips! Please lower your bet.')
                    continue
                player.hand = blackjack.card.Hand()
                player.bet(chip_count)
                active_players.append(player)
                break
        if active_players:
            table.dealer.hand = blackjack.card.Hand()
        return active_players

    def _deal_initial_cards(self, table):
        """Deal two cards to each active players and dealer."""
        print('Dealing initial two cards…')
        if not self.ruleset.AUTO_SHUFFLING_SHOE:
            table.shoe.shuffle()
        # First round
        for player in table.active_players:
            card = table.shoe.draw_card(visible=True)
            player.hand.add_card(card)
        card = table.shoe.draw_card(visible=True)
        table.dealer.hand.add_card(card)
        # Second round
        for player in table.active_players:
            card = table.shoe.draw_card(visible=True)
            player.hand.add_card(card)
            blackjack.ui.display_player(player)
        # Second round — Hole card
        if self.ruleset.DEALER_RECEIVES_HOLE_CARD:
            card = table.shoe.draw_card(visible=False)
            table.dealer.hand.add_card(card)
            if self.ruleset.DEALER_REVEALS_BLACKJACK_HAND:
                if table.dealer.hand.score == blackjack.score.TARGET_SCORE:
                    table.dealer.hand.reveal_all_cards()
        blackjack.ui.display_dealer(table.dealer)

    def _interact_with_player(self, table, player):
        """Deal more cards to given player as requested."""
        print('Interacting with player "{}"…'.format(player))
        while True:
            blackjack.ui.display_player(player)
            if player.hand.score > blackjack.score.TARGET_SCORE:
                print('Player\'s hand has gone bust with {} points!'.format(
                    player.hand.score), color='red')
                break
            key = blackjack.ui.ask('[h]it or [s]tand?', choices=['h', 's'], default='h')
            # Hit
            if key == 'h':
                card = table.shoe.draw_card(visible=True)
                player.hand.add_card(card)
                print('Player hit and received a "{}".'.format(card))
                continue
            # Stand
            if key == 's':
                print('Player stands.')
                break

    def _interact_with_dealer(self, table, dealer):
        """Deal more cards to given dealer as requested."""
        print('Interacting with dealer…')
        if not self.ruleset.DEALER_RECEIVES_HOLE_CARD:
            dealer.hand.add_card(table.shoe.draw_card(visible=True))
        dealer.hand.reveal_all_cards()
        blackjack.ui.display_dealer(dealer)
        while True:
            if dealer.hand.score > blackjack.score.TARGET_SCORE:
                print('Dealer has gone bust with {} points'.format(
                    dealer.hand.score), color='red')
                break
            if dealer.hand.score >= blackjack.score.MINIMUM_DEALER_SCORE:
                print('Dealer stands.')
                break
            card = table.shoe.draw_card(visible=True)
            dealer.hand.add_card(card)
            print('Dealer hit and received a "{}".'.format(card))
            blackjack.ui.display_dealer(dealer)

    def _pay_gains(self, table):
        """Pay every winning players."""
        print('Paying gains…')
        print('Dealer has {} points with {} cards.'.format(
            table.dealer.hand.score, len(table.dealer.hand)), color='white')
        for player in table.active_players:
            outcome, _ = blackjack.score.compare_hands(player.hand, table.dealer.hand)
            if outcome == blackjack.score.BUST:
                chip_count = 0
                print('Player "{}" busted with {} points.'.format(
                    player, player.hand.score), color='red')
            if outcome == blackjack.score.LOOSE:
                chip_count = 0
                print('Player "{}" loses with {} points on {} cards.'.format(
                    player, player.hand.score, len(player.hand)), color='red')
            if outcome == blackjack.score.PUSH:
                chip_count = 0
                print('Player "{}" is on tie with {} points on {} cards and gets his wager back.'.format(
                    player, player.hand.score, len(player.hand)), color='yellow')
                chip_count += player.hand.wager
            if outcome == blackjack.score.WIN:
                chip_count = player.hand.wager
                print('Player "{}" wins with {} points on {} cards and earns {} more chips.'.format(
                    player, player.hand.score, len(player.hand), chip_count), color='green')
                chip_count += player.hand.wager
            if outcome == blackjack.score.BLACKJACK:
                chip_count = int(player.hand.wager * self.ruleset.BLACKJACK_PAYOUT_RATIO)
                print('Player "{}" does Blackjack and earns {} more chips'.format(
                    player, chip_count), color='green')
                chip_count += player.hand.wager
            player.earn(chip_count)

    def _cleanup(self, table):
        """Drop all cards on table."""
        print('Cleaning table…')
        for player in table.active_players:
            player.drop_hand()
        table.dealer.drop_hand()
        table.shoe.reload()

