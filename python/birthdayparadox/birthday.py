#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculate probability of 'num_people_same_bday' people having the same birthday in a group of 'num_people' people
"""

from random import choices
from collections import Counter
days_in_year = 365

def analytical_solution(num_people):
    """
    Analytical solution of particular case when num_people_same_bday = 2
    """
    possible_combinations = 1
    for i in range(days_in_year - num_people + 1, days_in_year + 1):
        possible_combinations *= i
    total_combinations = days_in_year ** num_people
    return 1 - possible_combinations / total_combinations


def simulation_solution(num_people):
    """
    Simulation of particular case when num_people_same_bday = 2
    """
    
    num_trials = 100000
    trial = lambda: len(set(choices(range(days_in_year), k=num_people))) < num_people    
    return sum(trial() for i in range(num_trials)) / num_trials


def generic_simulation_solution(num_people_same_bday, num_people):
    """
    The advantage of using a simulation to calculate the solution is that it can be generalised easily
    """

    num_trials = 100000
    trial = lambda: Counter(choices(range(days_in_year), k=num_people)).most_common(1)[0][1] >= num_people_same_bday
    return sum(trial() for i in range(num_trials)) / num_trials

if __name__ == '__main__':
    print(analytical_solution(38))
    print(simulation_solution(38))
    print(generic_simulation_solution(2, 38))