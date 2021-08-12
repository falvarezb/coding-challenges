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

#endif