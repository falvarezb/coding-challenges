from math import sqrt, log, ceil
from random import sample


def is_prime(n):
    """
    0 and 1 are neither prime nor composite
    """
    assert n > 1, "the argument must be a positive integer greater than 1"
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for j in range(3, int(sqrt(n))+2, 2):
        if n % j == 0:
            return False
    return True


def next_prime(n):
    """
    Returns first prime greater than n

    Example:
    n=4 returns 5
    """
    n += 1
    while not is_prime(n):
        n += 1
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
    equal to some real number N) can be approximated by N/ln(N)

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


def generate_prime(seed):
    """
    Returns a random prime number less than or equal to seed with probability 2/ln(seed)
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


if __name__ == '__main__':
    print(generate_prime(10000))
