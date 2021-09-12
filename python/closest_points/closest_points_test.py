from closest_points.closest_points_solution import *
import hypothesis.strategies as st
from hypothesis import given, example, note
from random import sample
import pytest

@pytest.fixture
def split_even_number_points_fixture():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3)]
    return (p1, p2, p3, p4), Px, Py

@pytest.fixture
def split_odd_number_points_fixture():
    p1, p2, p3, p4, p5 = (0, 0), (1, 4), (2, 5), (3, 4), (4, 0)
    Px = [p1, p2, p3, p4, p5]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3), PyElement(p5, 4)]
    return (p1, p2, p3, p4, p5), Px, Py


def test_quadratic_solution():
    P=[(0, 1), (0, 3), (2, 0), (0, 0)]
    assert quadratic_solution(P) == ((0,1),(0,0))

def test_nlogn_left_half_solution():
    P=[(3,9),(1,5),(0,1),(5,3),(8,6),(20,20),(40,40)]
    assert nlogn_solution(P) == ((0,1),(1,5))

def test_nlogn_right_half_solution():
    P=[(3,9),(1,5),(0,1),(5,3),(8,6),(20,20),(20,21)]
    assert nlogn_solution(P) == ((20,20),(20,21))

def test_nlogn_inter_half_solution():
    P=[(2,-100),(0,0),(9,100),(10,0),(11,100),(20,-100),(20,0)]
    assert nlogn_solution(P) == ((9,100),(11,100))

def test_nlogn_repeat_points():
    P=[(3,9),(1,5),(10,5),(3,9)]
    assert nlogn_solution(P) == ((3,9),(3,9))


def test_nlogn_solution_par():
    P=[(0, 1), (0, 3), (2, 0), (0, 0)]
    assert nlogn_solution_par(P,1) == ((0,0),(0,1))


def test_sort_points():
    P = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(P)
    assert Px == [(0, 0), (1, 4), (2, 5), (3, 4)]
    assert Py == [PyElement((0, 0), 0), PyElement((1, 4), 1), PyElement((3, 4), 3), PyElement((2, 5), 2)]


def test_left_half_even(split_even_number_points_fixture):
    (p1, p2, p3, p4), Px, Py = split_even_number_points_fixture
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1,p2]
    assert newPy == [PyElement(p1, 0), PyElement(p2, 1)]

def test_right_half_even(split_even_number_points_fixture):
    (p1, p2, p3, p4), Px, Py = split_even_number_points_fixture
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3,p4]
    assert newPy == [PyElement(p3, 0), PyElement(p4, 1)]

def test_left_half_odd(split_odd_number_points_fixture):
    (p1, p2, p3, p4, p5), Px, Py = split_odd_number_points_fixture
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1,p2,p3]
    assert newPy == [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2)]

def test_right_half_odd(split_odd_number_points_fixture):
    (p1, p2, p3, p4, p5), Px, Py = split_odd_number_points_fixture
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3,p4,p5]
    assert newPy == [PyElement(p3, 0), PyElement(p4, 1), PyElement(p5, 2)]


@given(st.lists(st.tuples(st.integers(0,100), st.integers(0,100)), min_size=2, max_size=100, unique=True))
def test_quadratic_vs_nlogn(P):
    assert distance(*quadratic_solution(P)) == distance(*nlogn_solution(P))

@given(st.lists(st.tuples(st.integers(0,100), st.integers(0,100)), min_size=2, max_size=100, unique=True))
def test_nlogn_vs_nlogn_par(P):
    assert distance(*nlogn_solution_par(P,2)) == distance(*nlogn_solution(P))