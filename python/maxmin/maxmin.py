def maxMin(k, arr):
    arr = sorted(arr)
    min_distance = 10**9

    for i in range(len(arr)-k+1):
        d = arr[i+k-1] - arr[i]
        if d < min_distance:
            min_distance = d

    return min_distance


if __name__ == "__main__":
    print(maxMin(2, [1, 4, 7, 2]))
    test_case_16 = (3, [100,200,300,350,400,401,402])
    print(maxMin(*test_case_16))
