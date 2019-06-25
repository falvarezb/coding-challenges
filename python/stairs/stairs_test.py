# -*- coding: utf-8 -*-

from stairs_solution import *


# ==== FUNCTIONAL TESTING ======

def test_stairs_8():
    stairs = 8
    assert count_combinations_recursive(stairs) == 81
    assert count_combinations_dp_bottom_up(stairs) == 81
    assert count_combinations_dp_top_down(stairs) == 81
    assert count_optimal_combinations_recursive(stairs) == 3
    assert enumerate_optimal_combinations_dp(stairs) == [[3,3,2], [3,2,3], [2,3,3]]