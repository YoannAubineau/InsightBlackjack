"""Player object definitions."""

import blackjack.card


class NoEnoughChip(Exception):
    """Player wanted to bet more chips than he owns."""
    pass


class Player(object):
    """A player with chips and one hand of playing cards."""

    def __init__(self, name, chip_count):
        self.name = name
        self.chip_count = chip_count
        self.hand = None

    def __str__(self):
        return self.name

    def bet(self, chip_count):
        """Bet given amount of chips if possible."""
        if chip_count > self.chip_count:
            raise NoEnoughChip()
        self.chip_count -= chip_count
        self.hand.wager = chip_count

    def earn(self, chip_count):
        """Receive given amount of chips."""
        self.chip_count += chip_count

    def drop_hand(self):
        """Empty hand completely."""
        self.hand = None

    def __repr__(self):
        txt = '<Player "{}" with {} cards and {} chips>'.format(
            self.name, len(self.hand or []), self.chip_count)
        return txt

