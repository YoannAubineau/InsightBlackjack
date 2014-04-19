"""Everything about counting points."""


def values_from_card(card):
    """Return possible values of given card.

    Most cards have only one value: either the exact value of their rank, for
    numbered card, or exactly 10 for faced cards. Aces, on the contrary, have
    two possible values: 1 or 11. This is why this function returns a list of
    values instead of a single one. In case of an Ace, it is up to the caller
    to decide which value it wants to take into account, depending on if the
    hand is soft or hard.
    """
    try: values = [int(card.rank)]
    except ValueError:
        if card.rank in ('Jack', 'Queen', 'King'):
            values = [10]
        elif card.rank == 'Ace':
            values = [1, 11]
        else:
            raise Exception('unknown values for card "{}"'.format(card))
    return values

