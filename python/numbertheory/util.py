from math import log10, ceil, log
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
    for c in message_str:
        res = res * 256 + ord(c)
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
    MSB (most significant bit) is in the leftmost position
    """
    b = 2
    digits = []
    while n > 0:
        n, r = divmod(n, b)
        digits.append(str(r))
    return "".join(digits[::-1])

def negabinary_expansion(n):
    """
    Returns negabinary (base -2) representation of n
    MSB (most significant bit) is in the leftmost position
    """
    b = -2
    digits = []
    while n != 0:
        n, r = divmod(n, b)
        if r < 0:
            r -= b
            n += 1
        digits.append(str(r))
    return "".join(digits[::-1])


def two_complement(n, length=None):
    """
    Returns two's complement of n with regards to 2^(length): 2^(length) - n
    If length is not specified, by default is the number of bits of n
    """
    if not length:
        length = len(bin(n)[2:])
    mask = 2**length - 1  # = 111..(num_bits)..111
    return (~n & mask) + 1  # (~n & mask) = ones' complement


def radix_complement(x: int, b: int) -> int:
    """
    Returns radix complement of integer x in base b: b^n - x
    (where n is the number of digits of x in base b)
    """

    n = num_digits(x, b)
    return b**n - x


def num_digits(n: int, b: int = 10) -> int:
    '''
    Returns number of digits of integer n in base b
    '''

    return ceil(log(n, b))

    # q = n // b
    # if q > 0:
    #     return 1 + num_digits(q, b)

    # return 1


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
    # MSB must be 1 to ensure it is a n-bit long integer
    # LSB must be 1 to ensure it is odd
    mask = (1 << n - 1) | 1  # 100..(n)..001
    return getrandbits(n) | mask
