# -*- coding: utf-8 -*-

import random
from mna_solution import solution1, solution_n, solution_n_optimised
from hypothesis import given
import hypothesis.strategies as st


# ==== FUNCTIONAL TESTING ======

def test_missing_element_is_4():
    assert solution1([1, 3, 2, 5], 5) == 4
    assert solution_n([1, 3, 2, 5], 5) == [4]
    assert solution_n_optimised([1, 3, 2, 5], 5) == [4]


def test_missing_element_is_4_6():
    assert solution_n([1, 3, 2, 5, 7, 8], 8) == [4, 6]
    assert solution_n_optimised([1, 3, 2, 5, 7, 8], 8) == [4, 6]


def test_missing_element_in_extremes():
    assert solution_n([4, 3, 2, 5, 7, 6], 8) == [1, 8]
    assert solution_n_optimised([4, 3, 2, 5, 7, 6], 8) == [1, 8]


def test_missing_element_in_consecutive_positions():
    assert solution_n([1, 2, 5, 8], 8) == [3, 4, 6, 7]
    assert solution_n_optimised([1, 2, 5, 8], 8) == [3, 4, 6, 7]


def test_missing_element_in_consecutive_positions_beginning():
    assert solution_n([3, 4, 5], 5) == [1, 2]
    assert solution_n_optimised([3, 4, 5], 5) == [1, 2]


def test_missing_element_in_consecutive_positions_end():
    assert solution_n([1, 2, 3], 5) == [4, 5]
    assert solution_n_optimised([1, 2, 3], 5) == [4, 5]


def test_missing_element_in_combination_above():
    assert solution_n([3, 5, 8], 10) == [1, 2, 4, 6, 7, 9, 10]
    assert solution_n_optimised([3, 5, 8], 10) == [1, 2, 4, 6, 7, 9, 10]


# ==== PROPERTY-BASED TESTING ======

def missing_number_array_strategy(n):
    k = random.choice(range(1, n + 1))
    return random.sample(range(1, n + 1), k=k), n


@given(st.builds(missing_number_array_strategy, st.integers(10, 15)))
def test_hypothesis(t):
    assert sorted(solution_n(t[0], t[1]) + t[0]) == list(range(1, t[1] + 1))
    assert solution_n(t[0], t[1]) == solution_n_optimised(t[0], t[1])
