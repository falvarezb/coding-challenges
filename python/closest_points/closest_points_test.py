from closest_points.closest_points_solution import *
import hypothesis.strategies as st
from hypothesis import given, example, note
from random import sample


def test_quadratic_solution():
    points=[(0, 1), (0, 3), (2, 0), (0, 0)]
    assert quadratic_solution(points) == ((1,1),(2,1))

def test_nlogn_solution():
    points=[(0, 1), (0, 3), (2, 0), (0, 0)]
    assert nlogn_solution(points) == ((1,1),(2,1))


def test_sort_points():
    points = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(points)
    assert Px == [(0, 0), (1, 4), (2, 5), (3, 4)]
    assert Py == [PyElement((0, 0), 0), PyElement((1, 4), 1), PyElement((3, 4), 3), PyElement((2, 5), 2)]


def test_left_half_even():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3)]
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1,p2]
    assert newPy == [PyElement(p1, 0), PyElement(p2, 1)]


def test_right_half_even():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3)]
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3,p4]
    assert newPy == [PyElement(p3, 0), PyElement(p4, 1)]


@given(st.lists(st.tuples(st.integers(0,100), st.integers(0,100)), min_size=2, max_size=100, unique=True))
def test_solution_comparison(points):
    assert distance(*quadratic_solution(points)) == distance(*nlogn_solution(points))