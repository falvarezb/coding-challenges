#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Number of ways to climb n > 0 stairs when it is possible to take 1,2 or 3 steps at a time
"""


def count_combinations_recursive_generic(n, values):
    """
    recursive solution accepting any random steps
    """

    if n == 0:
        return 1

    allowed_values = [i for i in values if i <= n]
    return sum([count_combinations_recursive_generic(n - i, values) for i in allowed_values])

    # if n == 1:
    #     return 1  # (1)
    # elif n == 2:
    #     return 2  # (1,1), (2)
    # elif n == 3:
    #     return 4  # (1,1,1), (2,1), (1,2), (3)
    # return count_combinations_recursive(n-1) + count_combinations_recursive(n-2) + count_combinations_recursive(n-3)


def count_combinations_dp_bottom_up(n):
    """
    dynamic programming solution with bottom-up memoisation
    """
    results = [0] * n
    results[0] = 1
    if n >= 2:
        results[1] = 2
    if n >= 3:
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


def enumerate_combinations_recursive_generic(n, values):
    """
   recursive solution accepting any random steps
   """

    if n == 0:
        return [[]]

    allowed_values = [i for i in values if i <= n]
    result = []
    for j in allowed_values:
        result += ([i+[j]
                    for i in enumerate_combinations_recursive_generic(n-j, values)])
    return result

    # if n == 1:
    #     return [[1]]
    # elif n == 2:
    #     return [[1, 1], [2]]
    # elif n == 3:
    #     return [[1, 1, 1], [2, 1], [1, 2], [3]]
    # return [i+[1] for i in enumerate_combinations_recursive(n-1)] + [i+[2] for i in enumerate_combinations_recursive(n-2)] + [i+[3] for i in enumerate_combinations_recursive(n-3)]


def enumerate_combinations_dp_bottom_up(n):
    """
    dynamic programming solution with bottom-up memoisation
    """

    results = [[[1]], [[1, 1], [2]], [[1, 1, 1], [2, 1], [1, 2], [3]]]
    for j in range(3, n):
        results.append([i+[1] for i in results[j-1]] + [i+[2]
                                                        for i in results[j-2]] + [i+[3] for i in results[j-3]])
    return results[n-1]


def enumerate_combinations_dp_bottom_up_generic(n, values):
    """
    dynamic programming solution with bottom-up memoisation accepting any random steps
    """

    results = [[[]]]

    for j in range(1, n + 1):
        new_combination = []
        allowed_values = [i for i in values if i <= j]
        for k in allowed_values:
            for i in results[j - k]:
                new_combination.append(i+[k])
        results.append(new_combination)
    return results[n]


def enumerate_optimal_combinations_dp_bottom_up_generic(n, values):
    """
    dynamic programming solution with bottom-up memoisation and accepting any random steps
    """

    results = []

    for j in range(1, n + 1):
        if j in values:
            results.append([[j]])
        else:
            new_combination = []
            allowed_values = [i for i in values if i < j]
            for k in allowed_values:
                for i in results[j - k - 1]:
                    new_combination.append(i+[k])
            if new_combination:
                min_length = min([len(x) for x in new_combination])
                optimal_new_combination = []
                for arr in new_combination:
                    if len(arr) == min_length:
                        optimal_new_combination.append(arr)
                results.append(optimal_new_combination)
            else:
                results.append([])
    return results[n-1]


def enumerate_optimal_combinations_dp_without_permutation(n, values):
    result = enumerate_optimal_combinations_dp_bottom_up_generic(n, values)
    new_list = []
    for j in result:
        j = sorted(j)
        if j not in new_list:
            new_list.append(j)
    return new_list


if __name__ == '__main__':

    def main():
        import timeit
        n = 30
        values = [1, 2, 3]

        print(timeit.repeat(lambda: count_combinations_recursive_generic(n, values), repeat=1, number=1))
        print(timeit.repeat(lambda: count_combinations_dp_bottom_up(n), repeat=3, number=1))
        print(timeit.repeat(lambda: count_combinations_dp_top_down(n), repeat=3, number=1))

    main()

# print(count_combinations_dp_bottom_up(n))
# print(count_combinations_dp_top_down(n))
# print(count_combinations_recursive(n))
# print(enumerate_combinations_dp(n))
# print(enumerate_combinations_recursive(n))
