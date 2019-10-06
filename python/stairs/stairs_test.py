# -*- coding: utf-8 -*-

from stairs_solution import *


# ==== FUNCTIONAL TESTING ======

def test_stairs_gen():

    # assert count_combinations_recursive(0) == 0
    assert count_combinations_recursive_generic(1, [1, 2, 3]) == 1
    assert count_combinations_recursive_generic(2, [1, 2, 3]) == 2
    assert count_combinations_recursive_generic(3, [1, 2, 3]) == 4
    assert count_combinations_recursive_generic(4, [1, 2, 3]) == 7
    assert count_combinations_recursive_generic(8, [1, 2, 3]) == 81
    assert count_combinations_recursive_generic(5, [2, 4]) == 0
    assert count_combinations_recursive_generic(1, [2, 4]) == 0

def test_stairs_enum():

    assert enumerate_combinations_recursive_generic(1, [1, 2, 3]) == [[1]]
    assert enumerate_combinations_recursive_generic(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_combinations_recursive_generic(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_combinations_recursive_generic(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_combinations_recursive_generic(5, [2, 4]) == []
    assert enumerate_combinations_recursive_generic(1, [2, 4]) == []


def test_stairs_enum_generic():

    assert enumerate_combinations_dp_bottom_up_generic(1, [1, 2, 3]) == [[1]]
    assert enumerate_combinations_dp_bottom_up_generic(2, [1, 2, 3]) == [[1, 1], [2]]
    assert enumerate_combinations_dp_bottom_up_generic(3, [1, 2, 3]) == [[1, 1, 1], [2, 1], [1, 2], [3]]
    assert enumerate_combinations_dp_bottom_up_generic(4, [1, 2, 3]) == [[1, 1, 1, 1], [2, 1, 1], [1, 2, 1], [3, 1], [1, 1, 2], [2, 2], [1, 3]]
    assert enumerate_combinations_dp_bottom_up_generic(5, [2, 4]) == []
    assert enumerate_combinations_dp_bottom_up_generic(1, [2, 4]) == []

def test_stairs_8():
    stairs = 8
    steps = [1, 2, 3]
    assert count_combinations_recursive_generic(stairs, steps) == 81
    assert count_combinations_dp_bottom_up(stairs) == 81
    assert count_combinations_dp_top_down(stairs) == 81
    assert enumerate_optimal_combinations_dp_bottom_up_generic(stairs, steps) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(stairs, steps) == [[2, 3, 3]]

def test_enumerate_optimal_combinations_dp():
    assert enumerate_optimal_combinations_dp_bottom_up_generic(1, [1, 3]) == [[1]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(2, [1, 3]) == [[1, 1]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [1, 3]) == [[3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(4, [1, 3]) == [[3, 1], [1, 3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(8, [1, 4, 5]) == [[4, 4]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(8, [1, 2, 3]) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(12, [1, 3, 5]) == [[1, 1, 5, 5], [1, 3, 3, 5], [3, 3, 3, 3]]
    assert enumerate_optimal_combinations_dp_bottom_up_generic(1, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(7, [2, 4]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(3, [2, 5]) == []
    assert enumerate_optimal_combinations_dp_bottom_up_generic(4, [2]) == [[2, 2]]
