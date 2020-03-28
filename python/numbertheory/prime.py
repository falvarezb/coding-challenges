from math import sqrt, log, ceil
from random import sample, randint
from euclid_alg import fast_modular_exponentiation_by_squaring_gen
from util import even_as_power_of_2, random_n_bit_long_odd_integer


def is_prime(p):
    assert p > 1, "the argument must be a positive integer greater than 1 as 0 and 1 are neither prime nor composite"
    if p == 2:
        return True
    if p % 2 == 0:
        return False

    for j in range(3, int(sqrt(p))+2, 2):
        if p % j == 0:
            return False
    return True


def next_prime(n):
    """
    Returns first prime greater than n

    Example:
    n=4 returns 5
    """
    if n%2 == 0:
        n += 1
    else:
        n += 2
    while not is_prime(n):
        n += 2
    return n


def prime_factorisation(n):
    """
    Returns an array representing the factorisation of n as product of prime numbers. The primes are sorted in ascending order.

    By the fundamental theorem of arithmetic, the prime factorisation of any positive integer exists and is unique up to reordering

    Example:
    n = 12 returns [2,2,3]
    """
    primes = [2]
    factorisation = []
    while n > 1:
        candidate_divisor = primes[-1]
        if n % candidate_divisor == 0:
            factorisation.append(candidate_divisor)
            n //= candidate_divisor
        else:
            primes.append(next_prime(candidate_divisor))
    return factorisation


def num_primes_approx(n):
    """
    According to the prime number theorem, the prime-counting function (that counts the number of prime numbers less than or 
    equal to some real number n) can be approximated by n/ln(n)

    https://en.wikipedia.org/wiki/Prime_number_theorem
    """
    return int(n//log(n))


def prime_counting_function(n):
    """
    Returns the number of prime numbers less than or equal to the real number n

    Example:
    n=10 returns 4
    """
    count = 0
    for j in range(2, n):
        if is_prime(j):
            count += 1
    return count


def random_probable_prime_less_than(seed):
    """
    Returns a random prime number less than or equal to seed
    Returns None if prime number fails to be found

    By the prime number theorem, we know that there are seed/ln(seed) prime numbers in the interval [1, seed].

    If we only consider the odd numbers in the interval [1, seed], the probability that a randomly picked number is prime is given by:
    prob = (seed/ln(seed))/(seed/2) = 2/ln(seed)

    where seed/2 is the number of odd numbers in the interval [1, seed]

    Note: although we know that 1 is not a prime, we include it to simplify the reasoning and the above probability formula

    https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    """
    prob = 2/log(seed)
    num_samples = ceil(1/prob)
    print(f"probability to find prime number <= {seed} when sampling a single value: {prob}")
    print(f"num samples required to 'ensure' that a primer number is found: {num_samples}")
    candidates = sample(range(3, seed, 2), k=num_samples)
    for j in candidates:
        if is_prime(j):
            return j
    return None


def fermat_primality_test(p):
    '''
    Probabilistic test to determine whether a number is a probable prime

    It's based on Fermat's little theorem:

    if p is prime and a is an integer not divisible by p, then a^(p-1) = 1 mod p

    For the test, we try all values 2 .... p-1 < p.
    If the congruence holds for all possible values, then we consider n as prime.


    Note: clearly, this approach can give place to false positives as we can't try all infinite values of a that are not
    a multiple of p. What's more, there are composite numbers p (called Carmichael numbers) for which all possible values 
    of a that are not multiple of p satisfy the congruence
    '''

    assert p > 1, "the argument must be a positive integer greater than 1 as 0 and 1 are neither prime nor composite"
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    a_candidates = range(3, p)
    for j in a_candidates:
        if fast_modular_exponentiation_by_squaring_gen(j, p-1, p) != 1:
            return False
    return True


def miller_rabin_primality_test(p, repetitions):
    '''
    Probabilistic test to determine whether a number p is a probable prime

    It's based on Fermat's little theorem and the fact that there are no nontrivial square roots of 1 modulo p
    (see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)


    As a consequence of the above, one of the following congruences hold for any prime number p and for any
    integer a such that p does not divide a:

    a^d = 1 mod p
    a^(d*2^r) = -1 mod p, 0 =< r < s

    Note:
     * -1 mod p = p-1 mod p
     * s and d correspond to the expression of p-1 as 2^s*d (any even number can be written as the product of a power of 2
     and an odd number)

    Therefore, the test to determine if p is prime will consist of proving that one of the above congruences is true for a random
    a selected in the range 1 < a < p.

    In case the selected a is a strong liar, the test should be repeated a few times with different values of a
    to gain confidence in the result.
    '''

    def is_potential_prime(p, s, d):
        a = fast_modular_exponentiation_by_squaring_gen(randint(2, p-1), d, p)
        if a in (1, p-1):  # Python % operator is based on floor division, thus we need to compare to n-1 instead of -1
            return True
        for _ in range(s):
            a = fast_modular_exponentiation_by_squaring_gen(a, 2, p)
            if a == p-1:  # Python % operator is based on floor division, thus we need to compare to n-1 instead to -1
                return True
        return False

    assert p > 1, "the argument must be a positive integer greater than 1 as 0 and 1 are neither prime nor composite"
    if p == 2:
        return True
    if p % 2 == 0:
        return False

    s, d = even_as_power_of_2(p-1)
    for _ in range(repetitions):
        if not is_potential_prime(p, s, d):
            return False
    return True


def random_n_bit_long_prime(n):
    '''
    Returns a random n-bit long prime number
    '''
    assert n > 1, "the argument must be a positive integer greater than 1 as 0 and 1 are neither prime nor composite"

    num_repetitions_for_primality_test = 5
    p = random_n_bit_long_odd_integer(n)
    while not miller_rabin_primality_test(p, num_repetitions_for_primality_test):
        p = random_n_bit_long_odd_integer(n)
    return p


def primality_test_comparison(n):
    """
    Compares the accuracy of the probabilistic methods to find all primes less than n

    Outputs those cases that are not correctly classified
    """
    results = dict()
    for j in range(3, n, 2):
        fermat = fermat_primality_test(j)
        miller = miller_rabin_primality_test(j, 5)
        exact = is_prime(j)
        if fermat != exact or miller != exact:
            results[j] = (exact, fermat, miller)

    print(results)


if __name__ == '__main__':
    # print(random_probable_prime_less_than(10000))
    # primality_test_comparison(10000)
    print(random_n_bit_long_prime(1024))
    # print(miller_rabin_primality_test(123000001,1))
