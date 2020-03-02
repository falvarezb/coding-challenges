def extended_euclid_gcd(a, b):
    """
    Extended Euclidean algorithm to express the gcd of a and b as linear combination of a and b
    for a ≥ b, if d = gcd(a, b) then there are integers x and y such that: ax + by = d (Bezout's identity)

    By the Euclidean algorithm, d = gcd(b, a mod b), so if we know how to express d as linear combination of
    b and (a mod b), d = bp + (a mod b)q, then d as linear combination of a and b is:
    d = aq + b(p - floor(a/b)q)
    """
    
    if b == 0:
        d, x, y = a, 1, 0
    else:
        (d, p, q) = extended_euclid_gcd(b, a % b)
        x = q
        y = p - q * (a // b)

    return (d, x, y)


def squares(n, m):
    d = euclid_gcd(max(n, m), min(n, m))
    return n//d * m//d


def euclid_lcm(a, b):
    """
    least common multiple calculated with Euclid's algorithm:

    lcm(a,b) * gcd(a,b) = a*b
    """
    assert a > 0 and b > 0
    a, b = max(a, b), min(a, b)

    return a*b//euclid_gcd(a, b)


def euclid_gcd(a, b):
    """
    Euclidean algorithm to calculate the greatest common divisor of 2 numbers a and b
    https://exploringnumbertheory.wordpress.com/2013/07/28/the-euclidean-algorithm/
    https://en.wikipedia.org/wiki/Euclidean_algorithm

    The following two formulations are equivalent:
    - for a ≥ b, gcd(a, b) = gcd(b, a mod b) (where a mod b represents the remainder of the division a/b)
    - for a ≥ b, d|a and d|b iff d|a-b (where d|a means d divides a)
    """
    return a if b == 0 else euclid_gcd(b, a % b)


def diophantine(a, b, c):
    """
    Returns (x, y) such that a * x + b * y = c
    
    THEOREM
    Given integers a, b, c (at least one of a and b ̸= 0), the Diophantine equation ax+by = c
    has a solution (where x and y are integers) if and only if gcd(a, b) | c
    
    The proof of this theorem also provides a method to construct the solutions x and y:
    
    x = c/gcd(a,b) * x'
    y = c/gcd(a,b) * y'
    
    where x' and y' are Bezout's coefficients given by the extended Euclid's algorithm:
    
    ax'+by' = gcd(a,b)
    """

    d, x, y = extended_euclid_gcd(max(a, b), min(a, b))
    if c % d == 0:
        if a > b:
            return (c//d*x, c//d*y)
        return (c//d*y, c//d*x)
    return None


def divide(a, b, n):
    assert n > 1 and a > 0 and euclid_gcd(a, n) == 1

    # return the number x s.t. x = b / a (mod n) and 0 <= x <= n-1.
    s, t = diophantine(a, n, 1)
    return s*b % n


def ChineseRemainderTheorem(n1, r1, n2, r2):
    d, x, y = extended_euclid_gcd(max(n1, n2), min(n1, n2))
    if n1 > n2:
        return (r2*n1*x + r1*n2*y) % (n1*n2)
    return (r2*n1*y + r1*n2*x) % (n1*n2)


'''
computes b^2k mod m
'''


def FastModularExponentiation(b, k, m):
    # your code here
    result = b % m
    for _ in range(k):
        result = (result * result) % m
    return result


'''
generalisation of previous function when e != 2^k
'''


def FastModularExponentiation2(b, e, m):
    binary_e = binary(e)

    result = 1
    position = 0
    for position, digit in enumerate(binary_e):
        if digit == 1:
            result = result * FastModularExponentiation(b, position, m) % m
    return result


'''
Leading digit is in the rightmost position
'''


def binary(n):
    result = []
    while n > 0:
        result.append(n % 2)
        n = n//2
    return result


print(binary(10))
print(FastModularExponentiation(7, 2, 11))
print(FastModularExponentiation(7, 7, 11))
print(FastModularExponentiation2(7, 13, 11))
# print(lcm(2, 3))
# print(diophantine(10, 6, 14))
# print(diophantine(6, 10, 14))
# print(divide(5, 2, 6))
# print(ChineseRemainderTheorem(5, 2, 7, 3))
# print(ChineseRemainderTheorem(686579304, 295310485, 26855093, 8217207))
# print(extended_gcd(10, 6))
