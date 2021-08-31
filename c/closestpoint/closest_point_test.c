#include <stddef.h>
#include <stdarg.h>
#include <setjmp.h>
#include <cmocka.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <time.h>
#include "closest_point.h"

void assert_pyelem_equal(PyElement p1, PyElement p2)
{
    assert_int_equal(p1.p.x, p2.p.x);
    assert_int_equal(p1.p.y, p2.p.y);
    assert_int_equal(p1.xposition, p2.xposition);
}

void assert_point_equal(point p1, point p2)
{
    assert_int_equal(p1.x, p2.x);
    assert_int_equal(p1.y, p2.y);
}

void assert_points_distance_equal(points_distance p1, points_distance p2)
{
    assert_point_equal(p1.p1, p2.p1);
    assert_point_equal(p1.p2, p2.p2);
    assert_float_equal(p1.distance, p2.distance, 0.01);
}

void test_get_candidates_from_different_halves(void **state)
{
    (void)state; /* unused */

    PyElement p1 = {1, 2};
    PyElement p2 = {4, 2};
    PyElement p3 = {3, 2};
    PyElement p4 = {2, 2};
    PyElement Py[] = {p1, p2, p3, p4};
    point reference = p4.p;
    size_t length = 4;
    size_t *candidates_length = malloc(sizeof(size_t));
    float min_distance_upper_bound = 1.5;
    PyElement *result = get_candidates_from_different_halves(reference, Py, length, candidates_length, min_distance_upper_bound);

    assert_non_null(result);
    assert_int_equal(*candidates_length, 3);
    assert_pyelem_equal(*result, p1);
    assert_pyelem_equal(*(result + 1), p3);
    assert_pyelem_equal(*(result + 2), p4);
}

void test_get_candidates_from_different_halves_empty(void **state)
{
    (void)state; /* unused */

    PyElement p1 = {1, 2};
    PyElement p2 = {4, 2};
    PyElement p3 = {3, 2};
    PyElement p4 = {2, 2};
    PyElement Py[] = {p1, p2, p3, p4};
    point reference = p4.p;
    size_t length = 4;
    size_t *candidates_length = malloc(sizeof(size_t));
    float min_distance_upper_bound = .5;
    PyElement *result = get_candidates_from_different_halves(reference, Py, length, candidates_length, min_distance_upper_bound);

    assert_non_null(result);
    assert_int_equal(*candidates_length, 1);
    assert_pyelem_equal(*result, p4);
}

void test_sort_points(void **state)
{
    (void)state; /* unused */

    size_t length = 4;
    point p1 = {0, 0};
    point p2 = {3, 4};
    point p3 = {2, 5};
    point p4 = {1, 4};
    point P[] = {p1, p2, p3, p4};
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    
    sort_points(P, length, Py);

    assert_point_equal(*P, p1);
    assert_point_equal(*(P+1), p4);
    assert_point_equal(*(P+2), p3);
    assert_point_equal(*(P+3), p2);

    assert_point_equal(Py->p, p1);
    assert_int_equal(Py->xposition, 0);
    assert_point_equal((Py+1)->p, p4);
    assert_int_equal((Py+1)->xposition, 1);
    assert_point_equal((Py+2)->p, p2);
    assert_int_equal((Py+2)->xposition, 3);
    assert_point_equal((Py+3)->p, p3);
    assert_int_equal((Py+3)->xposition, 2);
}

void test_nlogn(void **state)
{
    size_t length = 5;
    point P[] = {
        3, 9,
        1, 5,
        0, 1,
        5, 3,
        8, 6};

    points_distance closest_points = nlogn_solution(P, length);
    points_distance expected = {{0, 1}, {1, 5}, 4.12};
    assert_points_distance_equal(closest_points, expected);
}

void test_nlogn_vs_quadratic(void **state)
{
    srand(time(NULL));
    for (size_t i = 2; i < 100; i++)
    {        
        size_t length = i;
        point P1[length];
        point P2[length];
        for (size_t i = 0; i < length; i++)
        {
            int x = rand() % 100 + 1;
            int y = rand() % 100 + 1;
            point p = {x, y};
            P1[i] = p;
            P2[i] = p;
            //printf("(%d,%d)", p.x,p.y);
        }
        //printf("\n");

        points_distance closest_points1 = nlogn_solution(P1, length);
        points_distance closest_points2 = quadratic_solution(P2, length);
        //printf("\n(%d,%d),(%d,%d)\n", closest_points1.p1.x, closest_points1.p1.y, closest_points1.p2.x, closest_points1.p2.y);
        //printf("\n(%d,%d),(%d,%d)\n\n", closest_points2.p1.x, closest_points2.p1.y, closest_points2.p2.x, closest_points2.p2.y);
        assert_float_equal(closest_points1.distance, closest_points2.distance, 0.01);
        
    }
}

void test_nlogn_vs_multiproc(void **state)
{
    srand(time(NULL));
    for (size_t i = 2; i < 100; i++)
    {        
        size_t length = i;
        point P1[length];
        point P2[length];
        for (size_t i = 0; i < length; i++)
        {
            int x = rand() % 100 + 1;
            int y = rand() % 100 + 1;
            point p = {x, y};
            P1[i] = p;
            P2[i] = p;
            //printf("(%d,%d)", p.x,p.y);
        }
        //printf("\n");

        points_distance closest_points1 = nlogn_solution(P1, length);
        points_distance closest_points2 = nlogn_solution_multiproc(P2, length, 4);
        //printf("\n(%d,%d),(%d,%d)\n", closest_points1.p1.x, closest_points1.p1.y, closest_points1.p2.x, closest_points1.p2.y);
        //printf("\n(%d,%d),(%d,%d)\n\n", closest_points2.p1.x, closest_points2.p1.y, closest_points2.p2.x, closest_points2.p2.y);
        assert_points_distance_equal(closest_points1, closest_points2);        
    }
}

void test_nlogn_multiproc_base_case(void **state)
{
    size_t length = 2;
    point p1 = {1,0};
    point p2 = {1,1};
    point P[] = {p1,p2};

    points_distance closest_points = nlogn_solution_multiproc(P, length, 4);
    points_distance expected = {p1,p2, 1.0};
    assert_points_distance_equal(closest_points, expected);
}

void test_nlogn_multiproc(void **state)
{
    size_t length = 7;
    point P[] = {
        3, 9,
        1, 5,
        0, 1,
        5, 3,
        8, 6,
        20,20,
        40,40};

    points_distance closest_points = nlogn_solution_multiproc(P, length, 4);
    points_distance expected = {{0, 1}, {1, 5}, 4.12};
    assert_points_distance_equal(closest_points, expected);
}

void test_nlogn_multithread_base_case(void **state)
{
    size_t length = 2;
    point p1 = {1,0};
    point p2 = {1,1};
    point P[] = {p1,p2};

    points_distance closest_points = nlogn_solution_multithread(P, length, 4);
    points_distance expected = {p1,p2, 1.0};
    assert_points_distance_equal(closest_points, expected);
}

void test_nlogn_multithread(void **state)
{
    size_t length = 7;
    point P[] = {
        3, 9,
        1, 5,
        0, 1,
        5, 3,
        8, 6,
        20,20,
        40,40};

    points_distance closest_points = nlogn_solution_multiproc(P, length, 4);
    points_distance expected = {{0, 1}, {1, 5}, 4.12};
    assert_points_distance_equal(closest_points, expected);
}

int main(int argc, char const *argv[])
{

    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_nlogn_multithread),
        cmocka_unit_test(test_nlogn_multithread_base_case),
        cmocka_unit_test(test_nlogn_vs_multiproc),
        cmocka_unit_test(test_nlogn_multiproc),
        cmocka_unit_test(test_nlogn_multiproc_base_case),
        cmocka_unit_test(test_sort_points),
        cmocka_unit_test(test_nlogn_vs_quadratic),
        cmocka_unit_test(test_get_candidates_from_different_halves),
        cmocka_unit_test(test_get_candidates_from_different_halves_empty),
        cmocka_unit_test(test_nlogn)
        };
    return cmocka_run_group_tests(tests, NULL, NULL);
}
