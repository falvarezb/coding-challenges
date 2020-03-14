from math import log10, ceil
from random import getrandbits

def even_as_power_of_2(n):
    """
    Returns the representation as a power of 2 of an even number n.

    Any even number n can be expressed as:
    n = 2^s*d and d is odd (this is easy to prove just by repeatedly dividing n by 2)

    This function returns (s,d)

    Example:
    n=12 returns (2,3)
    """
    assert n % 2 == 0, "the argument must be an even number"

    s = 0
    while n % 2 == 0:
        s += 1
        n //= 2
    return s, n


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


def binary_expansion(n):
    """
    Returns binary representation of n
    MSB (most significant bit) is in the rightmost position
    """
    result = []
    while n > 0:
        result.append(n % 2)
        n = n//2
    return result


def num_digits(n):
    '''
    Returns number of digits of integer n
    '''
    return ceil(log10(n))


def num_digits_exp(n, e):
    '''
    Returns number of digits of integer n^e
    '''
    return ceil(e*log10(n))

def num_digits_of_n_bit_long_integer(n):
    return num_digits_exp(2, n)


def random_n_bit_long_odd_integer(n):
    '''
    Returns a random n-bit long odd integer
    '''
    # apply a mask to set MSB and LSB to 1
    mask = (1 << n - 1) | 1 # 100...001
    return getrandbits(n) | mask


