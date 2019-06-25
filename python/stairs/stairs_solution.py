#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Number of ways to climb n stairs when it is possible to take 1,2 or 3 steps at a time
"""

import timeit


def count_combinations_recursive(n):
    """
    recursive solution
    """

    if n == 1:
        return 1  # (1)
    elif n == 2:
        return 2  # (1,1), (2)
    elif n == 3:
        return 4  # (1,1,1), (2,1), (1,2), (3)
    return count_combinations_recursive(n-1) + count_combinations_recursive(n-2) + count_combinations_recursive(n-3)


def count_combinations_dp_bottom_up(n):
    """
    dynamic programming solution with bottom-up memoisation
    """
    results = [0] * n
    results[0] = 1
    results[1] = 2
    results[2] = 4
    for i in range(3, n):
        results[i] = results[i-1] + results[i-2] + results[i-3]
    return results[n-1]


def count_combinations_dp_top_down(n):
    """
    dynamic programming solution with top-down memoisation
    """
    results = [0] * n

    def aux(i):
        if results[i - 1] == 0:
            if i == 1:
                results[i - 1] = 1
            elif i == 2:
                results[i - 1] = 2
            elif i == 3:
                results[i - 1] = 4
            else:
                results[i - 1] = aux(i - 1) + aux(i - 2) + aux(i - 3)
        return results[i - 1]
    return aux(n)


def enumerate_combinations_recursive(n):
    """
   recursive solution
   """

    if n == 1:
        return [[1]]
    elif n == 2:
        return [[1, 1], [2]]
    elif n == 3:
        return [[1, 1, 1], [2, 1], [1, 2], [3]]
    return [i+[1] for i in enumerate_combinations_recursive(n-1)] + [i+[2] for i in enumerate_combinations_recursive(n-2)] + [i+[3] for i in enumerate_combinations_recursive(n-3)]


def enumerate_combinations_dp(n):
    """
    dynamic programming solution with bottom-up memoisation
    """

    results = [[[1]], [[1, 1], [2]], [[1, 1, 1], [2, 1], [1, 2], [3]]]
    for j in range(3, n):
        results.append([i+[1] for i in results[j-1]] + [i+[2] for i in results[j-2]] + [i+[3] for i in results[j-3]])
    return results[n-1]


def enumerate_optimal_combinations_dp(n):
    """
    dynamic programming solution with bottom-up memoisation
    """

    results = [[[1]], [[2]], [[3]]]
    for j in range(3, n):
        x = j % 3
        results.append(([i+[1] for i in results[j-1]] if x == 0 else []) + ([i+[2] for i in results[j-2]] if x < 2 else []) + [i+[3] for i in results[j-3]])
    return results[n-1]


def count_optimal_combinations_recursive(n):
    """
    recursive solution
    """

    if n == 1:
        return 1  # (1)
    elif n == 2:
        return 1  # (2)
    elif n == 3:
        return 1  # (3)
    x = n % 3
    return (count_optimal_combinations_recursive(n-1) if x == 1 else 0) + (count_optimal_combinations_recursive(n-2) if x > 0 else 0) + count_optimal_combinations_recursive(n-3)


def count_optimal_combinations_dp_bottom_up(n):
    """
    dynamic programming solution with bottom-up memoisation
    """
    results = [0] * n
    results[0] = 1
    results[1] = 1
    results[2] = 1
    for i in range(3, n):
        x = i % 3
        results[i] = (results[i-1] if x == 0 else 0) + (results[i-2] if x < 2 else 0) + results[i-3]
    return results[n-1]


if __name__ == '__main__':
    n = 30

    print(timeit.repeat(lambda: count_combinations_recursive(n), repeat=1, number=1))
    print(timeit.repeat(lambda: count_combinations_dp_bottom_up(n), repeat=3, number=1))
    print(timeit.repeat(lambda: count_combinations_dp_top_down(n), repeat=3, number=1))

# print(count_combinations_dp_bottom_up(n))
# print(count_combinations_dp_top_down(n))
# print(count_combinations_recursive(n))
# print(enumerate_combinations_dp(n))
# print(enumerate_combinations_recursive(n))
