from merge_sorted_lists.merge_sorted_list import *

def test_l1endsfirst():
    assert merge_list([1,3,6,7], [2,4,5,9]) == [1,2,3,4,5,6,7,9]

def test_l2endsfirst():
    assert merge_list([1,3,6,7,10], [2,4,5,9]) == [1,2,3,4,5,6,7,9,10]


def test_mergesort():
    assert mergesort([1,6,2,3,8,9,4]) == [1,2,3,4,6,8,9]