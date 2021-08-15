#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include "closest_point.h"

//par-version headers
#include <sys/wait.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

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

/**
 * P -> Px, Py
 */
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

void populateLy(PyElement *Py, size_t Pylength, PyElement *Ly, size_t left_half_upper_bound)
{
    size_t j = 0;
    for (size_t i = 0; i < Pylength; i++)
        if ((Py + i)->xposition < left_half_upper_bound)
            *(Ly + j++) = *(Py + i);
}

void populateRy(PyElement *Py, size_t Pylength, PyElement *Ry, size_t right_half_lower_bound)
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
    float min_left_distance = left_closest_points.distance;

    //closest points in the right half
    points_distance right_closest_points = closest_points(Px + right_half_lower_bound, Ry, right_size);
    float min_right_distance = right_closest_points.distance;

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

void closest_points_par(point Px[], PyElement Py[], size_t length, points_distance *result, int par_threshold)
{
    if (length == 2)
    {
        result->p1 = Px[0];
        result->p2 = Px[1];
        result->distance = distance(result->p1, result->p2);
        return;
    }
    else if (length > par_threshold)
    {
        size_t left_half_upper_bound = ceil(length / 2.);
        size_t right_half_lower_bound = floor(length / 2.);
        size_t left_size = left_half_upper_bound;
        size_t right_size = length - right_half_lower_bound;
        PyElement *Ly = (PyElement *)malloc(left_size * sizeof(PyElement));
        PyElement *Ry = (PyElement *)malloc(right_size * sizeof(PyElement));

        populateLy(Py, length, Ly, left_half_upper_bound);
        populateRy(Py, length, Ry, right_half_lower_bound);

        points_distance *left_result = mmap(NULL, sizeof(points_distance), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
        if (left_result == MAP_FAILED)
            exit(EXIT_FAILURE);
        points_distance *right_result = (points_distance *)malloc(sizeof(points_distance));

        switch (fork())
        {
        case -1: //error
            exit(EXIT_FAILURE);
        case 0: //child
            //closest points in the left half
            closest_points_par(Px, Ly, left_size, left_result, par_threshold);
            break;
        default: //parent
            //closest points in the right half
            closest_points_par(Px + right_half_lower_bound, Ry, right_size, right_result, par_threshold);
            if (wait(NULL) == -1)
                exit(EXIT_FAILURE);

            float min_left_distance = left_result->distance;
            float min_right_distance = right_result->distance;

            float min_distance_upper_bound = MIN(min_left_distance, min_right_distance);
            size_t *candidates_length = (size_t *)malloc(sizeof(size_t));
            PyElement *candidates = get_candidates_from_different_halves(*(Px + left_size - 1), Py, length, candidates_length, min_distance_upper_bound);
            points_distance closest_candidates = closest_points_from_different_halves(candidates, *candidates_length);

            free(candidates_length);
            free(Ly);
            free(Ry);
            free(candidates);

            if (closest_candidates.distance < min_distance_upper_bound)
            {
                result->p1 = closest_candidates.p1;
                result->p2 = closest_candidates.p2;
                result->distance = closest_candidates.distance;
            }
            else if (min_left_distance < min_right_distance)
            {
                result->p1 = left_result->p1;
                result->p2 = left_result->p2;
                result->distance = left_result->distance;
            }
            else
            {
                result->p1 = right_result->p1;
                result->p2 = right_result->p2;
                result->distance = right_result->distance;
            }
            free(right_result);
            if (munmap(left_result, sizeof(points_distance)) == -1)
                exit(EXIT_FAILURE);
        }
    }
    else 
    {
        points_distance intermediate_result = closest_points(Px, Py, length);
        result->p1 = intermediate_result.p1;
        result->p2 = intermediate_result.p2;
        result->distance = intermediate_result.distance;
    }
}

points_distance nlogn_solution_par(point P[], size_t length)
{
    assert(length >= 2);
    points_distance *result = (points_distance *)malloc(sizeof(points_distance));
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    closest_points_par(P, Py, length, result, 100);
    return *result;
}

// int main(int argc, char const *argv[])
//{
//}
