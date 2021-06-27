import pytest
from util import *


def test_convert_to_int_h():
    assert convert_to_int('h') == 104

def test_convert_to_int_hi():
    assert convert_to_int('hi') == 26729

def test_convert_to_str():
    msg = 'whatever'
    assert convert_to_str(convert_to_int(msg)) == msg

def test_even_as_power_of_2_12():
    # 12 = 2^2*3
    s, d = even_as_power_of_2(12)
    assert (s, d) == (2, 3)
    assert d % 2 == 1

def test_even_as_power_of_2_13():
    with pytest.raises(AssertionError, match="the argument must be an even number"):
        even_as_power_of_2(13)


def test_binary_expansion():
    assert binary_expansion(10) == [1, 0, 1, 0]


def test_num_digits_132():
    assert num_digits(132) == 3

def test_num_digits_exp_32():
    assert num_digits_exp(2, 5) == 2

def test_num_digits_of_n_bit_long_integer_3():
    assert num_digits_of_n_bit_long_integer(3) == 1

def test_num_digits_of_n_bit_long_integer_2048():
    assert num_digits_of_n_bit_long_integer(2048) == 617

def test_random_n_bit_long_odd_integer():
    n = 2
    num = random_n_bit_long_odd_integer(n)
    assert num % 2 == 1
    assert len(binary_expansion(num)) == n

def test_two_complement():
    assert two_complement(5,4) == 11
    assert two_complement(5) == 3
    assert two_complement(two_complement(5,4), 4) == 5
    assert two_complement(0b0101, 4) == 0b1011
    assert two_complement(0b101, 6) == 0b111011

def test_radix_complement():
    assert radix_complement(5, 2) == 3
    assert radix_complement(5, 3) == 4
    assert radix_complement(5, 4) == 11
    assert radix_complement(5, 10) == 5
