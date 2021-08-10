#include <stdio.h>
#include <math.h>
#include <stdlib.h>

typedef struct
{
    int x;
    int y;
} point;

float distance(point *p1, point *p2)
{
    return sqrt(pow(p1->x - p2->x, 2) + pow(p1->y - p2->y, 2));
}

point *quadratic_solution(point P[], size_t length)
{
    float min_distance = INFINITY;
    float d;
    point *closest_points = (point *)malloc(sizeof(point) * 2);
    if (closest_points == NULL)
        return NULL;

    for (size_t i = 0; i < length - 1; i++)
    {
        for (size_t j = i + 1; j < length; j++)
        {
            d = distance(&P[i], &P[j]);
            if (d < min_distance)
            {
                min_distance = d;
                closest_points[0] = P[i];
                closest_points[1] = P[j];
            }
        }
    }
    return closest_points;
}

int main(int argc, char const *argv[])
{
    point P[] = {
        0, 0,
        3, 4,
        2, 5,
        1, 4};
    point *closest_points = quadratic_solution(P, 4);
    printf("(%d,%d),(%d,%d)", closest_points[0].x, closest_points[0].y, closest_points[1].x, closest_points[1].y);
    return 0;
}
