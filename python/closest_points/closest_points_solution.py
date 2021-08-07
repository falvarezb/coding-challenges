# Algorithm Design by Jon Kleinberg, Eva Tardos

"""
Given n points in the plane, find the pair that is closest together.
"""

import math
from multiprocessing import Process, Value

sol1_x, sol1_y, sol2_x, sol2_y = Value('d', math.inf), Value('d', math.inf), Value('d', math.inf), Value('d', math.inf)
lsol1_x, lsol1_y, lsol2_x, lsol2_y = Value('d', math.inf), Value('d', math.inf), Value('d', math.inf), Value('d', math.inf)
rsol1_x, rsol1_y, rsol2_x, rsol2_y = Value('d', math.inf), Value('d', math.inf), Value('d', math.inf), Value('d', math.inf)


def distance(p1: tuple, p2: tuple) -> float:
    """
    each tuple represents a point (x,y) in the plane
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def quadratic_solution(P):
    """
    brute force algorithm, O(n^2)

    points: list of tuples, each tuple representing a point (x,y) in the plane
    """
    min_distance = math.inf
    for i in range(len(P)-1):
        for j in range(i+1, len(P)):
            d = distance(P[i], P[j])
            if d < min_distance:
                min_distance = d
                min_pair = (P[i], P[j])
    return min_pair


class PyElement:
    """
    Given a list of points P:
    - Px is the list of points sorted by coordinate x
    - Py is the list of points sorted by coordinate y

    This class represents elemenets of Py:
    - point: point (x,y) in the plane
    - x_position: position of (x,y) in Px

    We use 
    - Px to split in two halves the set of elements in each recursion
    - Py to find the solution when merging the results of the two halves in each recursion
    """

    def __init__(self, point, x_position):
        self.point = point
        self.x_position = x_position

    def __repr__(self) -> str:
        return f"[{self.point}, {self.x_position}]"

    def __eq__(self, o: object) -> bool:
        return self.point == o.point and self.x_position == o.x_position


def sort_points(P):
    """
    P -> Px, Py
    """
    Px = sorted(P, key=lambda p: p[0])
    Py = sorted([PyElement(p, i) for i, p in enumerate(Px)], key=lambda py: py.point[1])
    return Px, Py


def left_half_points(Px, Py):
    """
    returns the values Px and Py corresponding to the left half of the points
    """
    n = len(Px)
    left_half_upper_bound = math.ceil(n/2)

    newPx, newPy = Px[:left_half_upper_bound], []
    for pentry in Py:
        if pentry.x_position < left_half_upper_bound:
            newPy.append(pentry)
    return newPx, newPy


def right_half_points(Px, Py):
    """
    returns the values Px and Py corresponding to the right half of the points
    """
    n = len(Px)
    right_half_lower_bound = math.floor(n/2)

    newPx, newPy = Px[right_half_lower_bound:], []
    for pentry in Py:
        if pentry.x_position >= right_half_lower_bound:
            newPy.append(PyElement(pentry.point, pentry.x_position-right_half_lower_bound))
    return newPx, newPy


def get_candidates_from_different_halves(left_half, Py, min_left_distance, min_right_distance):
    """
    Once the closest points in each half have been determined, we need to consider if the closest
    points overall belong to different halves.

    The potential candidates must lie within 'min_distance_upper_bound' of
    the middle point separating the left and right halves
    """

    rightmost_left_point = left_half[-1]
    min_distance_upper_bound = min(min_left_distance, min_right_distance)
    candidates = []
    for p in Py:
        if abs(p.point[0]-rightmost_left_point[0]) < min_distance_upper_bound:
            candidates.append(p)
    return min_distance_upper_bound, candidates


def closest_points_from_different_halves(candidates):
    """
    Obtain the closest points among the candidates belonging to different halves
    """
    min_distance = math.inf
    closest_candidates = None
    for i in range(len(candidates)-1):
        for j in range(i+1, min(len(candidates), i+16)):
            d = distance(candidates[i].point, candidates[j].point)
            if d < min_distance:
                min_distance = d
                closest_candidates = (candidates[i].point, candidates[j].point)
    return min_distance, closest_candidates


def closest_points(Px, Py):
    """
    Px: list of points sorted by coordinate x
    Py: list of points sorted by coordinate y

    Recursive function, each iteration halves the input, O(log n)
    """
    if len(Px) == 2:
        return Px[0], Px[1]

    Lx, Ly = left_half_points(Px, Py)
    Rx, Ry = right_half_points(Px, Py)

    # closest points in the left half
    left_closest_points = closest_points(Lx, Ly)
    min_left_distance = distance(*left_closest_points)
    # closest points in the right half
    right_closest_points = closest_points(Rx, Ry)
    min_right_distance = distance(*right_closest_points)

    min_distance_upper_bound, candidates = get_candidates_from_different_halves(Lx, Py, min_left_distance, min_right_distance)
    min_distance, closest_candidates = closest_points_from_different_halves(candidates)

    if min_distance < min_distance_upper_bound:
        return closest_candidates
    elif min_left_distance < min_right_distance:
        return left_closest_points
    else:
        return right_closest_points


def nlogn_solution(points):
    """
    divide and conquer algorithm, O(n log n)

    points: list of tuples, each tuple representing a point (x,y) in the plane
    """

    return closest_points(*sort_points(points))


def closest_points_par(Px, Py, s1_x, s1_y, s2_x, s2_y):
    """
    Px: list of points sorted by coordinate x
    Py: list of points sorted by coordinate y

    Recursive function, each iteration halves the input, O(log n)
    """
    if len(Px) == 2:
        s1_x.value = Px[0][0]
        s1_y.value = Px[0][1]
        s2_x.value = Px[1][0]
        s2_y.value = Px[1][1]
        return

    Lx, Ly = left_half_points(Px, Py)
    Rx, Ry = right_half_points(Px, Py)


    if len(Px) > 100000:        
        # closest points in each half
        pleft = Process(target=closest_points_par, args=(Lx, Ly, lsol1_x, lsol1_y, lsol2_x, lsol2_y))
        pright = Process(target=closest_points_par, args=(Rx, Ry, rsol1_x, rsol1_y, rsol2_x, rsol2_y))
        pleft.start()
        pright.start()
        pleft.join()
        pright.join()
        min_left_distance = distance((lsol1_x.value, lsol1_y.value), (lsol2_x.value, lsol2_y.value))
        min_right_distance = distance((rsol1_x.value, rsol1_y.value), (rsol2_x.value, rsol2_y.value))

        min_distance_upper_bound, candidates = get_candidates_from_different_halves(Lx, Py, min_left_distance, min_right_distance)
        min_distance, closest_candidates = closest_points_from_different_halves(candidates)

        if min_distance < min_distance_upper_bound:
            s1_x.value = closest_candidates[0][0]
            s1_y.value = closest_candidates[0][1]
            s2_x.value = closest_candidates[1][0]
            s2_y.value = closest_candidates[1][1]
        elif min_left_distance < min_right_distance:
            s1_x.value = lsol1_x.value
            s1_y.value = lsol1_y.value
            s2_x.value = lsol2_x.value
            s2_y.value = lsol2_y.value
        else:
            s1_x.value = rsol1_x.value
            s1_y.value = rsol1_y.value
            s2_x.value = rsol2_x.value
            s2_y.value = rsol2_y.value
    else:
        # closest points in the left half
        left_closest_points = closest_points(Lx, Ly)
        min_left_distance = distance(*left_closest_points)
        # closest points in the right half
        right_closest_points = closest_points(Rx, Ry)
        min_right_distance = distance(*right_closest_points)

        min_distance_upper_bound, candidates = get_candidates_from_different_halves(Lx, Py, min_left_distance, min_right_distance)
        min_distance, closest_candidates = closest_points_from_different_halves(candidates)

        if min_distance < min_distance_upper_bound:
            s1_x.value = closest_candidates[0][0]
            s1_y.value = closest_candidates[0][1]
            s2_x.value = closest_candidates[1][0]
            s2_y.value = closest_candidates[1][1]
        elif min_left_distance < min_right_distance:
            s1_x.value = left_closest_points[0][0]
            s1_y.value = left_closest_points[0][1]
            s2_x.value = left_closest_points[1][0]
            s2_y.value = left_closest_points[1][1]
        else:
            s1_x.value = right_closest_points[0][0]
            s1_y.value = right_closest_points[0][1]
            s2_x.value = right_closest_points[1][0]
            s2_y.value = right_closest_points[1][1]

def nlogn_solution_par(points):
    """
    divide and conquer algorithm, O(n log n)

    points: list of tuples, each tuple representing a point (x,y) in the plane
    """

    return closest_points_par(*sort_points(points), sol1_x, sol1_y, sol2_x, sol2_y)


if __name__ == "__main__":

    from random import sample
    import timeit

    def main():
        x = sample(range(1000000), 1000000)
        y = sample(range(1000000), 1000000)
        P = list(zip(x, y))
        # print(timeit.repeat(lambda: nlogn_solution(P), repeat=1, number=1))
        print(timeit.repeat(lambda: nlogn_solution_par(P), repeat=1, number=1))
        # P = [(0, 0), (3, 4), (2, 5), (1, 4)]
        # print(nlogn_solution(P))
        # print(nlogn_solution_par(P))
        # print(sol1_x.value)
        # print(sol1_y.value)
        # print(sol2_x.value)
        # print(sol2_y.value)

    main()
