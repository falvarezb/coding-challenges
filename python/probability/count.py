"""
                                    Without repetition                                    With Repetition
    Ordered (Permutations)          n * (n - 1) * ... * (n - r + 1) = n! / (n - r)!       n^r

    Non-ordered (Combinations)      n! / (n - r)! / r! ≡ (n r)                            (n + r - 1)! / (n - 1)! / r! ≡  (n+r-1 n-1)

"""

from itertools import product, permutations, combinations, combinations_with_replacement
from math import factorial

"""
PERMUTATIONS
"""


def count_permutations_without_repetition(n, r):
    return factorial(n) // factorial(n - r)


def enumerate_permutations_without_repetition(elements, r):
    return list(permutations(elements, r))


def count_permutations_with_repetition(n, r):
    return n**r


def enumerate_permutations_with_repetition(elements, r):
    return list(product(elements, repeat=r))


"""
COMBINATIONS
"""


def count_combinations_without_repetition(n, r):
    return factorial(n) // (factorial(n - r) * factorial(r))


def enumerate_combinations_without_repetition(elements, r):
    return list(combinations(elements, r))


def count_combinations_with_repetition(n, r):
    return factorial(n + r - 1) // (factorial(n - 1) * factorial(r))


def enumerate_combinations_with_repetition(elements, r):
    return list(combinations_with_replacement(elements, r))

