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

points_distance nlogn_solution(point P[], size_t length, int num_processes)
{
    assert(length >= 2);
    PyElement *Py = (PyElement *)malloc(length * sizeof(PyElement));
    sort_points(P, length, Py);
    return closest_points(P, Py, length);
}

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



void perf_test(points_distance (*func) (point P[], size_t length, int num_processes))
{
    srand(time(NULL));
    size_t length = 1000000;
    point *P = malloc(sizeof(point) * length);
    for (size_t i = 0; i < length; i++)
    {
        int x = rand() % (length * 10) + 1;
        int y = rand() % (length * 10) + 1;
        point p = {x, y};
        P[i] = p;
    }
    int num_processes = 16;
    {
        struct timespec start, finish;
        double elapsed;

        clock_gettime(CLOCK_MONOTONIC, &start);
        points_distance closest_points = func(P, length, num_processes);

        clock_gettime(CLOCK_MONOTONIC, &finish);

        elapsed = (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
        printf("time=%.4f seconds\n", elapsed);
    }
}

#ifdef FAB_MAIN
int main(int argc, char const *argv[])
{    
    perf_test(nlogn_solution_multiproc);
    perf_test(nlogn_solution_multithread);
}
#endif
