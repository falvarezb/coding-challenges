from grid.grid_solution import num_paths, paths, num_paths_forbidden_cells, paths_forbidden_cells

def test_num_paths_1x1():
    assert num_paths(1,1) == 1

def test_num_paths_2x2():
    assert num_paths(2,2) == 2

def test_num_paths_3x3():
    assert num_paths(3,3) == 6

def test_num_paths_2x4():
    assert num_paths(2,4) == 4

def test_num_paths_3x4():
    # 3x4 = 3x3 + 2x4
    assert num_paths(3,4) == 10

def test_paths_1x1():
    assert paths(1,1) == [[(1,1)]]

def test_paths_2x2():
    assert paths(2,2) == [[(1,1), (2,1), (2,2)], [(1,1), (1,2), (2,2)]]


# VERSION WITH FORBIDDEN CELLS

def test_num_paths_1x1_forbid():
    assert num_paths_forbidden_cells(1,1,[]) == 1

def test_num_paths_2x2_forbid():
    assert num_paths_forbidden_cells(2,2,[(1,2)]) == 1

def test_num_paths_2x2_nopaths():
    assert num_paths_forbidden_cells(2,2,[(1,2),(2,1)]) == 0

def test_paths_1x1_forbid():
    assert paths_forbidden_cells(1,1,[]) == [[(1,1)]]

def test_paths_2x2_forbid():
    assert paths_forbidden_cells(2,2,[(1,2)]) == [[(1,1), (2,1), (2,2)]]

def test_paths_2x2_forbid_nopaths():
    assert paths_forbidden_cells(2,2,[(1,2),(2,1)]) == []


def test_num_paths_3x4_forbid():    
    assert num_paths_forbidden_cells(3,4,[(1,4),(2,2)]) == 3

def test_paths_3x4_forbid():    
    assert paths_forbidden_cells(3,4,[(1,4),(2,2)]) == [[(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4)], [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)], [(1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]]





