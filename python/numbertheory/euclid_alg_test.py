from euclid_alg import euclid_gcd, euclid_lcm, extended_euclid_gcd, diophantine


def test_euclid_gcd():
    assert euclid_gcd(20, 15) == 5


def test_euclid_gcd_coprimes():
    assert euclid_gcd(20, 11) == 1


def test_euclid_gcd_order_does_not_matter():
    assert euclid_gcd(15, 20) == euclid_gcd(20, 15)


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
    assert diophantine(8, 4, 7) == None
