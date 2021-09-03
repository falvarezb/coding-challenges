#include "closest_point.h"

points_distance nlogn_solution(point P[], size_t length, int num_processes)
{
    assert(length >= 2);
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    return closest_points(P, Py, length);
}

#ifdef FAB_MAIN
int main(int argc, char const *argv[])
{    
    perf_test(nlogn_solution);    
}
#endif
