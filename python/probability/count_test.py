from count import *


def test_count_permutations_without_repetition():
    assert count_permutations_without_repetition(4, 2) == 12

def test_enumerate_permutations_without_repetition():
    assert enumerate_permutations_without_repetition('ABCD', 2) == [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'C'), ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'A'), ('D', 'B'), ('D', 'C')]

def test_count_permutations_with_repetition():
    assert count_permutations_with_repetition(4, 2) == 16

def test_enumerate_permutations_with_repetition():
    assert enumerate_permutations_with_repetition('ABCD', 2) == [('A', 'A'), ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'C'), ('C', 'D'), ('D', 'A'), ('D', 'B'), ('D', 'C'), ('D', 'D')]


def test_count_combinations_without_repetition():
    assert count_combinations_without_repetition(4, 2) == 6

def test_enumerate_combinations_without_repetition():
    assert enumerate_combinations_without_repetition('ABCD', 2) == [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]

def test_count_combinations_with_repetition():
    assert count_combinations_with_repetition(4, 2) == 10

def test_enumerate_combinations_with_repetition():
    assert enumerate_combinations_with_repetition('ABCD', 2) == [('A', 'A'), ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'C'), ('C', 'D'), ('D', 'D')]
