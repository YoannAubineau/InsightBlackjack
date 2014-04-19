"""Text-based user-interface."""

import builtins
import termcolor


def print(msg, color='grey'):
    """Display a colored message."""
    msg = termcolor.colored(msg, color=color, attrs=['bold'])
    builtins.print(msg)


def display_player(player):
    """Display player's hand and wealth."""
    # Display player with no cards
    if not player.hand or not len(player.hand):
        lines = ['Player "{}" has {} remaining chips.'.format(
            player.name, player.chip_count)]
    # Display player with cards
    else:
        lines = ['Player "{}" has {} cards and {} remaining chips:'.format(
            player.name, len(player.hand), player.chip_count)]
        for card in player.hand:
            lines.append('  Card "{}"'.format(card))
    txt = '\n'.join(lines)
    print(txt, color='white')


def display_dealer(dealer):
    """Display dealer's hand."""
    lines = ['Dealer has {} cards:'.format(len(dealer.hand or []))]
    for card in dealer.hand or []:
        lines.append('  Card "{}"'.format(card))
    txt = '\n'.join(lines)
    print(txt, color='white')

