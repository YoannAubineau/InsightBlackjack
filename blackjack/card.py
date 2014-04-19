"""Card object definition."""


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

