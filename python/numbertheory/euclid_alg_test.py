import hypothesis.strategies as st
from hypothesis import given

from euclid_alg import (chinese_remainder_theorem_2,
                        chinese_remainder_theorem_n, diophantine, euclid_gcd,
                        euclid_lcm, extended_euclid_gcd,
                        fast_modular_exponentiation_by_squaring,
                        fast_modular_exponentiation_by_squaring_gen,
                        modular_division, modular_exponentiation,
                        sum_as_multiple_3_and_5)


def test_euclid_gcd():
    assert euclid_gcd(20, 15) == 5


def test_euclid_gcd_coprimes():
    assert euclid_gcd(20, 11) == 1


def test_euclid_gcd_order_does_not_matter():
    assert euclid_gcd(15, 20) == euclid_gcd(20, 15)


def test_euclid_lcm_0():
    assert euclid_lcm(0, 10) == 0

def test_euclid_lcm():
    assert euclid_lcm(20, 15) == 60


def test_euclid_lcm_coprimes():
    assert euclid_lcm(5, 7) == 5*7


def test_extended_euclid_gcd():
    assert extended_euclid_gcd(10, 6) == (2, -1, 2)


def test_extended_euclid_gcd_order_does_matter():
    gcd1 = extended_euclid_gcd(10, 6)
    gcd2 = extended_euclid_gcd(6, 10)
    assert gcd1[0] == gcd2[0]
    assert gcd1[1] == gcd2[2]
    assert gcd1[2] == gcd2[1]


def test_extended_euclid_gcd_equal():
    assert extended_euclid_gcd(6, 6) == (6, 0, 1)


def test_diophantine_equation():
    # 10x+6y=14
    assert diophantine(10, 6, 14) == (-7, 14)


def test_diophantine_equation_order_does_matter():
    # 10x1+6y1=14, 6x2+10y2=14
    solution1 = diophantine(10, 6, 14)
    solution2 = diophantine(6, 10, 14)
    assert solution1[0] == solution2[1]
    assert solution1[1] == solution2[0]


def test_diophantine_equation_with_no_solution():
    # 8x+4y=7
    assert diophantine(8, 4, 7) is None


def test_modular_division():
    # 2/5 ≡ 4 mod 6
    assert modular_division(5, 2, 6) == 4


def test_modular_division2():
    # 6/4 ≡ 5 (mod 7)
    assert modular_division(4, 6, 7) == 5


def test_modular_division_not_possible():
    # 4/8 mod 6 is not possible
    assert modular_division(8, 4, 6) is None


def test_modular_exponentiation_exp_power_of_2():
    # 7^4 (mod 11) = 3
    assert modular_exponentiation(7, 4, 11) == 3
    assert fast_modular_exponentiation_by_squaring(7, 2, 11) == 3
    assert fast_modular_exponentiation_by_squaring_gen(7, 4, 11) == 3


def test_modular_exponentiation_exp_not_power_of_2():
    # 7^13 (mod 11) = 2
    assert modular_exponentiation(7, 13, 11) == 2
    assert fast_modular_exponentiation_by_squaring_gen(7, 13, 11) == 2


def test_chinese_remainder_theorem():
    '''
    x = 2 (mod 3)
    x = 3 (mod 5)
    '''
    assert chinese_remainder_theorem_2(3, 2, 5, 3) == (15, 8)


def test_chinese_remainder_theorem_n():
    '''
    x = 0 (mod 3)
    x = 3 (mod 4)
    x = 4 (mod 5)
    '''
    assert chinese_remainder_theorem_n([3, 4, 5], [0, 3, 4]) == (60, 39)


def test_sum_as_multiple_3_and_5_12():
    a, b = sum_as_multiple_3_and_5(12)
    assert (a, b) == (4, 0)


def test_sum_as_multiple_3_and_5_23():
    a, b = sum_as_multiple_3_and_5(23)
    assert (a, b) == (1, 4)


def test_sum_as_multiple_3_and_5_7():
    a, b = sum_as_multiple_3_and_5(7)
    assert (a, b) == (4, -1)


def test_sum_as_multiple_3_and_5_3():
    a, b = sum_as_multiple_3_and_5(3)
    assert (a, b) == (1, 0)


@given(st.integers(-100000, 100000))
def test_sum_as_multiple_3_and_5(n):
    a, b = sum_as_multiple_3_and_5(n)
    assert a*3 + b*5 == n
    assert abs(a) < 5
    assert n//5-3 <= b <= n//5
