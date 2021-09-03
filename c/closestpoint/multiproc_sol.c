#include "closest_point.h"


void closest_points_multiproc(point Px[], PyElement Py[], size_t length, points_distance *result, int par_threshold)
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
            exit(1);
        points_distance *right_result = (points_distance *)malloc(sizeof(points_distance));

        switch (fork())
        {
        case -1: //error
            exit(2);
        case 0: //child
            //closest points in the left half
            //printf("pid=%d, ppid=%d, child\n", getpid(), getppid());
            closest_points_multiproc(Px, Ly, left_size, left_result, par_threshold);
            _exit(10);
        default: //parent
            //closest points in the right half
            closest_points_multiproc(Px + right_half_lower_bound, Ry, right_size, right_result, par_threshold);
            int status;
            pid_t child_pid;
            do
            {
                child_pid = wait(&status);
            } while (child_pid == -1 && errno == EINTR);
            if (child_pid == -1 && errno != ECHILD)            
                errExit("error while waiting");                    
            //printWaitStatus(NULL, status);

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
                exit(4);
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

points_distance nlogn_solution_multiproc(point P[], size_t length, int num_processes)
{
    //printf("pid=%d, ppid=%d, main\n", getpid(), getppid());
    assert(length >= 2);
    int par_threshold = ceil((float)length / num_processes);
    points_distance *result = (points_distance *)malloc(sizeof(points_distance));
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    closest_points_multiproc(P, Py, length, result, par_threshold);
    return *result;
}

#ifdef FAB_MAIN
int main(int argc, char const *argv[])
{    
    perf_test(nlogn_solution_multiproc);    
}
#endif
