from count import *
from itertools import product


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

def test_count_numbers_with_fixed_digits_sum():
    """
    How many non-negative integer numbers are there below 10000 such that their sum of digits is equal to 9?

    This problem is similar to calculate the number of ways in which a set of 9 ones can be split into 4 groups!!
    (4 groups because all numbers below 10000 have at most 4 digits)
    """

    greatest_possible_digit = 9
    upper_bound = 10000
    digits_sum = 9
    num_digits = len(str(upper_bound-1))

    if digits_sum > 9:
        raise Exception(f"illegal argument: this test does not pass when the sum of digits is greater than {greatest_possible_digit} as no decimal position can contain {greatest_possible_digit+1} units")

    def brute_force_solution():
        count = 0
        for j in product(range(10), repeat=num_digits):
            if sum(j) == digits_sum:
                count += 1
        return count


    assert count_combinations_with_repetition(num_digits, digits_sum) == brute_force_solution()

