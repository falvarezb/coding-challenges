#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include "closest_point.h"

#define MIN(x, y) ((x < y) ? x : y)

/**
 * Euclidean distance
 */
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

points_distance quadratic_solution(point P[], size_t length)
{
    assert(length >= 2);
    float min_distance = INFINITY;
    float d;
    points_distance closest_points;

    for (size_t i = 0; i < length - 1; i++)
    {
        for (size_t j = i + 1; j < length; j++)
        {
            d = distance(P[i], P[j]);
            if (d < min_distance)
            {
                min_distance = d;
                closest_points.p1 = P[i];
                closest_points.p2 = P[j];
                closest_points.distance = d;
            }
        }
    }
    return closest_points;
}

/**
 * Special cases:
 * -> returns 0 elements when there are repeat points
 * -> returns 1 element when the only candidate is the point used as reference
 * 
 */ 
PyElement *get_candidates_from_different_halves(point reference, PyElement Py[], size_t length, size_t *candidates_length, float min_distance_upper_bound)
{
    PyElement *candidates = (PyElement *)malloc(length * sizeof(PyElement));
    if (candidates == NULL)
        return NULL;

    size_t j = 0;
    for (size_t i = 0; i < length; i++)
        if (abs((Py + i)->p.x - reference.x) < min_distance_upper_bound)
            *(candidates + j++) = *(Py + i);

    *candidates_length = j;
    return candidates;
}

points_distance closest_points_from_different_halves(PyElement P[], size_t length)
{
    points_distance closest_points;

    // CAUTION: guard to avoid size_t overflow
    // --> length = 0 when there are repeat points
    // --> length = 1 when the only candidate is the point
    //      used as reference to determine the candidates
    if (length < 2)
    {
        closest_points.distance = INFINITY;
        return closest_points;
    }
    
    
    float min_distance = INFINITY;
    float d;

    // CAUTION: size_t is unsigned => if length=0, length-1 is positive
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

void populateLy(PyElement* Py, size_t Pylength, PyElement* Ly, size_t left_half_upper_bound)
{    
    size_t j = 0;
    for (size_t i = 0; i < Pylength; i++)
        if ((Py + i)->xposition < left_half_upper_bound)
            *(Ly + j++) = *(Py + i);
}

void populateRy(PyElement* Py, size_t Pylength, PyElement* Ry, size_t right_half_lower_bound)
{
    size_t j = 0;
    for (size_t i = 0; i < Pylength; i++)
        if ((Py + i)->xposition >= right_half_lower_bound)
        {
            PyElement py = {(Py + i)->p, (Py + i)->xposition - right_half_lower_bound};
            *(Ry + j++) = py;
        }
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

    size_t left_half_upper_bound = ceil(length / 2.);
    size_t right_half_lower_bound = floor(length / 2.);
    size_t left_size = left_half_upper_bound;
    size_t right_size = length - right_half_lower_bound;
    PyElement *Ly = (PyElement *)malloc(left_size * sizeof(PyElement));
    PyElement *Ry = (PyElement *)malloc(right_size * sizeof(PyElement));

    populateLy(Py, length, Ly, left_half_upper_bound);
    populateRy(Py, length, Ry, right_half_lower_bound);

    //closest points in the left half
    points_distance left_closest_points = closest_points(Px, Ly, left_size);
    float min_left_distance = distance(left_closest_points.p1, left_closest_points.p2);
    
    //closest points in the right half
    points_distance right_closest_points = closest_points(Px + right_half_lower_bound, Ry, right_size);
    float min_right_distance = distance(right_closest_points.p1, right_closest_points.p2);

    float min_distance_upper_bound = MIN(min_left_distance, min_right_distance);
    size_t *candidates_length = (size_t *)malloc(sizeof(size_t));
    PyElement *candidates = get_candidates_from_different_halves(*(Px + left_size - 1), Py, length, candidates_length, min_distance_upper_bound);
    points_distance closest_candidates = closest_points_from_different_halves(candidates, *candidates_length);

    free(candidates_length);
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

points_distance nlogn_solution(point P[], size_t length)
{
    assert(length >= 2);
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    return closest_points(P, Py, length);
}

// int main(int argc, char const *argv[])
// {
// {
//     size_t length = 6;
//     point P[] = {
//         0, 0,
//         3, 4,
//         2, 5,
//         1, 4,
//         2, 2,
//         3, 3};

//     //quadratic_solution test
//     points_distance closest_points = quadratic_solution(P, length);
//     printf("(%d,%d),(%d,%d)\n", closest_points.p1.x, closest_points.p1.y, closest_points.p2.x, closest_points.p2.y);
// }

// {
//     //sort_points test
//     size_t length = 4;
//     point P[] = {
//         0, 0,
//         3, 4,
//         2, 5,
//         1, 4};
//     PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
//     sort_points(P, length, Py);
//     for (size_t i = 0; i < length; i++)
//     {
//         point p = *(P + i);
//         printf("Px[%zu]=(%d,%d)\n", i, p.x, p.y);
//     }

//     for (size_t i = 0; i < length; i++)
//     {
//         PyElement p = *(Py + i);
//         printf("Py[%zu]=(%d,%d)\n", i, p.p.x, p.p.y);
//     }
// }

// {
//     //nlogn_solution test
//     size_t length = 5;
//     point P[] = {
//         1, 2,
//         10, 4,
//         6, 3,
//         1, 8,
//         6,3};

//     points_distance closest_points = nlogn_solution(P, length);
//     printf("(%d,%d),(%d,%d)\n", closest_points.p1.x, closest_points.p1.y, closest_points.p2.x, closest_points.p2.y);
// }

// {
//     //nlogn_solution vs quadratic_solution
//     srand (time(NULL));
//     size_t length = 5;
//     point P1[length];
//     point P2[length];
//     for (size_t i = 0; i < length; i++)
//     {
//         int x = rand() % 10+1;
//         int y = rand() % 10+1;
//         point p = {x,y};
//         P1[i] = p;
//         P2[i] = p;
//         printf("(%d,%d)", p.x,p.y);
//     }

//     points_distance closest_points1 = nlogn_solution(P1, length);
//     points_distance closest_points2 = quadratic_solution(P2, length);
//     printf("\n(%d,%d),(%d,%d)\n", closest_points1.p1.x, closest_points1.p1.y, closest_points1.p2.x, closest_points1.p2.y);
//     printf("\n(%d,%d),(%d,%d)\n", closest_points2.p1.x, closest_points2.p1.y, closest_points2.p2.x, closest_points2.p2.y);
//     assert(closest_points1.distance == closest_points2.distance);
// }
//}
