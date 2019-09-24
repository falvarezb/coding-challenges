# -*- coding: utf-8 -*-

from stairs_solution import *


# ==== FUNCTIONAL TESTING ======

def test_stairs_8():
    stairs = 8
    steps = [1, 2, 3]
    assert count_combinations_recursive(stairs) == 81
    assert count_combinations_dp_bottom_up(stairs) == 81
    assert count_combinations_dp_top_down(stairs) == 81
    assert enumerate_optimal_combinations_dp(stairs, steps) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(stairs, steps) == [[2, 3, 3]]

def test_enumerate_optimal_combinations_dp():
    assert enumerate_optimal_combinations_dp(1, [1, 3]) == [[1]]
    assert enumerate_optimal_combinations_dp(2, [1, 3]) == [[1, 1]]
    assert enumerate_optimal_combinations_dp(3, [1, 3]) == [[3]]
    assert enumerate_optimal_combinations_dp(4, [1, 3]) == [[3, 1], [1, 3]]
    assert enumerate_optimal_combinations_dp(8, [1, 4, 5]) == [[4, 4]]
    assert enumerate_optimal_combinations_dp(8, [1, 2, 3]) == [[3, 3, 2], [3, 2, 3], [2, 3, 3]]
    assert enumerate_optimal_combinations_dp_without_permutation(12, [1, 3, 5]) == [[1, 1, 5, 5], [1, 3, 3, 5], [3, 3, 3, 3]]
    assert enumerate_optimal_combinations_dp(1, [2, 4]) == []
    assert enumerate_optimal_combinations_dp(3, [2, 4]) == []
    assert enumerate_optimal_combinations_dp(7, [2, 4]) == []
    assert enumerate_optimal_combinations_dp(3, [2, 5]) == []
