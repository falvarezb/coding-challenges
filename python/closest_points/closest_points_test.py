from closest_points.closest_points_solution import *


def test_quadratic_solution():
    points = [(0, 0), (1, 1), (2, 1), (2, 4), (9,9)]
    assert quadratic_solution(points) == ((1,1),(2,1))

def test_nlogn_solution():
    points = [(0, 0), (1, 1), (2, 1), (2, 4), (9,9)]
    assert nlogn_solution(points) == ((1,1),(2,1))


def test_sort_points():
    points = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(points)
    assert Px == [(0, 0), (1, 4), (2, 5), (3, 4)]
    assert Py == [PEntry((0, 0), 0), PEntry((1, 4), 1), PEntry((3, 4), 3), PEntry((2, 5), 2)]


def test_left_half_even():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PEntry(p1, 0), PEntry(p2, 1), PEntry(p3, 2), PEntry(p4, 3)]
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1,p2]
    assert newPy == [PEntry(p1, 0), PEntry(p2, 1)]


def test_right_half_even():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PEntry(p1, 0), PEntry(p2, 1), PEntry(p3, 2), PEntry(p4, 3)]
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3,p4]
    assert newPy == [PEntry(p3, 0), PEntry(p4, 1)]
