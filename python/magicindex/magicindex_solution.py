def magic_index(l: list):
    """
    Simplest approach is to iterate over the array checking the value of each element, resulting
    in a time complexity of O(N)

    However, given the constraints of the problem, namely:
    * integers are sorted in ascending order
    * there are no duplicate elements
    
    then it is possible to reduce time complexity to O(log N) by using binary search based on the
    following observations:
    (1) i < j => a[i] < a[j]
    (2) i < a[i] => j < a[j] for all j > i (behind index)
    (3) a[i] < i => a[j] < j for all j < i (ahead index)

    Args:
        l (list): list of sorted integers without repeat elements

    Returns:
        int: magic index, else -1. If multiple magic indexes exist, the first one found is returned
    """
    lo, hi = 0, len(l)
    while lo < hi:
        mid = (lo+hi)//2
        if mid < l[mid]:
            hi = mid
        elif l[mid] < mid:
            lo = mid + 1
        else:
            return mid
    return -1
