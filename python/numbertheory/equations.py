
from collections import Counter

def equation() -> dict:
    """
    Find integer solutions in the range (0, 100) of
    a^3 + b^3 = c^3 + d^3

    Example
    ===========

    For any value that a and b take in the given range, for instance, a=1, b=5, there are at least 4 possible solutions:

    1^3 + 5^3 = 1^3 + 5^3
    1^3 + 5^3 = 5^3 + 1^3
    5^3 + 1^3 = 1^3 + 5^3
    5^3 + 1^3 = 5^3 + 1^3

    These solutions are just permutations of the values (1, 5) and can be counted as just 1 solution.

    With this approach in mind, the problem can be reduced to find all the possible solutions for each of the equations:

    x^3 + y^3 = z, where z equals z = [a^3 + b^3 for a in 0..100 for b in 0..100] 

    """
    solutions = dict()
    lowerbound, upperbound = 0, 1000
    for x in range(lowerbound, upperbound+1):
        for y in range(x, upperbound+1):
            z = x**3 + y**3
            if z in solutions:
                existing_value = solutions.pop(z)
                existing_value.append((x, y))
                solutions.update({z: existing_value})
            else:
                solutions.update({z: [(x, y)]})
    return solutions


def analyse_solutions(solutions: dict) -> dict:
    num_solutions = dict()
    for k,v in solutions.items():
        num_solutions.update({len(v): num_solutions.get(len(v), 0) + 1})
    return Counter(num_solutions)  


def n_solutions(n: int, solutions: dict) -> dict:
    return {k: v for (k,v) in solutions.items() if len(v) == n}


if __name__ == "__main__":
    solutions = equation()
    print(len(solutions))
    print(n_solutions(3, solutions))

