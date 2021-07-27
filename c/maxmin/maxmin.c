#include <stdio.h>
#include <stdlib.h>

int compar(const void *p1, const void *p2)
{
    const int* intp1 = (const int *)p1;
    const int* intp2 = (const int *)p2;

    return (*intp1 > *intp2) - (*intp1 < *intp2);
}

int maxMin(int k, int arr_count, int *arr)
{
    qsort(arr, arr_count, sizeof(int), compar);
    int min_distance = 1000000000;

    for (size_t i = 0; i < arr_count - k + 1; i++)
    {
        int d = arr[i + k - 1] - arr[i];
        if (d < min_distance)
            min_distance = d;        
    }
    return min_distance;
}

int main(int argc, char const *argv[])
{
    int arr[] = {1, 4, 7, 2};
    printf("result=%d\n", maxMin(2, 4, arr));
    int test_case_16[] = {100,200,300,350,400,401,402};
    printf("result=%d\n", maxMin(3, 7, test_case_16));
    return 0;
}
