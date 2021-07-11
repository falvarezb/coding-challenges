from powerset.powerset_solution import *


def test_emptyset():
    assert powerset(0) == [[]]


def test_2elem():
    assert powerset(2) == [[], [1], [2], [1, 2]]


def test_3elem():
    assert powerset(3) == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
