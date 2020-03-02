from math import sqrt, log
from random import sample, randint


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


def convert_to_int(message_str):
    """
    Converts any string into an int
    """
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res


def convert_to_str(n):
    """
    Inverse operation to convert_to_int:

    convert_to_str(convert_to_int(msg)) == msg

    """
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]


def is_prime(n):
    if n % 2 == 0:
        return False

    for j in range(3, int(sqrt(n))+2, 2):
        if n % j == 0:
            return False
    return True


def num_primes_approx(n):
    return int(n//log(n))


def num_primes_exact(n):
    count = 0
    for j in range(2, n):
        if is_prime(j):
            count += 1
    return count


def generate_prime(seed):
    num_samples = int(log(seed)//2)
    candidates = sample(range(3, seed, 2), k=num_samples)
    for j in candidates:
        if is_prime(j):
            return j
    print("no prime was found")
    return None


def fermat_primality_test(n):
    '''
    Probabilistic test to determine whether a number is a probable prime

    It's based on Fermat's little theorem:

    if prime p does not divide integer a, then a^(p-1) = 1 mod p

    For the test, we try all values 2 .... p-1 < p. 
    If the congruence holds for all possible values, then we consider n as prime.


    Note: clearly, this approach can give place to false positives as we can't try all infinite values of a that are not
    a multiple of p. What's more, there are composite numbers p (called Carmichael numbers) for which all possible values 
    of a that are not multiple of p satisfy the congruence
    '''

    assert(n > 1)
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    a_candidates = range(3, n)
    for j in a_candidates:
        if FastModularExponentiation2(j, n-1, n) != 1:
            return False
    return True


def even_as_power_of_2(n):
    '''
    Given even number 'n', returns 's' and 'd' such that n = 2^s*d and d is odd
    '''

    s = 0
    while n % 2 == 0:
        s += 1
        n //= 2
    return s, n


def miller_rabin_primality_test(n, repetitions):
    '''
    Probabilistic test to determine whether a number is a probable prime

    It's based on Fermat's little theorem and the fact that there are no nontrivial square roots of 1 modulo p 
    (see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)


    As a consequence of the above, one of the following congruences hold for any prime number n and for any
    integer a such that n does not divide a:

    a^d = 1 mod n
    a^(d*2^r) = -1 mod n, 0 =< r < s

    Note: 
     * -1 mod n = n-1 mod n
     * s and d correspond to the expression of n-1 as 2^s*d (any even number can be written as the product of a power of 2
     and an odd number)

    Therefore, the test to determine if n is prime will consist of proving that one of the above congruences is true for a random
    a selected in the range 1 < a < n.

    In case the selected a is a strong liar, the test should be repeated a few times with different values of a
    to gain confidence in the result.
    '''

    def is_prime(n, s, d):
        a = randint(2, n-1)**d % n
        if a == 1 or a == n-1:  # Python % operator is based on floor division, thus we need to compare to n-1 instead to -1
            return True
        for _ in range(s):
            a = a**2 % n
            if a == n-1:  # Python % operator is based on floor division, thus we need to compare to n-1 instead to -1
                return True
        return False

    assert(n > 1)
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    s, d = even_as_power_of_2(n-1)
    for _ in range(repetitions):
        if not is_prime(n, s, d):
            return False
    return True


if __name__ == '__main__':
    print('hello')
    n = 1000000

    results = dict()
    for j in range(3, 10000, 2):
        fermat = fermat_primality_test(j)
        miller = miller_rabin_primality_test(j, 5)
        exact = is_prime(j)
        if fermat != miller:
            results[j] = (exact, fermat, miller)

    print(results)

    # print(num_primes_approx(n))
    # print(num_primes_exact(n))
    # print(num_primes_approx(n)/num_primes_exact(n))
    # print(1/log(n))
    # print(generate_prime(1000))
    # potential_prime = 919
    # print(is_prime(potential_prime))
    # print(fermat_primality_test(potential_prime))
