# -*- coding: utf-8 -*-

import functools
import time

"""
Number of ways to climb n > 0 stairs when it is possible to take 1,2 or 3 steps at a time

This problem can be formulated in a more generic way as:

enumerate all permutations with repetition of [1,2,3] such that the sum of its elements equals n
"""


def enumerate_conditional_permutations(n: int, elems: list, f: 'list of lists') -> 'list of lists':
    """
    Enumerate all permutations with repetition of up to 'n' elements that satisfy the
    condition expressed by the function 'f'

    Example:
    - n = 3
    - elems = [1,2]
    - f = lambda x: sum(x) == 3 (the sum of the elements of the permutation equals 4)

    The algorithm in action:

    length    permutations                           solutions
    0         [[]]                                   []
    1         [[1],[2]]                              []
    2         [[1,1],[2,1],[1,2],[2,2]]              [[2,1],[1,2]]
    3         [[1,1,1],[2,1,1],[1,2,1],[2,2,1],      [[2,1],[1,2],[1,1,1]]
               [1,1,2],[2,1,2],[1,2,2],[2,2,2]]
    """
    solutions = []
    permutations = [[]]

    # each iteration adds a new element to the previous permutations
    for _ in range(n):
        new_permutations = []
        for elem in elems:
            for permutation in permutations:
                new_permutation = permutation+[elem]
                if f(new_permutation):
                    solutions.append(new_permutation)
                new_permutations.append(new_permutation)
        permutations = new_permutations
    return solutions


def enumerate_solutions(n, elems):
    """
    Function tailored to solve the stairs problem
    (using dynamic programming with bottom-up memoisation)

    This function is an optimisation of 'enumerate_conditional_permutations' for a specific
    value of 'f' (lambda permutation: sum(permutation) == n) and for a specific type of elements (int)

    Note: here 'n' is the sum of the elements of the permutation, not the number of elements in the permutation

    Example:
    - n = 3
    - elems = [1,2]

    The algorithm in action:

    sum       permutations
    0         [[[]]]
    1         [[[]],[[1]]]
    2         [[[]],[[1]],[[1,1],[2]]]
    3         [[[]],[[1]],[[1,1],[2]],[[1,1,1],[2,1],[1,2]]]

    and the solution is the last element of the final list: [[1,1,1],[2,1],[1,2]]

    Obviously, the solution is the same as the generic formulation but the number of intermediate
    permutations that needs to be calculated is far less

    """

    permutations = [[[]]]

    for j in range(1, n + 1):
        new_permutations = []
        allowed_elems = [i for i in elems if i <= j]
        for elem in allowed_elems:
            for permutation in permutations[j - elem]:
                new_permutations.append(permutation+[elem])
        permutations.append(new_permutations)
    return permutations[n]


def enumerate_solutions_recursive(n, elems):
    """
    Recursive version of 'enumerate_solutions'
    """

    if n == 0:
        return [[]]

    allowed_elems = [i for i in elems if i <= n]
    permutations = []
    for j in allowed_elems:
        permutations += ([i+[j]
                          for i in enumerate_solutions_recursive(n-j, elems)])
    return permutations


def enumerate_optimal_solutions(n, elems):
    """
    Version of 'enumerate_solutions' to retrieve only the optimal solutions.
    Optimal solutions are those permutations with the minimum number of elements
    """

    optimal_permutations = []

    for j in range(1, n + 1):
        if j in elems:
            optimal_permutations.append([[j]])
        else:
            new_permutations = []
            allowed_elems = [elem for elem in elems if elem < j]
            for elem in allowed_elems:
                for permutation in optimal_permutations[j - elem - 1]:
                    new_permutations.append(permutation+[elem])
            if new_permutations:
                min_length = min([len(x) for x in new_permutations])
                optimal_new_permutation = []
                for new_permutation in new_permutations:
                    if len(new_permutation) == min_length:
                        optimal_new_permutation.append(new_permutation)
                optimal_permutations.append(optimal_new_permutation)
            else:
                optimal_permutations.append([])
    return optimal_permutations[n-1]


def enumerate_unique_optimal_solutions(n, elems):
    """
    Version of 'enumerate_optimal_solutions' that discards all permutations of the same solution
    """
    solutions = enumerate_optimal_solutions(n, elems)
    return remove_permutations(solutions)



@functools.lru_cache()
def count_solutions_recursive(n, values):
    """
    recursive solution accepting any random steps
    """

    if n == 0:
        return 1

    allowed_values = [i for i in values if i <= n]
    return sum([count_solutions_recursive(n - i, values) for i in allowed_values])


def count_solutions_dp_bottom_up(n):
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


def count_solutions_dp_top_down(n):
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


def remove_permutations(ls: 'list of lists') -> 'list of lists':
    """
    given a list of lists, this function returns a new list without permutations

    Example:

    [[2,1,3], [3,1,2], [1,1]] -> [[1,2,3], [1,1]]
    """
    new_list = []
    for l in ls:
        l = sorted(l)
        if l not in new_list:
            new_list.append(l)
    return new_list


if __name__ == '__main__':

    def main():
        import timeit        
        n = 30
        values = tuple([1, 2, 3])

        print(timeit.repeat(lambda: count_combinations_recursive(n, values), repeat=3, number=1))
        print(timeit.repeat(lambda: count_combinations_dp_bottom_up(n), repeat=3, number=1))
        print(timeit.repeat(lambda: count_combinations_dp_top_down(n), repeat=3, number=1))

        """
        Without lru_cache:

        [81.46017726]
        [1.0622000004900656e-05, 7.500999998910629e-06, 7.085000007123199e-06]
        [2.9890999996950995e-05, 4.6634000000267406e-05, 3.5531999998283936e-05]

        With lru_cache:
        [9.587700000000116e-05, 7.820000000012539e-07, 4.080000000003525e-07]
        [9.722000000000203e-06, 7.455999999999435e-06, 7.037000000001403e-06]
        [6.505399999999842e-05, 4.275000000000112e-05, 2.6471000000000133e-05]
        """

    main()

# print(count_combinations_dp_bottom_up(n))
# print(count_combinations_dp_top_down(n))
# print(count_combinations_recursive(n))
# print(enumerate_combinations_dp(n))
# print(enumerate_combinations_recursive(n))
