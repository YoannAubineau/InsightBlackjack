"""Card, Desk and Shoe object definitions."""

import collections
import itertools
import random


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


class Shoe(collections.Iterator):
    """A shoe to iterate over a set of playing cards."""

    def __init__(self, cards):
        for card in cards:
            card.visible = False
        self._cards = cards
        self.reload()

    def reload(self):
        self._card_iterator = iter(self._cards)
        self._remaining_card_count = len(self._cards)

    def shuffle(self):
        """Shuffle remaining cards."""
        remaining_cards = list(self._card_iterator)
        random.shuffle(remaining_cards)
        self._card_iterator = iter(remaining_cards)

    def __next__(self):
        """Return next card in shoe."""
        card = next(self._card_iterator)
        self._remaining_card_count -= 1
        return card

    def draw_card(self, visible=False):
        card = next(self)
        card.visible = visible
        return card

    def __len__(self):
        """Return number of remaining cards."""
        return self._remaining_card_count

    def __repr__(self):
        txt = '<Shoe with {} remaining cards>'.format(len(self))
        return txt


class ShufflingShoe(Shoe):
    """An auto-shuffling shoe."""

    def __next__(self):
        """Return next card in shoe after shuffling."""
        self.shuffle()
        card = super(ShufflingShoe, self).__next__()
        return card

    def __repr__(self):
        txt = '<Shuffling Shoe with {} remaining cards>'.format(len(self))
        return txt

