from rsa import even_as_power_of_2, miller_rabin_primality_test


def test_even_as_power_of_2():
    # 12 = 2^2*3
    s, d = even_as_power_of_2(12)
    assert (s, d) == (2, 3)
    assert d % 2 == 1


def test_miller_rabin_primality_test_positive():
    assert miller_rabin_primality_test(11, 1)

def test_miller_rabin_primality_test_negative():
    assert not miller_rabin_primality_test(60, 1)
