# Algorithm Design by Jon Kleinberg, Eva Tardos

"""
Given n points in the plane, find the pair that is closest together.
"""

import math


def distance(p1: tuple, p2: tuple) -> float:
    """
    each tuple represents a point (x,y) in the plane
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def quadratic_solution(points):
    """
    brute force algorithm, O(n^2)

    points: list of tuples, each tuple representing a point (x,y) in the plane
    """
    min_distance = math.inf
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            d = distance(points[i], points[j])
            if d < min_distance:
                min_distance = d
                min_pair = (points[i], points[j])
    return min_pair


class PyElement:
    """
    Object representing elemlents of Py (list of points sorted by coordinate y):
    - point: point (x,y) in the plane
    - x_position: position of (x,y) in the list of points Px sorted by coordinate x    
    """

    def __init__(self, point, x_position):
        self.point = point
        self.x_position = x_position

    def __repr__(self) -> str:
        return f"[{self.point}, {self.x_position}]"

    def __eq__(self, o: object) -> bool:
        return self.point == o.point and self.x_position == o.x_position


def sort_points(points):
    """
    points: list of tuples, each tuple representing a point (x,y) in the plane

    returns the tuple (Px, Py) where:
    Px = list of points ordered by coordinate x
    Py = list of points ordered by coordinate y
    """
    Px = sorted(points, key=lambda p: p[0])
    Px_aux = [PyElement(p, i) for i, p in enumerate(Px)]
    Py = sorted(Px_aux, key=lambda pentry: pentry.point[1])
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


def get_candidates(left_half, Py, min_left_distance, min_right_distance):
    """
    candidates to be the closest points lie within 'min_distance_upper_bound' of
    the middle point separating the left and right halves  
    """

    rightmost_left_point = left_half[-1]
    min_distance_upper_bound = min(min_left_distance, min_right_distance)
    candidates = []
    for p in Py:
        if abs(p.point[0]-rightmost_left_point[0]) < min_distance_upper_bound:
            candidates.append(p)
    return min_distance_upper_bound, candidates

def nlogn_solution(points):
    """
    divide and conquer algorithm, O(n log n)

    points: list of tuples, each tuple representing a point (x,y) in the plane
    """

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
        l1, l2 = closest_points(Lx, Ly)
        min_left_distance = distance(l1, l2)
        # closest points in the right half
        r1, r2 = closest_points(Rx, Ry)
        min_right_distance = distance(r1, r2)

        # min_distance = min(min_left_distance, min_right_distance)
        # rightmost_left_point = Lx[-1]
        # candidates = []
        # for p in Py:
        #     if abs(p.point[0]-rightmost_left_point[0]) < min_distance:
        #         candidates.append(p)
        min_distance_upper_bound, candidates = get_candidates(Lx, Py, min_left_distance, min_right_distance)
        min_distance = min_distance_upper_bound

        for i in range(len(candidates)-1):
            for j in range(i+1, min(len(candidates), i+16)):
                d = distance(candidates[i].point, candidates[j].point)
                if d < min_distance:
                    min_distance = d
                    min_pair = (candidates[i].point, candidates[j].point)

        if min_distance < min_distance_upper_bound:
            return min_pair
        elif min_left_distance < min_right_distance:
            return (l1, l2)
        else:
            return (r1, r2)

    return closest_points(*sort_points(points))


if __name__ == "__main__":
    points = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(points)
    print(Px)
    print(Py)
