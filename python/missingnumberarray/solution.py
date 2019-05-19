# -*- coding: utf-8 -*-

def solution1(arr, max_value):
    return int(max_value*(max_value+1)/2 - sum(arr))


def solution_n(arr, max_value):
    arr_sorted = sorted(arr)
    misses = list()

    if arr_sorted[0] != 1:
        misses.extend(list(range(1, arr_sorted[0])))

    for i in range(len(arr)-1):
        if arr_sorted[i]+1 != arr_sorted[i+1]:
            misses.extend(list(range(arr_sorted[i]+1, arr_sorted[i+1])))

    if arr_sorted[-1] != max_value:
        misses.extend(list(range(arr_sorted[-1]+1, max_value+1)))

    return misses

import numpy as np
def solution_n_optimised(arr, max_value):
    bitset = np.ones(max_value)
    for i in range(0, len(arr)):
        bitset[arr[i]-1] = 0

    return list(np.nonzero(bitset)[0]+1)


if __name__ == '__main__':

    import timeit

    MAX_VALUE = 10000000
    test_data = list(range(1, int(MAX_VALUE/2))) + list(range(int(MAX_VALUE/2)+1, MAX_VALUE+1))
    print(solution1(test_data, MAX_VALUE))
    print(solution_n(test_data, MAX_VALUE))
    print(solution_n_optimised(test_data, MAX_VALUE))


    t1 = timeit.repeat('solution1(test_data, MAX_VALUE)', globals=globals(), repeat=3, number=10)
    print(f't1: {t1}')
    tn = timeit.repeat('solution_n(test_data, MAX_VALUE)', globals=globals(), repeat=3, number=10)
    print(f'tn: {tn}')
    tn_optimised = timeit.repeat('solution_n_optimised(test_data, MAX_VALUE)', globals=globals(), repeat=3, number=10)
    print(f'tn_optimised: {tn_optimised}')
    