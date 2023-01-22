from pascal_triangle import galton_board_concentration, binomial_coefficient_def, binomial_coefficient_recursive, binomial_coefficient_row,pascal_triangle
from hypothesis import given
import hypothesis.strategies as st
from  scipy.special import comb


def test_galton_board_concentration():
    assert abs(galton_board_concentration(1000, range(400,601)) - 1) < 0.001


def test_pascal_triangle():
    assert pascal_triangle(4) == [[1],[1,1],[1,2,1],[1,3,3,1]]


# ==== PROPERTY-BASED TESTING ======

def binomial_coefficient_strategy(numerator):
    """
    Generator of binomial coefficients:
    (numerator 0), (numerator 1),  ... (numerator numerator-1), (numerator, numerator)
    """
    for j in range(numerator+1):
        yield (numerator, j)


def binomial_coefficient_strategy2(numerator):
    return [(numerator, j) for j in range(numerator+1)]


@given(st.builds(binomial_coefficient_strategy, st.integers(1, 30)))
def test_methods_to_calculate_binomial_coefficients(l):
    for (n, k) in l:
        assert binomial_coefficient_def(n, k) == binomial_coefficient_recursive(n, k)
        assert binomial_coefficient_def(n, k) == comb(n, k, exact=True)
        assert binomial_coefficient_def(n, k) == binomial_coefficient_row(n, k)     
