def merge_list(l1: list, l2: list) -> list:
    """
    Merge two sorted lists, the result must be sorted too
    O(N)

    Args:
        l1 (list): sorted list asc order
        l2 (list): sorted list asc order

    Returns:
        list: (l1 + l2) sorted asc order
    """
    ptr1, ptr2 = 0, 0
    result = []
    while(ptr1 < len(l1) and ptr2 < len(l2)):
        if l1[ptr1] <= l2[ptr2]:
            result.append(l1[ptr1])
            ptr1 += 1
        else:
            result.append(l2[ptr2])
            ptr2 += 1

    if ptr1 == len(l1):
        result.extend(l2[ptr2:len(l2)])
    else:
        result.extend(l1[ptr1:len(l1)])
    return result


def mergesort(l: list) -> list:
    if len(l) == 1:
        return l
    left = mergesort(l[:len(l)//2])
    right = mergesort(l[len(l)//2:])
    return merge_list(left, right)