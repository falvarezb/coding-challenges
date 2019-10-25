# -*- coding: utf-8 -*-

from random import choice, sample
from hypothesis import given
import hypothesis.strategies as st
from stairs_solution import *


# ==== FUNCTIONAL TESTING ======

def test_count_combinations_recursive_generic():

    assert count_combinations_recursive_generic(1, [1, 2, 3]) == 1
    assert count_combinations_recursive_generic(2, [1, 2, 3]) == 2
    assert count_combinations_recursive_generic(3, [1, 2, 3]) == 4
    assert count_combinations_recursive_generic(4, [1, 2, 3]) == 7
    assert count_combinations_recursive_generic(8, [1, 2, 3]) == 81
    assert count_combinations_recursive_generic(5, [2, 4]) == 0
    assert count_combinations_recursive_generic(1, [2, 4]) == 0


def test_count_combinations_dp_bottom_up():

    assert count_combinations_dp_bottom_up(1) == 1
    assert count_combinations_dp_bottom_up(2) == 2
    assert count_combinations_dp_bottom_up(3) == 4
    assert count_combinations_dp_bottom_up(4) == 7
    assert count_combinations_dp_bottom_up(8) == 81


def test_count_combinations_dp_top_down():

    assert count_combinations_dp_top_down(1) == 1
    assert count_combinations_dp_top_down(2) == 2
    assert count_combinations_dp_top_down(3) == 4
    assert count_combinations_dp_top_down(4) == 7
    assert count_combinations_dp_top_down(8) == 81


def test_enumerate_combinations_recursive_generic():

    assert enumerate_combinations_recursive_generic(1, [1, 2, 3]) == [[1]]
    assert enumerate_combinations_recursive_generic(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_combinations_recursive_generic(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_combinations_recursive_generic(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_combinations_recursive_generic(5, [2, 4]) == []
    assert enumerate_combinations_recursive_generic(1, [2, 4]) == []


def test_enumerate_combinations_dp_bottom_up_generic():

    assert enumerate_combinations_dp_bottom_up_generic(1, [1, 2, 3]) == [[1]]
    assert enumerate_combinations_dp_bottom_up_generic(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_combinations_dp_bottom_up_generic(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_combinations_dp_bottom_up_generic(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_combinations_dp_bottom_up_generic(5, [2, 4]) == []
    assert enumerate_combinations_dp_bottom_up_generic(1, [2, 4]) == []


def test_enumerate_combinations_dp_bottom_up():

    assert enumerate_combinations_dp_bottom_up(1) == [[1]]
    assert enumerate_combinations_dp_bottom_up(2) == [[1, 1], [2]]
    assert enumerate_combinations_dp_bottom_up(
        3) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_combinations_dp_bottom_up(4) == [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]


def test_stairs_8():
    stairs = 8
    steps = [1, 2, 3]
    assert count_combinations_recursive_generic(stairs, steps) == 81
    assert count_combinations_dp_bottom_up(stairs) == 81
    assert count_combinations_dp_top_down(stairs) == 81
    assert enumerate_optimal_combinations_dp_bottom_up_generic(
        stairs, steps) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(stairs, steps) == [
        [2, 3, 3]]


def test_enumerate_optimal_combinations_dp_bottom_up_generic():
    assert enumerate_optimal_combinations_dp_bottom_up_generic(1, [1, 3]) == [[1]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(2, [1, 3]) == [[1, 1]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [1, 3]) == [[3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(4, [1, 3]) == [[3, 1], [1, 3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(8, [1, 4, 5]) == [[4, 4]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(8, [1, 2, 3]) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(
        12, [1, 3, 5]) == [[1, 1, 5, 5], [1, 3, 3, 5], [3, 3, 3, 3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(1, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(7, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [2, 5]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(4, [2]) == [[2, 2]]


# ==== PROPERTY-BASED TESTING ======

def stairs_strategy(max_stairs):
    """
     Generator of tuples of number of stairs 'n' and list of steps 'values':
        - 'n' is a value such that 0 < n <= max_stairs
        - steps[i] is value such that 0 < steps[i] <= n for all 0 < i <= n
    """

    n = choice(range(1, max_stairs + 1))
    i = choice(range(1, n + 1))
    return n, sample(range(1, n + 1), i)

def list1_subset_list2(list1, list2):
    """
    list1 and list2 are list of lists of ints
    """

    return all(l in list2 for l in list1)


def test_list():
    assert list1_subset_list2([[1, 1, 1, 4]], [[1, 1, 1, 4], [2, 1, 4]])

@given(st.builds(stairs_strategy, st.integers(10, 25)))
def test_hypothesis(t):
    assert count_combinations_recursive_generic(t[0], t[1]) == len(enumerate_combinations_recursive_generic(t[0], t[1]))
    assert enumerate_combinations_dp_bottom_up_generic(t[0], t[1]) == enumerate_combinations_recursive_generic(t[0], t[1])
    assert list1_subset_list2(enumerate_optimal_combinations_dp_bottom_up_generic(t[0], t[1]), enumerate_combinations_dp_bottom_up_generic(t[0], t[1]))
    assert list1_subset_list2(enumerate_optimal_combinations_dp_without_permutation(t[0], t[1]), enumerate_optimal_combinations_dp_bottom_up_generic(t[0], t[1]))
