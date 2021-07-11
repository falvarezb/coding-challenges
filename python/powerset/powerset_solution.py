def powerset(n: int)->list:
    if n == 0:
        return [[]]
    subsets = powerset(n-1)
    return subsets + [elem+[n] for elem in subsets]