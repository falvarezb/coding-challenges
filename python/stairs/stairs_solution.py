# -*- coding: utf-8 -*-

import functools
from util import remove_permutations

"""
Number of ways to climb n > 0 stairs when it is possible to take 1,2 or 3 steps at a time

This problem can be formulated in a more generic way as:
enumerate all permutations with repetition of [1,2,3] such that the sum of its elements equals n

This problem is an example of combinatorial searching. From the book The Art of Programming:

there are five basic types of questions in combinatorial problems:
1. existence: are there any arrangements of a set of elements that conform to a given pattern?
2. construction: if so, can such arrangement be found quickly?
3. enumeration: how many different arrangements exist?
4. generation: can all arrangements be visited systematically?
5. optimisation: what arrangements maximise/minimise a given function (known as objective function)?

In the following functions, we use "count" instead of "enumeration", and "enumeration" instead of "generation"
"""


def enumerate_conditional_permutations(n: int, elems: list, f: 'list -> boolean') -> 'list of lists':
    """
    Enumerate all permutations with repetition of up to 'n' elements that satisfy the
    condition expressed by the function 'f'.

    Given that we cannot make any assumption about 'f', the only way to solve this problem is by using
    brute force: enumerate all possible permutations and apply f to each of them.

    We'll use this method as "test oracle" when doing property-based testing

    Example:
    - n = 3
    - elems = [1,2]
    - f = lambda x: sum(x) == 3 (the sum of the elements of the permutation equals 3)

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

    The solution is the same as the generic formulation but the number of intermediate
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
    return [solution+[elem] for elem in allowed_elems for solution in enumerate_solutions_recursive(n-elem, elems)]


def find_any_optimal_solution(n, elems):
    """
    Version of 'enumerate_solutions_recursive' restricted to finding 1 optimal solution
    """

    if n == 0:
        return []

    allowed_elems = [i for i in elems if i <= n]
    return min([solution+[elem] for elem in allowed_elems for solution in enumerate_solutions_recursive(n-elem, elems)], key=len, default=[])


def enumerate_optimal_solutions(n, elems):
    """
    Version of 'enumerate_solutions' to retrieve only the optimal solutions.
    Optimal solutions are those permutations with the minimum number of elements
    """

    if n == 0:
        return [[]]

    optimal_permutations = []

    for j in range(1, n + 1):
        if j in elems:
            optimal_permutations.append([[j]])
        else:
            new_permutations = []
            allowed_elems = [i for i in elems if i < j]
            for elem in allowed_elems:
                for permutation in optimal_permutations[j - elem - 1]:
                    new_permutations.append(permutation+[elem])
            if new_permutations:
                min_length = min([len(x) for x in new_permutations])
                optimal_permutations.append([j for j in new_permutations if len(j) == min_length])
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
    recursive solution
    """

    if n == 0:
        return 1

    allowed_values = [i for i in values if i <= n]
    return sum([count_solutions_recursive(n - i, values) for i in allowed_values])


def count_solutions_dp_bottom_up(n, elems):
    """
    dynamic programming solution with bottom-up memoisation
    """
    results = [0] * (n + 1)
    results[0] = 1

    for j in range(1, n + 1):
        allowed_elems = [i for i in elems if i <= j]
        results[j] = sum([results[j-elem] for elem in allowed_elems])
    return results[n]


def count_solutions_dp_top_down(n, elems):
    """
    dynamic programming solution with top-down memoisation
    """
    results = [0] * (n + 1)
    results[0] = 1

    def aux(j):
        if results[j] == 0:
            allowed_elems = [i for i in elems if i <= j]
            results[j] = sum([aux(j-elem) for elem in allowed_elems])
        return results[j]
    return aux(n)


if __name__ == '__main__':

    def main():
        import timeit
        n = 30
        values = tuple([1, 2, 3])

        print(timeit.repeat(lambda: count_solutions_recursive(n, values), repeat=3, number=1))
        print(timeit.repeat(lambda: count_solutions_dp_bottom_up(n, values), repeat=3, number=1))
        print(timeit.repeat(lambda: count_solutions_dp_top_down(n, values), repeat=3, number=1))

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
