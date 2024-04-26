from itertools import permutations
from math import factorial
from random import randint
from functools import lru_cache
from probability.probability import freq_prob


"""
Secretary's problem

probability P(n,r) of finding the best candidate out of 'n' for some value 'r' of rejected candidates
"""


def best_candidate_probability(n, r):
    """    
    n --> number of candidates
    r --> number of candidates initially rejected to create the baseline

    theoretical solution as per:
    https://www.cantorsparadise.com/math-based-decision-making-the-secretary-problem-a30e301d8489
    """
    assert n>0 and r>0
    prob = 0
    for i in range(r+1, n+1):
        prob += (1/(i-1))
    prob *= (r/n)
    return prob


def best_candidate_probability_sim(n, r):
    """
    n --> number of candidates
    r --> number of candidates initially rejected to create the baseline

    solution calculated by simulating the poblem by inspecting each of the possible permutations of candidates
    O(n!)
    """
    assert n>0 and r>0
    # candidates:  1 .... n
    candidates = list(range(1, n+1))
    # the number used to enumerate each candidate also represents the candidate's rank, therefore the best candidate is 'n'
    best_candidate = n
    # each permutation represents the order in which candidates are processed
    ps = permutations(candidates, len(candidates))

    num_solutions = 0
    for p in ps:
        best_baseline_candidate = max(p[:r])
        selected_candidate = 0
        for candidate in p[r:]:
            if candidate > best_baseline_candidate:
                # best-yet candidate after the initial rejection phase
                selected_candidate = candidate
                break
        num_solutions += (selected_candidate == best_candidate)

    return num_solutions/factorial(n)


def best_candidate_probability_sim_optimised(n, r):
    """
    optimi
    sation of 'best_candidate_probability_sim' to run on O(n^2)
    """
    @lru_cache
    def memoized_fact(n):
        return factorial(n)

    def comb(n, k):
        # must use integer division to avoid floating-point overflow errors
        # it's ok to use integer division as binomial coefficients are always integer numbers
        return memoized_fact(n)//memoized_fact(n-k)//memoized_fact(k)

    assert n>1 and 0<r<n
    num_solutions = 0
    for j in range(n-2-r+1):
        num_solutions += (comb(n-2, j+r)*r*memoized_fact(r+j-1)*memoized_fact(n-r-j-1))
    num_solutions += memoized_fact(r)*comb(n-2, r-1)*memoized_fact(n-r)
    return num_solutions/factorial(n)

@lru_cache
def optimalr(n, P):
    """
    Calculate the maximum of the probability function P(n,r) on the variable 'r' for a fixed 'n'

    Returns
    -------
    tuple (rmax/n, P(rmax))   
    """
    values = [P(n, r) for r in range(1, n-1)]
    mx = max(values)
    return ((values.index(mx)+1)/n, mx)


########################
# variant simulation

def rejection_sim(n, r):
    """
    simulating a 50% chance of the candidate rejecting the offer
    """
    # candidates:  1 .... n
    candidates = list(range(1, n+1))
    # the number used to enumerate each candidate also represents the candidate's rank
    best_candidate = n
    # each permutation represents the order in which candidates are processed
    # due to the possibility of rejection, all permutations (except the ones containing 'n' in the first 'r' positions) are potential solutions
    ps = [p for p in permutations(candidates, len(candidates)) if max(p[:r]) != n]
    # ps = permutations(candidates, len(candidates))
    # ps = [p for p in permutations(candidates, len(candidates)) if max(p[:r])!=n] if r else list(ps)

    def experiment(num_trials):
        num_solutions = 0
        for _ in range(num_trials):
            for p in ps:
                best_baseline_candidate = max(p[:r])
                selected_candidate = 0
                for candidate in p[r:]:
                    if candidate > best_baseline_candidate and randint(0, 1):
                        selected_candidate = candidate
                        break
                num_solutions += (selected_candidate == best_candidate)

        return num_solutions/factorial(n)/num_trials

    return freq_prob(0.001, 100, 50, experiment)[0]


def recall_sim(n, r):
    """

    """
    # candidates:  1 .... n
    candidates = list(range(1, n+1))
    # the number used to enumerate each candidate also represents the candidate's rank
    best_candidate = n
    # each permutation represents the order in which candidates are processed
    # due to the possibility of rejection, all permutations (except the ones containing 'n' in the first 'r' positions) are potential solutions
    ps = [p for p in permutations(candidates, len(candidates)) if max(p[:r]) != n]

    def experiment(num_trials):
        num_solutions = 0
        for _ in range(num_trials):
            for p in ps:
                best_baseline_candidate = max(p[:r])
                selected_candidate = 0
                for candidate in p[r:]:
                    if not selected_candidate and candidate > best_baseline_candidate:
                        selected_candidate = candidate
                    elif selected_candidate and candidate > selected_candidate and randint(0, 1):
                        selected_candidate = candidate
                        break
                num_solutions += (selected_candidate == best_candidate)

        return num_solutions/factorial(n)/num_trials

    return freq_prob(0.001, 100, 50, experiment)[0]


if __name__ == '__main__':
    n = 3
    r = 1
    print(best_candidate_probability_sim_optimised(n, r))
    # print(best_candidate_probability_sim(n, r))
    # print(best_candidate_probability_sim_optimised(n, r))

    # print(optimalr(n, best_candidate_probability))
    # print(optimalr(n, best_candidate_probability_sim))
    # print(optimalr(n, best_candidate_probability_sim_optimised))
    # print([recall_sim(n,r) for r in range(1,n-1)])
    # print(rejection_sim(5,2))
