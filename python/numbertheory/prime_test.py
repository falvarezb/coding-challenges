import pytest
from prime import is_prime, prime_factorisation, prime_counting_function, next_prime


def test_is_1_prime():
    with pytest.raises(AssertionError, match="the argument must be a positive integer greater than 1"):
        is_prime(1)


def test_is_2_prime():
    assert is_prime(2)


def test_is_19_prime():
    assert is_prime(19)


def test_is_20_prime():
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
