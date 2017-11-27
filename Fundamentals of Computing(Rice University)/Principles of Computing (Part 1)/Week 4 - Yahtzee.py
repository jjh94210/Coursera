"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""
# By Jaehwi Cho

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    maximal_score = 0
    for dummy_dice in hand:
        temp_score = 0
        for dummy_index in range(len(hand)):
            if(dummy_dice == hand[dummy_index]):
                temp_score += dummy_dice
        if maximal_score < temp_score:
            maximal_score = temp_score
    return maximal_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = range(1, num_die_sides + 1, 1)
    all_free_dices = gen_all_sequences(outcomes, num_free_dice)
    total_score = 0
    for dummy_free_dice in all_free_dices:
        total_score += score(held_dice + dummy_free_dice)
    return float(total_score) / float(len(all_free_dices))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds_set = set([()])
    for dummy_index in range(len(hand)):
        temp_set = set()
        for partial_hold in all_holds_set:
            comp_hold_list = list(hand)
            for dummy_dice in partial_hold:
                comp_hold_list.remove(dummy_dice)
            for dummy_dice in comp_hold_list:
                new_hold = list(partial_hold)
                new_hold.append(dummy_dice)
                new_hold.sort()
                temp_set.add(tuple(new_hold))
        all_holds_set = all_holds_set.union(temp_set)
    return all_holds_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds_set = gen_all_holds(hand)
    final_expected_value = 0
    final_held_dice = tuple()
    for held_dice in all_holds_set:
        temp_expected_value = expected_value(held_dice, num_die_sides, len(hand) - len(held_dice))
        if temp_expected_value > final_expected_value:
            final_expected_value = temp_expected_value
            final_held_dice = held_dice
    return (final_expected_value, final_held_dice)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

# http://www.codeskulptor.org/#user43_JtcAawcbM73VnlV.py
