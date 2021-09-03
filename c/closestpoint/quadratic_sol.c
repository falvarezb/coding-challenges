#include "closest_point.h"

points_distance quadratic_solution(point P[], size_t length, int num_processes)
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

#ifdef FAB_MAIN
int main(int argc, char const *argv[])
{    
    perf_test(quadratic_solution);    
}
#endif
