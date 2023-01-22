from math import factorial
from  scipy.special import comb

"""

Pascal's triangle facts:

1. The binomial coefficient (n k) corresponds to the entry in the nth row and kth column of Pascal's triangle
2. Sum of the elements of row n of Pascal's triangle equals 2^n (first row is n=0)
3. The number of elements of row n of Pascal's triangle equals n+1 (first row is n=0)


Relationship between Pascal's triangle and Galton board (aka Bean machine):

1. the number of elements in a bin of Galton board equals the corresponding entry in Pascal's triangle
2. combining the previous statement and #2 of Pascal's triangle facts, the probability of an elements reaching a bin
of Galton board is Pnk = (n k) / 2^n

Using the recursive nature of Pascal's triangle, the latest #2 can also be expressed as:

Pnk = (Pn-1k-1 + Pn-1k)/2

"""

def pascal_triangle(n):
    """
    Generation of Pascal's triangle up to the row 'n'
    """
    if n == 1:
        return [[1]]

    triangle = pascal_triangle(n-1)
    previous_row = triangle[n-2]
    new_row = [1]*n
    for i in range(1, n-1):
        new_row[i] = previous_row[i-1]+previous_row[i]
    triangle.append(new_row)
    return triangle


def binomial_coefficient_def(n, k):
    """
    Implementation based on the definition of binomial coefficient: (n k) = n! / (n-k)! / k!
    """
    return factorial(n) // (factorial(n-k) * factorial(k))


def binomial_coefficient_recursive(n, k):

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


def binomial_coefficient_row(n, k):
    """
    Implementation based on the algorithm to calculate a row by itself:

    (n k) = (n k-1) * (n+1-k)/k

    """

    # taking advantage of binomial coefficients symmetry: (n k) = (n n-k)
    if k > n//2:
        k = n - k

    c = dict()
    c[n, 0] = 1

    for i in range(1, k+1):
        c[n, i] = c[n, i-1] * (n+1-i)//i

    return c[n, k]




def sum_elements_row(n):
    """
    Sum of the elements of row n of Pascal's triangle equals 2^n (first row is n=0)
    """
    
    return 2**n


def galton_board_concentration(n, bins):
    """

    Example
    -------

    Fraction of beans that end near the center (bins 40-60 among 0-100) for the ideal Galton board with 100 layers
    """

    if max(bins) >= n:
        raise Exception("illegal argument: given n layers, the bins must be enumerated from 0 to n-1")

    count = 0
    for k in bins:
        count += binomial_coefficient_def(n, k)

    total = sum_elements_row(n)

    return count/total


if __name__ == "__main__":

    def main():
        import timeit

        n = 120
        k = 70
        print(timeit.timeit(lambda: binomial_coefficient_def(n, k), number=1))
        print(timeit.timeit(lambda: binomial_coefficient_recursive(n, k), number=1))
        print(timeit.timeit(lambda: comb(n, k), number=1))
        print(timeit.timeit(lambda: binomial_coefficient_row(n, k), number=1))

    main()

