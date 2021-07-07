from towerhanoi.hanoi_solution import *


def test_basecase():
    tower1, tower2, tower3 = Stack.factory_n(1), Stack(), Stack()
    assert tower1.arr == [1]
    assert tower2.arr == []
    assert tower3.arr == []
    move_disks(tower1, tower2, tower3)
    assert tower1.arr == []
    assert tower2.arr == []
    assert tower3.arr == [1]

def test_2elem():
    tower1, tower2, tower3 = Stack.factory_n(2), Stack(), Stack()
    assert tower1.arr == [2,1]
    assert tower2.arr == []
    assert tower3.arr == []
    move_disks(tower1, tower2, tower3)
    assert tower1.arr == []
    assert tower2.arr == []
    assert tower3.arr == [2,1]

def test_3elem():
    tower1, tower2, tower3 = Stack.factory_n(3), Stack(), Stack()
    assert tower1.arr == [3,2,1]
    assert tower2.arr == []
    assert tower3.arr == []
    move_disks(tower1, tower2, tower3)
    assert tower1.arr == []
    assert tower2.arr == []
    assert tower3.arr == [3,2,1]