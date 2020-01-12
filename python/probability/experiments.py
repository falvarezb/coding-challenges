from random import choices, sample
from itertools import product
import numpy as np
from count import enumerate_permutations_with_repetition, count_combinations_without_repetition


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

    if(white_wanted > drawn):
        raise Exception("illegal argument, 'white_wanted' must be less or equal to 'drawn'")

    def aux(num_trials):
        bag = ['W'] * white + ['B'] * black
        trial = lambda: sample(bag, k=drawn).count('W') == white_wanted
        return sum(trial() for j in range(0, num_trials)) / num_trials
    return aux


def balls_draw_classical(white, black, drawn, white_wanted):

    if white_wanted > drawn:
        raise Exception("illegal argument, 'white_wanted' must be less or equal to 'drawn'")

    return count_combinations_without_repetition(white, white_wanted) * count_combinations_without_repetition(black, drawn - white_wanted) / count_combinations_without_repetition(white + black, drawn)    
