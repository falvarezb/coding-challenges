# -*- coding: utf-8 -*-
import numpy as np

"""
    Given an array 'arr' containing k distinct numbers taken from 1,2 ... n with k < n, 
    find the n - k missing numbers
"""


def solution1(arr, n):
    return int(n * (n + 1) / 2 - sum(arr))


def solution_n(arr, n):
    arr_sorted = sorted(arr)
    misses = list()

    if arr_sorted[0] != 1:
        misses.extend(list(range(1, arr_sorted[0])))

    for i in range(len(arr)-1):
        if arr_sorted[i]+1 != arr_sorted[i+1]:
            misses.extend(list(range(arr_sorted[i]+1, arr_sorted[i+1])))

    if arr_sorted[-1] != n:
        misses.extend(list(range(arr_sorted[-1] + 1, n + 1)))

    return misses


def solution_n_optimised(arr, n):
    bitset = np.ones(n)
    for i in range(0, len(arr)):
        bitset[arr[i]-1] = 0

    return list(np.nonzero(bitset)[0]+1)


if __name__ == '__main__':

    import timeit

    n = 10000000
    # By construction, the missing number is max/2+1
    test_data = list(range(1, int(n / 2))) + list(range(int(n / 2) + 1, n + 1))
    print(solution1(test_data, n))
    print(solution_n(test_data, n))
    print(solution_n_optimised(test_data, n))

    t1 = timeit.repeat(lambda: solution1(test_data, n), repeat=3, number=1)
    print(f't1: {t1} sec') # [0.05796466600440908, 0.058634756998799276, 0.05945016899931943]
    tn = timeit.repeat(lambda: solution_n(test_data, n), repeat=3, number=1)
    print(f'tn: {tn} sec')  # [1.6984177570047905, 1.6123321470004157, 1.627043018997938]
    tn_optimised = timeit.repeat(lambda: solution_n_optimised(test_data, n), repeat=3, number=1)
    print(f'tn_optimised: {tn_optimised} sec')  # [1.7067252099950565, 1.6756674749995, 1.654086376001942]
