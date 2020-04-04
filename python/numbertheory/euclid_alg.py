from util import binary_expansion


def extended_euclid_gcd(a, b):
    """
    Extended Euclidean algorithm to express the gcd of a and b as linear combination of a and b
    if d = gcd(a, b) then there are integers x and y such that: ax + by = d (Bezout's identity)

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
    - gcd(a, b) = gcd(b, a mod b) (where a mod b represents the remainder of the division a/b)
    - d|a and d|b iff d|a-b (where d|a means d divides a)
    """
    return euclid_gcd(b, a % b) if b else a


def diophantine(a, b, c):
    """
    Returns (x, y) such that a * x + b * y = c

    THEOREM
    Given integers a, b, c (at least one of a and b != 0), the Diophantine equation ax+by = c
    has a solution (where x and y are integers) if and only if gcd(a, b) | c

    The proof of this theorem also provides a method to construct the solutions x and y:

    x = c/gcd(a,b) * x'
    y = c/gcd(a,b) * y'

    where x' and y' are Bezout's coefficients given by the extended Euclid's algorithm:

    ax'+by' = gcd(a,b)

    Furthermore, if (x0, y0) is a solution, then the other solutions have the form (x0 + k * b/gcd(a,b), y0 − k * a/gcd(a,b))
    where k is an arbitrary integer
    """

    d, x, y = extended_euclid_gcd(max(a, b), min(a, b))
    if c % d == 0:
        if a > b:
            return (c//d*x, c//d*y)
        return (c//d*y, c//d*x)
    return None


def sum_as_multiple_3_and_5(n):
    '''
    Any integer can be written as sum of multiples of 3 and 5.

    Proof
    =====

    We know that given integer n, the linear diophantine equation

    3 * x + 5 * y = n

    has solution iff gcd(3,5) divides n.

    And since gcd(3,5) = 1 then gcd(3,5) divides n

    Furthermore, if (x0, y0) is a solution, then the other solutions have the form (x0 + 5k, y0 − 3k)
    where k is an arbitrary integer.

    This property can be exploited to return solutions in a specific range.
    Concretely, this function returns x0 and y0 such that:

    * 0 <= |x0| < 5
    * n//5-3 <= y0 <= n//5 (// denotes the floor division)


    Note: another way to prove that any integer can be written as sum of multiples of 3 and 5 is
    based on the fact that 3Z + 5Z = Z, where 3Z and 5Z are principal ideals and Z is the set of
    the integer numbers
    '''
    x0, y0 = diophantine(3, 5, n)

    # push x0 to the range [0, 5) and update y0 accordingly
    k, x0 = divmod(x0, 5)

    return (x0, y0 + 3*k)


def modular_division(a, b, m):
    """
    Given a != 0 and b, if exists x such that a * x ≡ b (mod m), then
    x plays the role of modular division x = b/a (mod m)

    Example:

    2/5 ≡ 4 (mod 6) as 4*5≡2 (mod 6)

    Modular division is not always possible. In the following example, there is no x such that:

    3*x ≡ 1 (mod 6)

    Given that congruence is preserved under multiplication, it's easy to prove that b/a ≡ b*a' (mod m), where a' is
    the multiplicative inverse modulo m of a

    Also, it's possible to prove that a' exists iff gcd(a, m) = 1 and its value is given by the solution s of
    the Diophantine equation in the variables s and t:

    as + mt = 1

    So finally, b/a ≡ b*s (mod m)
    """
    assert a != 0

    solution = diophantine(a, m, 1)
    if solution is not None:
        return solution[0]*b % m
    return None


def chinese_remainder_theorem_2(n1, r1, n2, r2):
    '''
    We want to solve the following 2-equation system, where n1 and n2 are coprime
    x = r1 (mod n1)
    x = r2 (mod n2)

    Solution:
    x = (r2*m1*n1 + r1*m2*n2) mod (n1*n2), where m1 and m2 are Bezout coefficients of the Bezout's identity: m1*n1+m2*n2 = 1
    '''

    d, x, y = extended_euclid_gcd(max(n1, n2), min(n1, n2))

    print(d)
    if d > 1:
        raise ValueError(f"{n1} and {n2} must be coprime")

    if n1 > n2:
        return (n1*n2, (r2*n1*x + r1*n2*y) % (n1*n2))
    return (n1*n2, (r2*n1*y + r1*n2*x) % (n1*n2))


def chinese_remainder_theorem_n(n, r):
    '''
    This is the generalisation to n equations of "chinese_remainder_theorem_2"

    Given arrays
    - n = [n1, n2, ... nj], where all ni (i=1...j) are pairwise coprime
    - r = [r1, r2, ... rj]

    we want to solve the system of equations
    x = r (mod n)

    x = r1 (mod n1)
    x = r2 (mod n2)
    ....
    x = rj (mod nj)

    Solution:
    Apply chinese remainder theorem for 2 equations iteratively
    '''

    equation1 = (n[0], r[0])
    idx = 0
    while idx < len(n) - 1:
        equation2 = (n[idx+1], r[idx+1])
        equation1 = chinese_remainder_theorem_2(equation1[0], equation1[1], equation2[0], equation2[1])
        idx += 1
    return equation1


def modular_exponentiation(b, e, m):
    """
    Returns b^e (mod m)
    The process takes e steps
    """
    b = b % m
    result = 1
    for _ in range(e):
        result = (result * b) % m
    return result


def fast_modular_exponentiation_by_squaring(b, k, m):
    """
    Returns b^e (mod m) where the exponent e is a power of 2: e=2^k
    The process takes k steps by doing exponentiation by squaring

    Note: b^(2^k) = (((b^2)^2)^2)^ ..(k times)..
    """
    result = b % m
    for _ in range(k):
        result = result * result % m
    return result


def fast_modular_exponentiation_by_squaring_gen(b, e, m):
    """
    Generalisation of exponentiation by squaring when the exponent e is not a power of 2

    b^e = b^(a1*2^0 + a2*2^1 + ... aN*2*N) = b^(a1*2^0) * .... * b^(aN*2^N) where a1, a2 ... aN take the values 0 or 1

    Steps:
    1. Rewrite e in binary form
    2. Compute each of the factors b^(2^k) mod m for each element of the binary representation of the exponent
    3. Multiply the results of previous step

    Note: b^(2^k) = (((b^2)^2)^2)^ ..(k times)..
    """
    binary_e = binary_expansion(e)

    factor = b % m
    result = factor if binary_e[0] else 1
    for digit in binary_e[1:]:
        factor = factor * factor % m
        if digit == 1:
            result = result * factor % m
    return result


def timing_fast_exp():
    import timeit

    b = 2
    e = 2**100
    m = 5
    number = 1000
    # print(timeit.timeit(lambda: b**e % m, number=1000))
    # print(timeit.timeit(lambda: modular_exponentiation(b, e, m), number=number))
    print(timeit.timeit(lambda: fast_modular_exponentiation_by_squaring(b, 100, m), number=number))
    print(timeit.timeit(lambda: fast_modular_exponentiation_by_squaring_gen(b, e, m), number=number))
    print(timeit.timeit(lambda: pow(b, e, m), number=number))


if __name__ == "__main__":
    timing_fast_exp()
