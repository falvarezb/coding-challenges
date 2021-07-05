from magicindex.magicindex_solution import magic_index


def test_multiple_magic_index():
    l = [-1, 1, 2, 4, 5]
    assert magic_index(l) == 2


def test_behind_index():
    l = [0, 2, 3, 4, 5]
    assert magic_index(l) == 0


def test_ahead_index():
    l = [-2, 0, 1, 2, 3, 4, 6]
    assert magic_index(l) == 6


def test_no_magicindex():
    l = [-2, 0, 1, 2, 3, 4]
    assert magic_index(l) == -1
