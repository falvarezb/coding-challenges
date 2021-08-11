#include <stdio.h>
#include <stdlib.h>

/**
 * Given 2 sorted arrays, 'arr1' and 'arr2', each of them with 'num1' and 'num2' elements of
 * the same type and with size 'size':
 * merge 'arr1' and 'arr2' in such a way that the resulting array is also sorted
 * 
 * 'compare' is the function used to compare the elements of the array
 * 
 * Implementation notes:
 * - the type of the arrays is generic (void*)
 * - in order to use pointer arithmetic, it is necessary to cast the type to 'char*', that
 * is equivalent to deal with bytes directly
 * - that's why we need the parameter 'size': to know how to interpret the bytes
 */
void *merge_lists(void *arr1, size_t num1,
                  void *arr2, size_t num2,
                  size_t size,
                  int (*compare)(const void *, const void *))
{
    char *result = (char *)malloc((num1 + num2) * size);
    if (result == NULL)
        return NULL;

    size_t i = 0; //index over elements of arr1
    size_t j = 0; //index over elements of arr2
    size_t k = 0; //index over bytes of result
    while (i < num1 && j < num2)
    {
        char *x = (char *)arr1 + i * size;
        char *y = (char *)arr2 + j * size;
        if (compare(x, y) <= 0)
        {
            //copy i-th element of arr1 to result (byte by byte)
            for (size_t m = 0; m < size; m++)
            {
                *(result + k) = *(x++);
                k++;
            }
            i++;
        }
        else
        {
            //copy j-th element of arr2 to result (byte by byte)
            for (size_t m = 0; m < size; m++)
            {
                *(result + k) = *(y++);
                k++;
            }
            j++;
        }
    }

    if (i == num1)
    {
        //copy remaining elements of arr2 to result (byte by byte)
        for (size_t m = j * size; m < num2 * size; m++)
        {
            *(result + k) = *((char *)arr2 + m);
            k++;
        }
    }
    else
    {
        //copy remaining elements of arr1 to result (byte by byte)
        for (size_t m = i * size; m < num1 * size; m++)
        {
            *(result + k) = *((char *)arr1 + m);
            k++;
        }
    }

    return result;
}

void *mymergesort(void *base, size_t num, size_t size, int (*compar)(const void *, const void *))
{
    if (num == 1)
    {
        char *result = (char *) malloc(size);
        for (size_t m = 0; m < size; m++)
            *(result+m) = *((char *)base+m);
        return result;
    }

    void *left = mymergesort(base, num / 2, size, compar);
    void *right = mymergesort((char*)base + (num / 2)*size, num - num / 2, size, compar);
    void *result = merge_lists(left, num / 2, right, num - num / 2, size, compar);
    free(left);
    free(right);
    return result;
}

int compar(const void *p1, const void *p2)
{
    const int *intp1 = (const int *)p1;
    const int *intp2 = (const int *)p2;
    return (*intp1 > *intp2) - (*intp1 < *intp2);
}

int main(int argc, char const *argv[])
{
    int arr1[] = {1, 4, 7, 8};
    int arr2[] = {2, 3, 6, 9, 10};
    size_t num1 = 4;
    size_t num2 = 5;
    int *result = merge_lists(arr1, num1, arr2, num2, sizeof(int), compar);
    for (size_t i = 0; i < num1 + num2; i++)
        printf("result[%zu]=%d\n", i, *(result + i));

    int base[] = {2,1,5,3,8,4,3};
    size_t num = 7;
    size_t size = sizeof(int);
    int* mergesort_result = mymergesort(base, num, size, compar);
    for (size_t i = 0; i < num; i++)
        printf("mergesort_result[%zu]=%d\n", i, *(mergesort_result + i));

    return 0;
}
