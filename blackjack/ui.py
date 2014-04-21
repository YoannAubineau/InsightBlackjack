"""Text-based user-interface."""

import builtins
import sys
import termcolor


def print(msg, color='grey'):
    """Display a colored message."""
    msg = termcolor.colored(msg, color=color, attrs=['bold'])
    builtins.print(msg)


ORDINAL_FROM_INDEX = {
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
}

def display_player(player, only_hand=None):
    """Display player's hand and wealth."""
    # Display player with no cards
    if len(player.hands) == 0:
        lines = ['Player "{}" has {} remaining chips.'.format(
            player.name, player.chip_count)]
    # Display player with 1 hand
    if len(player.hands) == 1:
        lines = ['Player "{}" has {} cards and {} remaining chips:'.format(
            player.name, len(player.hands[0]), player.chip_count)]
        for card in player.hands[0]:
            lines.append('  Card "{}"'.format(card))
    # Display player with multiple hands
    if len(player.hands) > 1:
        lines = ['Player "{}" has {} hands and {} remaining chips:'.format(
            player.name, len(player.hands), player.chip_count)]
        for i, hand in enumerate(player.hands):
            if only_hand and hand != only_hand:
                continue
            lines.append('  {} hand with {} cards:'.format(
                ORDINAL_FROM_INDEX[i + 1].capitalize(), len(hand)))
            for card in hand:
                lines.append('    Card "{}"'.format(card))
    txt = '\n'.join(lines)
    print(txt, color='white')


def display_dealer(dealer):
    """Display dealer's hand."""
    lines = ['Dealer has {} cards:'.format(len(dealer.hand or []))]
    for card in dealer.hand or []:
        lines.append('  Card "{}"'.format(card))
    txt = '\n'.join(lines)
    print(txt, color='white')


def ask(msg, type=None, choices=None, default=None):
    """Prompt user for some action and return his decision."""

    # Check arguments consistency
    if default and type:
        try: value = type(default)
        except ValueError:
            raise ValueError('default value cannot be casted into {}'.format(type))
    if default and choices:
        if default not in choices:
            raise ValueError('default value not in choices')

    # Prepare prompt message
    msg = ''.join([
        msg,
        ' ({})'.format('/'.join(choices)) if choices else '',
        ' (default={})'.format(default) if default else '',
        ': ',
    ])
    msg = termcolor.colored(msg, color='cyan', attrs=['bold'])

    # Prompt user until valid choice is made.
    while True:
        sys.stdout.write(msg)
        value = input()
        if default and not value:
            value = default
        if type:
            try: value = type(value)
            except ValueError:
                print('should be of type {}'.format(type))
                continue
        if choices:
            if not value in choices:
                print('not valid choice!')
                continue
        return value

