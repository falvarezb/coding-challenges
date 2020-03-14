from util import binary_expansion

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


def modular_division(a, b, m):
    """
    Given a != 0 and b, there exists x (not always) such that a * x ≡ b (mod m), therefore
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


def ChineseRemainderTheorem(n1, r1, n2, r2):
    d, x, y = extended_euclid_gcd(max(n1, n2), min(n1, n2))
    if n1 > n2:
        return (r2*n1*x + r1*n2*y) % (n1*n2)
    return (r2*n1*y + r1*n2*x) % (n1*n2)


def modular_exponentiation(b, e, m):
    """
    Returns b^e (mod m)
    The process takes e steps
    """
    result = 1
    for _ in range(e):
        result = (result * b) % m
    return result


def fast_modular_exponentiation_by_squaring(b, k, m):
    """
    Returns b^e (mod m) where the exponent e is a power of 2: e=2^k
    The process takes k steps by doing exponentiation by squaring
    """
    result = b % m
    for _ in range(k):
        result = (result * result) % m
    return result


def fast_modular_exponentiation_by_squaring_gen(b, e, m):
    """
    Generalisation of exponentiation by squaring when the exponent e is not a power of 2

    Steps:
    1. Rewrite e in binary form
    2. Compute b^(2^k) mod m for each element of the binary representation of the exponent
    3. Multiply the results of previous step
    """
    binary_e = binary_expansion(e)

    result = 1
    position = 0
    for position, digit in enumerate(binary_e):
        if digit == 1:
            result = result * fast_modular_exponentiation_by_squaring(b, position, m) % m
    return result



