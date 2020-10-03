# -*- coding: utf-8 -*-

from random import choice, sample

import hypothesis.strategies as st
from hypothesis import given, example, note

from stairs_solution import *
from util import list1_equals_list2_except_order, list1_is_subset_of_list2


def test_enumerate_conditional_permutations():
    assert enumerate_conditional_permutations(1, [1, 2, 3], lambda l: sum(l) == 1) == [[1]]
    assert list1_equals_list2_except_order(enumerate_conditional_permutations(2, [1, 2, 3], lambda l: sum(l) == 2), [[1, 1], [2]])
    assert list1_equals_list2_except_order(enumerate_conditional_permutations(3, [1, 2, 3], lambda l: sum(l) == 3), [[1, 1, 1], [2, 1], [1, 2], [3]])
    assert list1_equals_list2_except_order(enumerate_conditional_permutations(4, [1, 2, 3], lambda l: sum(l) == 4), [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]])
    assert enumerate_conditional_permutations(5, [2, 4], lambda l: sum(l) == 5) == []
    assert enumerate_conditional_permutations(1, [2, 4], lambda l: sum(l) == 1) == []
    assert enumerate_conditional_permutations(1, [1, 2, 3], lambda l: sum(l) == 0) == []


def test_count_solutions_recursive():
    assert count_solutions_recursive(1, tuple([1, 2, 3])) == 1
    assert count_solutions_recursive(2, tuple([1, 2, 3])) == 2
    assert count_solutions_recursive(3, tuple([1, 2, 3])) == 4
    assert count_solutions_recursive(4, tuple([1, 2, 3])) == 7
    assert count_solutions_recursive(8, tuple([1, 2, 3])) == 81
    assert count_solutions_recursive(5, tuple([2, 4])) == 0
    assert count_solutions_recursive(1, tuple([2, 4])) == 0
    assert count_solutions_dp_bottom_up(0, [1, 2, 3]) == 1


def test_count_solutions_dp_bottom_up():
    assert count_solutions_dp_bottom_up(1, [1, 2, 3]) == 1
    assert count_solutions_dp_bottom_up(2, [1, 2, 3]) == 2
    assert count_solutions_dp_bottom_up(3, [1, 2, 3]) == 4
    assert count_solutions_dp_bottom_up(4, [1, 2, 3]) == 7
    assert count_solutions_dp_bottom_up(8, [1, 2, 3]) == 81
    assert count_solutions_dp_bottom_up(5, [2, 4]) == 0
    assert count_solutions_dp_bottom_up(1, [2, 4]) == 0
    assert count_solutions_dp_bottom_up(0, [1, 2, 3]) == 1


def test_count_solutions_dp_top_down():
    assert count_solutions_dp_top_down(1, [1, 2, 3]) == 1
    assert count_solutions_dp_top_down(2, [1, 2, 3]) == 2
    assert count_solutions_dp_top_down(3, [1, 2, 3]) == 4
    assert count_solutions_dp_top_down(4, [1, 2, 3]) == 7
    assert count_solutions_dp_top_down(8, [1, 2, 3]) == 81
    assert count_solutions_dp_top_down(5, [2, 4]) == 0
    assert count_solutions_dp_top_down(1, [2, 4]) == 0
    assert count_solutions_dp_top_down(0, [1, 2, 3]) == 1


def test_enumerate_solutions_recursive():
    assert enumerate_solutions_recursive(1, [1, 2, 3]) == [[1]]
    assert enumerate_solutions_recursive(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_solutions_recursive(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_solutions_recursive(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_solutions_recursive(5, [2, 4]) == []
    assert enumerate_solutions_recursive(1, [2, 4]) == []
    assert enumerate_solutions_recursive(0, [1, 2, 3]) == [[]]


def test_enumerate_solutions():
    assert enumerate_solutions(1, [1, 2, 3]) == [[1]]
    assert enumerate_solutions(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_solutions(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_solutions(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [
        1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_solutions(5, [2, 4]) == []
    assert enumerate_solutions(1, [2, 4]) == []
    assert enumerate_solutions(0, [1, 2, 3]) == [[]]


def test_stairs_8():
    stairs = 8
    steps = tuple([1, 2, 3])
    assert count_solutions_recursive(stairs, steps) == 81
    assert count_solutions_dp_bottom_up(stairs, steps) == 81
    assert count_solutions_dp_top_down(stairs, steps) == 81
    assert enumerate_optimal_solutions(stairs, steps) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_unique_optimal_solutions(stairs, steps) == [[2, 3, 3]]


def test_enumerate_optimal_solutions():
    assert enumerate_optimal_solutions(1, [1, 3]) == [[1]]
    assert enumerate_optimal_solutions(2, [1, 3]) == [[1, 1]]
    assert enumerate_optimal_solutions(3, [1, 3]) == [[3]]
    assert enumerate_optimal_solutions(4, [1, 3]) == [[3, 1], [1, 3]]
    assert enumerate_optimal_solutions(8, [1, 4, 5]) == [[4, 4]]
    assert enumerate_optimal_solutions(8, [1, 2, 3]) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_unique_optimal_solutions(
        12, [1, 3, 5]) == [[1, 1, 5, 5], [1, 3, 3, 5], [3, 3, 3, 3]]
    assert enumerate_optimal_solutions(1, [2, 4]) == []
    assert enumerate_optimal_solutions(3, [2, 4]) == []
    assert enumerate_optimal_solutions(7, [2, 4]) == []
    assert enumerate_optimal_solutions(3, [2, 5]) == []
    assert enumerate_optimal_solutions(4, [2]) == [[2, 2]]
    assert enumerate_solutions_recursive(0, [1, 2, 3]) == [[]]


def test_list_subset():
    assert list1_is_subset_of_list2([[1, 1, 1, 4]], [[1, 1, 1, 4], [2, 1, 4]])

# ==== PROPERTY-BASED TESTING ======


def stairs_strategy(max_stairs):
    """
     Generator of tuples of number of stairs 'n' and list of steps 'steps':
        - 'n' is a value such that 0 < n <= max_stairs
        - steps[i] is value such that 0 < steps[i] <= n for all 0 < i <= n
    """

    n = choice(range(1, max_stairs + 1))
    i = choice(range(1, n + 1))
    return n, tuple(sample(range(1, n + 1), i))


@given(st.builds(stairs_strategy, st.integers(5, 25)))
def test_solution_comparison(t):
    n = t[0]
    elems = t[1]
    assert count_solutions_recursive(n, elems) == len(enumerate_solutions_recursive(n, elems))
    assert enumerate_solutions(n, elems) == enumerate_solutions_recursive(n, elems)
    assert list1_is_subset_of_list2(enumerate_optimal_solutions(n, elems), enumerate_solutions(n, elems))
    assert list1_is_subset_of_list2(enumerate_unique_optimal_solutions(n, elems), enumerate_optimal_solutions(n, elems))
    assert count_solutions_recursive(n, elems) == count_solutions_dp_bottom_up(n, elems)
    assert count_solutions_recursive(n, elems) == count_solutions_dp_top_down(n, elems)


@given(st.builds(stairs_strategy, st.integers(4, 7)))
def test_enumerate_conditional_permutations_vs_enumerate_solutions(t):
    n = t[0]
    elems = t[1]
    list1 = enumerate_solutions(n, elems)
    list2 = enumerate_conditional_permutations(n, elems, lambda l: sum(l) == n)
    note(f"result:{list1_equals_list2_except_order(list1, list2)}")
    assert list1_equals_list2_except_order(list1, list2)
