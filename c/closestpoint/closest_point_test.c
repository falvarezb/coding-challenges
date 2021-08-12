#include <stddef.h>
#include <stdarg.h>
#include <setjmp.h>
#include <cmocka.h>
#include "closest_point.h"

void assert_pyelem_equal(PyElement p1, PyElement p2)
{
    assert_int_equal(p1.p.x, p2.p.x);
    assert_int_equal(p1.p.y, p2.p.y);
    assert_int_equal(p1.xposition, p2.xposition);
}

void test_get_candidates_from_different_halves(void** state){
    (void) state; /* unused */

    point reference = {2,2};
    PyElement p1 = {1,2};
    PyElement p2 = {4,2};
    PyElement p3 = {3,2};
    PyElement p4 = {2,2};    
    PyElement Py[] = {p1, p2, p3, p4};
    size_t length = 4;
    size_t *candidates_length = malloc(sizeof(size_t));
    float min_distance_upper_bound = 1.5;
    PyElement* result = get_candidates_from_different_halves(reference, Py, length, candidates_length, min_distance_upper_bound);

    
    assert_non_null(result);
    assert_int_equal(*candidates_length, 3);  
    assert_pyelem_equal(*result, p1);
    assert_pyelem_equal(*(result+1), p3);
    assert_pyelem_equal(*(result+2), p4);  
}

void test_get_candidates_from_different_halves_empty(void** state){
    (void) state; /* unused */

    point reference = {2,2};
    PyElement p1 = {1,2};
    PyElement p2 = {4,2};
    PyElement p3 = {3,2};
    PyElement p4 = {2,2};    
    PyElement Py[] = {p1, p2, p3, p4};
    size_t length = 4;
    size_t *candidates_length = malloc(sizeof(size_t));
    float min_distance_upper_bound = .5;
    PyElement* result = get_candidates_from_different_halves(reference, Py, length, candidates_length, min_distance_upper_bound);

    
    assert_non_null(result);
    assert_int_equal(*candidates_length, 1);  
    assert_pyelem_equal(*result, p4); 
}

int main(int argc, char const *argv[])
{
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(test_get_candidates_from_different_halves),
        cmocka_unit_test(test_get_candidates_from_different_halves_empty)      
    };
    return cmocka_run_group_tests(tests, NULL, NULL);
}



