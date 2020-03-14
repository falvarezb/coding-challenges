import pytest
from prime import is_prime, prime_factorisation, prime_counting_function, next_prime, fermat_primality_test, miller_rabin_primality_test, random_n_bit_long_prime
from util import binary_expansion


def test_is_prime_1():
    with pytest.raises(AssertionError, match="the argument must be a positive integer greater than 1"):
        is_prime(1)


def test_is_prime_2():
    assert is_prime(2)


def test_is_prime_19():
    assert is_prime(19)

def test_is_prime_1009():
    assert is_prime(1009)


def test_is_prime_20():
    assert not is_prime(20)


def test_prime_factorisation_2():
    assert prime_factorisation(2) == [2]


def test_prime_factorisation_12():
    assert prime_factorisation(12) == [2, 2, 3]


def test_prime_factorisation_20():
    assert prime_factorisation(20) == [2, 2, 5]


def test_prime_counting_function_10():
    assert prime_counting_function(10) == 4


def test_prime_counting_function_100():
    assert prime_counting_function(100) == 25

def test_next_prime_4():
    assert next_prime(4) == 5

def test_fermat_primality_test_19():
    assert fermat_primality_test(19)

def test_fermat_primality_test_20():
    assert not fermat_primality_test(20)


def test_miller_rabin_primality_test_11():
    assert miller_rabin_primality_test(11, 1)

def test_miller_rabin_primality_test_60():
    assert not miller_rabin_primality_test(60, 1)

def test_random_n_bit_long_prime():
    n = 3
    p = random_n_bit_long_prime(n)
    assert is_prime(p)
    assert len(binary_expansion(p)) == n
