from closest_points.closest_points_solution import *


def test_quadratic_solution():
    points = [(0, 0), (1, 1), (2, 1), (2, 4)]
    assert quadratic_solution(points) == 1

def test_nlogn_solution():
    points = [(0, 0), (1, 1), (2, 1), (2, 4)]
    assert nlogn_solution(points) == 1


def test_sort_points():
    points = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(points)
    assert Px == [PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1), PEntry((2, 5), 2, 3), PEntry((3, 4), 3, 2)]
    assert Py == [PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1), PEntry((3, 4), 3, 2), PEntry((2, 5), 2, 3)]


def test_left_half():
    p1, p2, p3, p4 = PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1), PEntry((2, 5), 2, 3), PEntry((3, 4), 3, 2)
    Px = [p1, p2, p3, p4]
    Py = [p1, p2, p4, p3]
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1)]
    assert newPy == [PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1)]


def test_right_half():
    p1, p2, p3, p4 = PEntry((0, 0), 0, 0), PEntry((1, 4), 1, 1), PEntry((2, 5), 2, 3), PEntry((3, 4), 3, 2)
    Px = [p1, p2, p3, p4]
    Py = [p1, p2, p4, p3]
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [PEntry((2, 5), 0, 1), PEntry((3, 4), 1, 0)]
    assert newPy == [PEntry((3, 4), 1, 0), PEntry((2, 5), 0, 1)]
