#include <stddef.h>
#include <stdarg.h>
#include <setjmp.h>
#include <cmocka.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <time.h>
#include <stdbool.h>
#include "closest_point.h"

struct testcase {
    size_t length;
    point* P;
    points_distance expected;
    int num_processes;
};

struct testcase tc1()
{   
    int num_points = 2; 
    point p1 = {1,0};
    point p2 = {1,1};    
    point* P = malloc(sizeof(point)*num_points);
    P[0] = p1;
    P[1] = p2;      
    return (struct testcase) {num_points, P, {p1,p2, 1.0}, 4};
}

struct testcase tc2()
{
    int num_points = 7; 
    point* P = malloc(sizeof(point)*num_points);
    P[0] = (point){3,9};
    P[1] = (point){1, 5};
    P[2] = (point){0, 1};
    P[3] = (point){5, 3};
    P[4] = (point){8, 6};
    P[5] = (point){20,20};
    P[6] = (point){40,40};
    return (struct testcase) {num_points, P, {{0, 1}, {1, 5}, 4.12}, 4};
}

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

void assert_points_distance_equal(points_distance p1, points_distance p2, bool only_distance)
{
    if (!only_distance)
    {            
        assert_point_equal(p1.p1, p2.p1);
        assert_point_equal(p1.p2, p2.p2);
    }
    assert_float_equal(p1.distance, p2.distance, 0.01);
}

void compare_solutions(points_distance (*func1) (point P[], size_t length, int num_processes), points_distance (*func2) (point P[], size_t length, int num_processes), bool only_distance)
{
    const int max_num_points = 100;
    srand(time(NULL));
    for (size_t i = 2; i < max_num_points; i++)
    {        
        size_t length = i;
        point P1[length];
        point P2[length];
        for (size_t i = 0; i < length; i++)
        {
            int x = rand() % max_num_points + 1;
            int y = rand() % max_num_points + 1;
            point p = {x, y};
            P1[i] = p;
            P2[i] = p;         
        }        
        points_distance closest_points1 = func1(P1, length, 4);
        points_distance closest_points2 = func2(P2, length, 4);        
        assert_points_distance_equal(closest_points1, closest_points2, only_distance);        
    }
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
    struct testcase tc = tc2();
    points_distance closest_points = nlogn_solution(tc.P, tc.length, tc.num_processes);    
    assert_points_distance_equal(closest_points, tc.expected, false);
}

void test_nlogn_multiproc_base_case(void **state)
{
    struct testcase tc = tc1();
    points_distance closest_points = nlogn_solution_multiproc(tc.P, tc.length, tc.num_processes);    
    assert_points_distance_equal(closest_points, tc.expected, false);
}

void test_nlogn_multiproc(void **state)
{
    struct testcase tc = tc2();
    points_distance closest_points = nlogn_solution_multiproc(tc.P, tc.length, tc.num_processes);    
    assert_points_distance_equal(closest_points, tc.expected, false);
}

void test_nlogn_multithread_base_case(void **state)
{    
    struct testcase tc = tc1();
    points_distance closest_points = nlogn_solution_multithread(tc.P, tc.length, tc.num_processes);    
    assert_points_distance_equal(closest_points, tc.expected, false);
}

void test_nlogn_multithread(void **state)
{
    struct testcase tc = tc2();
    points_distance closest_points = nlogn_solution_multithread(tc.P, tc.length, tc.num_processes);    
    assert_points_distance_equal(closest_points, tc.expected, false);
}

void test_nlogn_vs_quadratic(void **state)
{
    compare_solutions(nlogn_solution, quadratic_solution, true);
}

void test_nlogn_vs_multiproc(void **state)
{
    compare_solutions(nlogn_solution, nlogn_solution_multiproc, false);
}

void test_multiproc_vs_multithread(void **state)
{
    compare_solutions(nlogn_solution_multithread, nlogn_solution_multiproc, false);
}

int main(int argc, char const *argv[])
{

    const struct CMUnitTest tests[] = {        
        cmocka_unit_test(test_multiproc_vs_multithread),
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
