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


def hand_can_be_splited(hand):
    can_be_splitted = (
        len(hand) == 2 and
        values_from_card(hand[0]) == values_from_card(hand[1]) and
        not any(card.rank == 'Ace' for card in hand)
    )
    return can_be_splitted


BUST, LOOSE, PUSH, WIN, BLACKJACK = 0, 1, 2, 3, 4


def compare_hands(hand1, hand2):
    """Return outcome comparing two given hands.

    The outcome of comparing two hands is as follow:
      * a hand over 21 loose in any case, otherwise
      * the hand with greater score wins, or
      * if both hands score equally it is a "push" (ie. tied game)

    Also, a hand which score 21 points with only 2 cards is call a "blackjack"
    and wins over any other hand.
    """
    outcome1 = outcome2 = WIN

    # Examine hand1 independently
    score1 = score_from_hand(hand1)
    if score1 > TARGET_SCORE:
        outcome1 = BUST
    if score1 == TARGET_SCORE and len(hand1) == 2:
        outcome1 = BLACKJACK

    # Examine hand2 independently
    score2 = score_from_hand(hand2)
    if score2 > TARGET_SCORE:
        outcome2 = BUST
    if score2 == TARGET_SCORE and len(hand2) == 2:
        outcome2 = BLACKJACK

    # Resolve two BLACKJACKs
    if outcome1 == outcome2 == BLACKJACK:
        return PUSH, PUSH

    # Resolve one BLACKJACK
    if outcome1 == BLACKJACK:
        outcome2 = min(outcome2, LOOSE)
    if outcome2 == BLACKJACK:
        outcome1 = min(outcome1, LOOSE)

    # Compare scores
    if outcome1 == outcome2 == WIN:
        if score1 < score2:
            outcome1, outcome2 = LOOSE, WIN
        if score1 > score2:
            outcome1, outcome2 = WIN, LOOSE
        if score1 == score2:
            outcome1, outcome2 = PUSH, PUSH

    return outcome1, outcome2


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

