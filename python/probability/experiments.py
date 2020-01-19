from random import choices, sample
from itertools import product
import numpy as np
from count import enumerate_permutations_with_repetition, count_combinations_without_repetition, count_permutations_without_repetition


def dice_roll(num_trials, wanted_result):
    dice = range(1, 7)
    return choices(dice, k=num_trials).count(wanted_result)/num_trials


def two_dice_roll(num_trials, wanted_result):
    dice = range(1, 7)
    return list(np.array(choices(dice, k=num_trials)) + np.array(choices(dice, k=num_trials))).count(wanted_result)/num_trials


def two_dice_roll_classical(wanted_result):
    dice = range(1, 7)
    two_dice = enumerate_permutations_with_repetition(dice, 2)
    num_total_cases = len(list(two_dice))
    num_favourable_cases = list(map(lambda x: x[0] + x[1], two_dice)).count(wanted_result)

    return num_favourable_cases / num_total_cases


def balls_draw(white, black, drawn, white_wanted):
    """
    Example
    -------

    If 3 balls are “randomly drawn” from a bowl containing 6 white and 5 black balls, 
    what is the probability that one of the balls is white and the other two black?
    """

    if(white_wanted > drawn):
        raise Exception("illegal argument, 'white_wanted' must be less or equal to 'drawn'")

    def aux(num_trials):
        bag = ['W'] * white + ['B'] * black

        def trial():
            return sample(bag, k=drawn).count('W') == white_wanted

        return sum(trial() for j in range(0, num_trials)) / num_trials

    return aux


def balls_draw_classical(white, black, drawn, white_wanted):
    if white_wanted > drawn:
        raise Exception("illegal argument, 'white_wanted' must be less or equal to 'drawn'")

    return count_combinations_without_repetition(white, white_wanted) * count_combinations_without_repetition(black, drawn - white_wanted) / count_combinations_without_repetition(white + black, drawn)


def married_couples(num_couples, num_trials):
    """
    Example
    -------

    Probability that 10 married couples are seated at random at a round table, then no wife sits next to her husband.
    """

    def flatten(z):
        return [x for y in z for x in y]

    participants = flatten([[j*10, j*10 + 1] for j in range(num_couples)])

    def identify_couples_seated_together(participants):
        for j in range(len(participants) - 1):
            if abs(participants[j] - participants[j + 1]) == 1:
                return True

        return abs(participants[len(participants) - 1] - participants[0]) == 1

    def trial(participants):
        return identify_couples_seated_together(sample(participants, k=len(participants)))

    return 1 - sum(trial(participants) for j in range(0, num_trials)) / num_trials


def married_couples_theoretical(num_couples):
    """

    Probability that 10 married couples are seated at random at a round table, then no wife sits next to her husband.

    Steps:
    1. calculate probability that any of husbands sits next to his wife
    2. given that these events are not mutually exclusive (a couple sitting together does not prevent another one of sitting together),
    we need to use the inclusion-exclusion identity
    3. finally the wanted probability is the difference up to 1

    """

    def probK(n, m):
        """
        Probability that, given n couples A1, A2, ... , An, then the couples A1, A2, ... , Am (m <= n) sit together
        """

        num_arrangements_couples_sit_together = 2**m * count_permutations_without_repetition(2*n-m-1, 2*n-m-1)
        total_num_arrangements = count_permutations_without_repetition(2*n-1, 2*n-1)

        return num_arrangements_couples_sit_together/total_num_arrangements

    # inclusion-exclusion identity
    prob = 0
    for r in range(1, 10):
        prob += (-1)**(r+1) * count_combinations_without_repetition(num_couples, r) * probK(num_couples, r)

    return 1 - prob


def probK_generalization(n, m, k):
    """
    Probability that, given n groups A1, A2, ... , An, of k people each, then the couples A1, A2, ... , Am (m <= n) sit together
    """

    num_arrangements_members_same_group_sit_together = count_permutations_without_repetition(k, k)**m * count_permutations_without_repetition(k*n-m-1, k*n-m-1)
    total_num_arrangements = count_permutations_without_repetition(k*n-1, k*n-1)

    return num_arrangements_members_same_group_sit_together/total_num_arrangements

