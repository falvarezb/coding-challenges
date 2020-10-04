def remove_permutations(ls: 'list of lists') -> 'list of lists':
    """
    given a list of lists, this function returns a new list without permutations

    Example:

    [[2,1,3], [3,1,2], [1,1]] -> [[1,2,3], [1,1]]
    """
    new_list = []
    for l in ls:
        l = sorted(l)
        if l not in new_list:
            new_list.append(l)
    return new_list


def list1_is_subset_of_list2(list1, list2):
    """
    Checks if list1 is a subset of list2
    """

    return all(l in list2 for l in list1)


def list1_equals_list2_except_order(list1, list2):
    """
    Checks if two lists are equal (without considering the order of the elements)

    So basically it is a 'set' comparison. 
    We cannot use 'set' though because the elements of the lists may also be lists, and lists are not hashable)
    """

    return list1_is_subset_of_list2(list1, list2) and list1_is_subset_of_list2(list2, list1)