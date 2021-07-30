# Algorithm Design by Jon Kleinberg, Eva Tardos

"""
Given n points in the plane, find the pair that is closest together.
"""

import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def quadratic_solution(points):
    """
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


class PEntry:
    """
    point: point (x,y) in the plane
    x_position: position of (x,y) in the list of points sorted by coordinate x
    y_position: position of (x,y) in the list of points sorted by coordinate y
    """

    def __init__(self, point, x_position):
        self.point = point
        self.x_position = x_position        

    def __repr__(self) -> str:
        return f"[{self.point}, {self.x_position}]"

    def __eq__(self, o: object) -> bool:
        return self.point == o.point and self.x_position == o.x_position


def sort_points(points):
    Px = sorted(points, key=lambda p: p[0])
    Px_aux = [PEntry(p, i) for i, p in enumerate(Px)]
    Py = sorted(Px_aux, key=lambda pentry: pentry.point[1])
    return Px, Py


def left_half_points(Px, Py):
    n = len(Px)
    left_half_upper_bound = math.ceil(n/2)

    Qx, Qy = Px[:left_half_upper_bound], []    
    for pentry in Py:
        if pentry.x_position < left_half_upper_bound:                        
            Qy.append(pentry)            
    return Qx, Qy


def right_half_points(Px, Py):
    n = len(Px)
    right_half_lower_bound = math.floor(n/2)

    Rx, Ry = Px[right_half_lower_bound:], []    
    for pentry in Py:
        if pentry.x_position >= right_half_lower_bound:            
            Ry.append(PEntry(pentry.point, pentry.x_position-right_half_lower_bound))            
    return Rx, Ry


def nlogn_solution(points):
    """
    divide and conquer algorithm
    """

    def closest_points(Px, Py):
        """
        Px: list of points sorted by coordinate x
        Py: list of points sorted by coordinate y
        """
        if len(Px) == 2:
            return Px[0], Px[1]

        Qx, Qy = left_half_points(Px, Py)
        Rx, Ry = right_half_points(Px, Py)

        q1, q2 = closest_points(Qx, Qy)
        r1, r2 = closest_points(Rx, Ry)

        delta = min(distance(q1,q2), distance(r1,r2))
        rightmost_Qx = Qx[-1]
        s = []
        for p in Py:
            if distance(p.point,rightmost_Qx) < delta:
                s.append(p)
        
        min_distance = delta        
        for i in range(len(Py)-1):
            for j in range(i+1, min(len(Py),i+16)):
                d = distance(Py[i].point, Py[j].point)
                if d < min_distance:
                    min_distance = d
                    min_pair = (Py[i].point, Py[j].point)

        if min_distance < delta:
            return min_pair
        elif distance(q1,q2) < distance(r1,r2):
            return (q1,q2)
        else:
            return (r1,r2)                


    return closest_points(*sort_points(points))


if __name__ == "__main__":
    points = [(0, 0), (3, 4), (2, 5), (1, 4)]
    Px, Py = sort_points(points)
    print(Px)
    print(Py)
