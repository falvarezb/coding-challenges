from itertools import permutations
from math import factorial
from functools import lru_cache

"""
Secretary's problem

success probability P(n,r) of picking the best candidate out of 'n' for some value 'r' of rejected candidates
"""


def best_candidate_probability(n, r):
    """
    solution as per:
    https://www.cantorsparadise.com/math-based-decision-making-the-secretary-problem-a30e301d8489
    """
    prob = 0
    for i in range(r+1, n+1):
        prob += (1/(i-1))
    prob *= (r/n)
    return prob


def best_candidate_probability_sim(n, r):
    """
    solution calculated by simulating the poblem by inspecting each of the possible permutations of candidates
    O(n!)
    """
    # candidates:  1 .... n
    candidates = list(range(1, n+1))
    # the number used to enumerate each candidate also represents the candidate's rank
    best_candidate = n
    # each permutation represents the order in which candidates are processed
    ps = list(permutations(candidates, len(candidates)))

    num_solutions = 0
    for p in ps:
        best_baseline_candidate = max(p[:r])
        selected_candidate = 0
        for candidate in p[r:]:
            if candidate > best_baseline_candidate:
                selected_candidate = candidate
                break
        num_solutions += (selected_candidate == best_candidate)

    return num_solutions/factorial(n)


def best_candidate_probability_sim_optimised(n, r):
    """
    optimisation of 'best_candidate_probability_sim' to run on O(n^2)
    """
    @lru_cache
    def memoized_fact(n):
        return factorial(n)

    def comb(n, k):
        return memoized_fact(n)//memoized_fact(n-k)//memoized_fact(k)

    num_solutions = 0
    for j in range(n-2-r+1):
        num_solutions += (comb(n-2, j+r)*r*memoized_fact(r+j-1)*memoized_fact(n-r-j-1))
    num_solutions += memoized_fact(r)*comb(n-2, r-1)*memoized_fact(n-r)
    return num_solutions/factorial(n)


def optimalr(n, P):
    """
    calculation of the maximum of the probability function P(n,r) on the variable 'r' for a fixed 'n'
    returns (rmax/n, P(rmax))
    """
    values = [P(n, r) for r in range(1, n-1)]
    mx = max(values)
    return ((values.index(mx)+1)/n, mx)


if __name__ == '__main__':
    n = 20
    r = 1
    # print(best_candidate_probability(n, r))
    # print(best_candidate_probability_sim(n, r))
    # print(best_candidate_probability_sim_optimised(n, r))

    print(optimalr(n, best_candidate_probability))
    # print(optimalr(n, best_candidate_probability_sim))
    print(optimalr(n, best_candidate_probability_sim_optimised))
