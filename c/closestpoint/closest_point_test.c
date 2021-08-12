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

void assert_points_distance_equal(points_distance p1, points_distance p2)
{
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
    for (size_t i = 0; i < 100; i++)
    {        
        size_t length = 5;
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

int main(int argc, char const *argv[])
{

    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_nlogn_vs_quadratic),
        cmocka_unit_test(test_get_candidates_from_different_halves),
        cmocka_unit_test(test_get_candidates_from_different_halves_empty),
        cmocka_unit_test(test_nlogn)};
    return cmocka_run_group_tests(tests, NULL, NULL);
}
