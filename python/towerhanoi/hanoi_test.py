from towerhanoi.hanoi_solution import *


def test_basecase():
    tower1, tower2, tower3 = Stack.factory_n(1), Stack.empty(), Stack.empty()
    assert tower1 == Stack([1])
    assert tower2 == Stack.empty()
    assert tower3 == Stack.empty()
    move_disks(tower1, tower2, tower3)
    assert tower1 == Stack.empty()
    assert tower2 == Stack.empty()
    assert tower3 == Stack([1])

def test_2elem():
    tower1, tower2, tower3 = Stack.factory_n(2), Stack.empty(), Stack.empty()
    assert tower1 == Stack([2,1])
    assert tower2 == Stack.empty()
    assert tower3 == Stack.empty()
    move_disks(tower1, tower2, tower3)
    assert tower1 == Stack.empty()
    assert tower2 == Stack.empty()
    assert tower3 == Stack([2,1])

def test_3elem():
    tower1, tower2, tower3 = Stack.factory_n(3), Stack.empty(), Stack.empty()
    assert tower1 == Stack([3,2,1])
    assert tower2 == Stack.empty()
    assert tower3 == Stack.empty()
    move_disks(tower1, tower2, tower3)
    assert tower1 == Stack.empty()
    assert tower2 == Stack.empty()
    assert tower3 == Stack([3,2,1])