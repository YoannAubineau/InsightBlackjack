"""Command-line interface for setting-up and starting a game."""

import argparse
import copy
import sys

import blackjack.card
import blackjack.game
import blackjack.player
import blackjack.score


def play(ruleset, player_infos):
    """Setup and play the game."""

    # Prepare card shoe
    shoe_type = blackjack.card.Shoe
    if ruleset.AUTO_SHUFFLING_SHOE:
        shoe_type = blackjack.card.ShufflingShoe
    cards = ruleset.DECK_COUNT_IN_SHOE * blackjack.card.Deck()
    cards = [copy.copy(card) for card in cards]  # instantiate new cards
    shoe = shoe_type(cards)

    # Prepare table
    dealer = blackjack.player.Dealer()
    players = [blackjack.player.Player(name, chip_count)
        for name, chip_count in player_infos]
    table = blackjack.player.Table(shoe, dealer, players)

    # Start playing
    game = blackjack.game.Game(ruleset)
    table.play(game)

    return table, game


def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Text-based blackjack card game.')
    parser.add_argument('--ruleset', choices=blackjack.game.ruleset_map.keys(), default='insight',
        help='''Use this option to select the ruleset to be used while
        playing.  Possible choices are "basic", "european", "american" or
        "insight". If this option is not set, it defaults to "insight."''')
    parser.add_argument('player_names', nargs='+', metavar='NAME',
        help='''Give each players\'s name as arguments. There must be at least
        1 player. Maximum number of players depends on choosen ruleset.''')
    args = parser.parse_args()

    # Select ruleset
    ruleset = blackjack.game.ruleset_map[args.ruleset]()

    # Register players
    STARTING_CHIP_COUNT = 100  #XXX should be set via command line for each player
    player_infos = [(name, STARTING_CHIP_COUNT) for name in args.player_names]
    if len(player_infos) > ruleset.MAXIMUM_PLAYER_COUNT:
        print('This ruleset allows up to {} concurrent players.'.format(ruleset.MAXIMUM_PLAYER_COUNT))
        sys.exit(1)

    # Have fun
    play(ruleset, player_infos)

