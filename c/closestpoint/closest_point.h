#ifndef FAB_CLOSEST_POINT
#define FAB_CLOSEST_POINT

#include <stdlib.h>

typedef struct
{
    int x;
    int y;
} point;

typedef struct
{
    point p;
    int xposition;
} PyElement;

typedef struct
{
    point p1;
    point p2;
    float distance;
} points_distance;

PyElement *get_candidates_from_different_halves(point reference, PyElement Py[], size_t length, size_t *candidates_length, float min_distance_upper_bound);
points_distance nlogn_solution(point P[], size_t length);
points_distance quadratic_solution(point P[], size_t length);
void sort_points(point P[], size_t length, PyElement Py[]);
points_distance nlogn_solution_par(point P[], size_t length, int num_processes);

#endif