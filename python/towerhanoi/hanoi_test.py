from towerhanoi.hanoi_solution import *

def test_basecase():
    tower1, tower2, tower3 = Stack.factory_n(2), Stack(), Stack()
    solve(tower1, tower2, tower3)
    assert tower1.arr == []
    assert tower3.arr == [2,1]

def test_recursivecase():
    tower1, tower2, tower3 = Stack.factory_n(3), Stack(), Stack()
    solve(tower1, tower2, tower3)
    assert tower1.arr == []
    assert tower3.arr == [3,2,1]