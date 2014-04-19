"""Card and Desk object definitions."""

import itertools


class Card(object):
    """A playing card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = '{} of {}s'.format(self.rank, self.suit)
        self.visible = True

    def __str__(self):
        return self.name if self.visible else '<hidden>'

    def __repr__(self):
        txt = '<Card "{}" face {}>'.format(
            self.name, 'up' if self.visible else 'down')
        return txt


class Deck(list):
    """A standard deck of 52 playing cards."""

    def __init__(self):
        """Build all 52 cards in deck."""
        suits = ['Spade', 'Heart', 'Diamond', 'Club']
        ranks = [
            'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
            'Jack', 'Queen', 'King',
        ]
        combinations = itertools.product(suits, ranks)
        cards = (Card(suit, rank) for suit, rank in combinations)
        self.extend(cards)

    def __repr__(self):
        txt = '<Deck of {} cards>'.format(len(self))
        return txt

