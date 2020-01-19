from math import factorial
from  scipy.special import comb


# def factorial(n):
#     f = 1
#     for j in range(2, n+1):
#         f *= j
#     return f


def binomial_coefficient(n, k):
    """
    Implementation based on the definition of binomial coefficient: (n k) = n! / (n-k)! / k!
    """
    return int(factorial(n) / factorial(n-k) / factorial(k))


def binomial_coefficient2(n, k):

    """
    Implementation based on the recursive formula: (n k) = (n-1 k-1) + (n-1 k)
    """

    c = dict()

    if k == 0 or k == n:
        return 1

    for i in range(n):
        c[i, 0] = 1
        c[i, i] = 1

        for j in range(1, i):
            c[i, j] = c[i-1, j-1] + c[i-1, j]

    return c[n-1, k-1] + c[n-1, k]


if __name__ == "__main__":

    def main():
        import timeit

        n = 1000
        k = 1000
        print(timeit.timeit(lambda: binomial_coefficient(n, k), number=1))
        print(timeit.timeit(lambda: binomial_coefficient2(n, k), number=1))
        print(timeit.timeit(lambda: comb(n, k), number=1))
        a = binomial_coefficient(n, k)
        b = binomial_coefficient2(n, k)
        c = comb(n, k, exact=True)
        print(a)
        print(b)
        print(c)
        assert b == c
        assert a == c

    main()
