#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MIN(x, y) ((x < y) ? x : y)

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

float distance(point p1, point p2)
{
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}

int compar_point(const void *p1, const void *p2)
{
    const point *point1 = (const point *)p1;
    const point *point2 = (const point *)p2;
    return (point1->x > point2->x) - (point1->x < point2->x);
}

int compar_PyElem(const void *p1, const void *p2)
{
    const PyElement *point1 = (const PyElement *)p1;
    const PyElement *point2 = (const PyElement *)p2;
    return (point1->p.y > point2->p.y) - (point1->p.y < point2->p.y);
}

void sort_points(point P[], size_t length, PyElement Py[])
{
    //P is sorted in place and becomes Px
    mergesort(P, length, sizeof(point), compar_point);

    //building Py
    for (size_t i = 0; i < length; i++)
    {
        PyElement py = {*(P + i), i};
        *(Py + i) = py;
    }
    mergesort(Py, length, sizeof(PyElement), compar_PyElem);
}

point *quadratic_solution(point P[], size_t length)
{
    float min_distance = INFINITY;
    float d;
    point *closest_points = (point *)malloc(sizeof(point) * 2);
    if (closest_points == NULL)
        return NULL;

    for (size_t i = 0; i < length - 1; i++)
    {
        for (size_t j = i + 1; j < length; j++)
        {
            d = distance(P[i], P[j]);
            if (d < min_distance)
            {
                min_distance = d;
                closest_points[0] = P[i];
                closest_points[1] = P[j];
            }
        }
    }
    return closest_points;
}

PyElement *get_candidates_from_different_halves(point reference, PyElement Py[], size_t length, size_t *new_length, float min_distance_upper_bound)
{
    PyElement *candidates = (PyElement *)malloc(length * sizeof(PyElement));
    if (candidates == NULL)
        return NULL;

    size_t i;
    for (i = 0; i < length; i++)
        if (abs((Py + i)->p.x - reference.x) < min_distance_upper_bound)
            *(candidates + i) = *(Py + i);

    *new_length = i;
    return candidates;
}

points_distance closest_points_from_different_halves(PyElement P[], size_t length)
{
    float min_distance = INFINITY;
    float d;
    points_distance closest_points;

    for (size_t i = 0; i < length - 1; i++)
    {
        for (size_t j = i + 1; j < MIN(length, i + 16); j++)
        {
            d = distance(P[i].p, P[j].p);
            if (d < min_distance)
            {
                min_distance = d;
                closest_points.p1 = P[i].p;
                closest_points.p2 = P[j].p;
                closest_points.distance = d;
            }
        }
    }

    return closest_points;
}

points_distance closest_points(point Px[], PyElement Py[], size_t length)
{
    if (length == 2)
    {
        points_distance result;
        result.p1 = Px[0];
        result.p2 = Px[1];
        result.distance = distance(result.p1, result.p2);
        return result;
    }

    size_t left_half_upper_bound = ceil(length / 2);
    size_t right_half_lower_bound = floor(length / 2);
    size_t left_size = left_half_upper_bound;
    size_t right_size = length - right_half_lower_bound + 1;
    PyElement *Ly = (PyElement *)malloc(left_size * sizeof(PyElement));
    PyElement *Ry = (PyElement *)malloc(right_size * sizeof(PyElement));

    for (size_t i = 0; i < length; i++)
        if ((Py + i)->xposition < left_half_upper_bound)
            *(Ly + i) = *(Py + i);

    for (size_t i = 0; i < length; i++)
        if ((Py + i)->xposition >= right_half_lower_bound)
        {
            PyElement py = {(Py + i)->p, (Py + i)->xposition - right_half_lower_bound};
            *(Ly + i) = py;
        }

    points_distance left_closest_points = closest_points(Px, Ly, left_size);
    float min_left_distance = distance(left_closest_points.p1, left_closest_points.p2);
    points_distance right_closest_points = closest_points(Px + right_half_lower_bound, Ry, right_size);
    float min_right_distance = distance(right_closest_points.p1, right_closest_points.p2);

    int min_distance_upper_bound = MIN(min_left_distance, min_right_distance);
    size_t *new_length;
    PyElement *candidates = get_candidates_from_different_halves(*(Px + left_size - 1), Py, length, new_length, min_distance_upper_bound);
    points_distance closest_candidates = closest_points_from_different_halves(candidates, *new_length);

    free(Ly);
    free(Ry);
    free(candidates);
    
    if (closest_candidates.distance < min_distance_upper_bound)    
        return closest_candidates;    
    else if (min_left_distance < min_right_distance)    
        return left_closest_points;    
    else
        return right_closest_points;    
}



int main(int argc, char const *argv[])
{
    //test data
    size_t length = 4;
    point P[] = {
        0, 0,
        3, 4,
        2, 5,
        1, 4};

    //quadratic_solution test
    point *closest_points = quadratic_solution(P, length);
    printf("(%d,%d),(%d,%d)\n", closest_points[0].x, closest_points[0].y, closest_points[1].x, closest_points[1].y);

    //sort_points test
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    for (size_t i = 0; i < length; i++)
    {
        point p = *(P + i);
        printf("Px[%zu]=(%d,%d)\n", i, p.x, p.y);
    }

    for (size_t i = 0; i < length; i++)
    {
        PyElement p = *(Py + i);
        printf("Py[%zu]=(%d,%d)\n", i, p.p.x, p.p.y);
    }

    return 0;

    //closest points test
}
