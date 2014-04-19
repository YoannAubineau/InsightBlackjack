"""Everything about counting points."""

import functools
import itertools


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


TARGET_SCORE = 21
MINIMUM_DEALER_SCORE = 17


def score_from_hand(hand):
    """Return best score from given hand or None if unknown.

    If a hand contains at least one Ace, it may have multiple scores. For
    example, a hand with an Ace and a 3 may be scored 4 (1 + 3) or 14 (11 +
    3). In that case, we say that the hand is best scored a "soft" 14.
    However, another hand with an Ace, a 3 and Jack has only one score of
    "hard" 14 (1 + 3 + 10).

    The best score for a given hand is thus the higher score that is lower or
    equal to 21. Otherwise, it is the closest score to 21 which.
    """
    scores = []
    card_values = [values_from_card(card) for card in hand]
    value_combinations = itertools.product(*card_values)
    for value_combination in value_combinations:
        score = sum(value_combination)
        scores.append(score)
    best_score = (safe_max(s for s in scores if s <= TARGET_SCORE)
               or safe_min(s for s in scores if s > TARGET_SCORE))
    return best_score


def _safe_operation(func, values):
    """Apply given function on values or return None if no values.

    Note that `values` may be an iterator over a large sequence of values that
    may not all fit into memory. This is why it is prefered to check only if
    the first value exists, in order to handle the special case of returning
    None on an empty sequence.
    """
    try: next_value = next(iter(values))
    except StopIteration:
        return None
    values = itertools.chain([next_value], values)
    r = func(values)
    return r


safe_min = functools.partial(_safe_operation, min)
safe_max = functools.partial(_safe_operation, max)

