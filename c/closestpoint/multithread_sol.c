#include "closest_point.h"

void* closest_points_multithread(void* targs)
{
    thread_arg* args = (thread_arg*) targs;
    if (args->length == 2)
    {
        args->result->p1 = args->Px[0];
        args->result->p2 = args->Px[1];
        args->result->distance = distance(args->result->p1, args->result->p2);        
    }
    else if (args->length > args->par_threshold)
    {
        size_t left_half_upper_bound = ceil(args->length / 2.);
        size_t right_half_lower_bound = floor(args->length / 2.);
        size_t left_size = left_half_upper_bound;
        size_t right_size = args->length - right_half_lower_bound;
        PyElement *Ly = (PyElement *)malloc(left_size * sizeof(PyElement));
        PyElement *Ry = (PyElement *)malloc(right_size * sizeof(PyElement));

        populateLy(args->Py, args->length, Ly, left_half_upper_bound);
        populateRy(args->Py, args->length, Ry, right_half_lower_bound);

        points_distance *left_result = (points_distance *)malloc(sizeof(points_distance));
        points_distance *right_result = (points_distance *)malloc(sizeof(points_distance));

        //new thread
        //closest points in the left half        
        pthread_t thread;
        thread_arg* left_args = malloc(sizeof(thread_arg));
        left_args->Px = args->Px;
        left_args->Py = Ly;
        left_args->length = left_size;
        left_args->result = left_result;
        left_args->par_threshold = args->par_threshold;
        int s = pthread_create(&thread, NULL, closest_points_multithread, left_args);            
        if (s != 0)        
            errExit("pthread_create");        
        

        //current thread
        //closest points in the right half            
        thread_arg* right_args = malloc(sizeof(thread_arg));
        right_args->Px = args->Px + right_half_lower_bound;
        right_args->Py = Ry;
        right_args->length = right_size;
        right_args->result = right_result;
        right_args->par_threshold = args->par_threshold;
        closest_points_multithread(right_args);
        s = pthread_join(thread, NULL);
        if (s != 0)        
            errExit("pthread_join");        

        float min_left_distance = left_result->distance;
        float min_right_distance = right_result->distance;

        float min_distance_upper_bound = MIN(min_left_distance, min_right_distance);
        size_t *candidates_length = (size_t *)malloc(sizeof(size_t));
        PyElement *candidates = get_candidates_from_different_halves(*(args->Px + left_size - 1), args->Py, args->length, candidates_length, min_distance_upper_bound);
        points_distance closest_candidates = closest_points_from_different_halves(candidates, *candidates_length);

        free(candidates_length);
        free(Ly);
        free(Ry);
        free(candidates);

        if (closest_candidates.distance < min_distance_upper_bound)
        {
            args->result->p1 = closest_candidates.p1;
            args->result->p2 = closest_candidates.p2;
            args->result->distance = closest_candidates.distance;
        }
        else if (min_left_distance < min_right_distance)
        {
            args->result->p1 = left_result->p1;
            args->result->p2 = left_result->p2;
            args->result->distance = left_result->distance;
        }
        else
        {
            args->result->p1 = right_result->p1;
            args->result->p2 = right_result->p2;
            args->result->distance = right_result->distance;
        }
        free(right_result);
    }
    else
    {
        points_distance intermediate_result = closest_points(args->Px, args->Py, args->length);
        args->result->p1 = intermediate_result.p1;
        args->result->p2 = intermediate_result.p2;
        args->result->distance = intermediate_result.distance;
    }
    return NULL;
}

points_distance nlogn_solution_multithread(point P[], size_t length, int num_processes)
{    
    assert(length >= 2);
    int par_threshold = ceil((float)length / num_processes);
    points_distance *result = (points_distance *)malloc(sizeof(points_distance));
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    thread_arg* args = malloc(sizeof(thread_arg));
    args->Px = P;
    args->Py = Py;
    args->length = length;
    args->result = result;
    args->par_threshold = par_threshold;
    closest_points_multithread(args);
    return *result;
}


#ifdef FAB_MAIN
int main(int argc, char const *argv[])
{        
    perf_test(nlogn_solution_multithread);
}
#endif
