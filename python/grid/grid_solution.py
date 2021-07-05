
import functools

@functools.lru_cache()
def num_paths(m: int, n: int):
    """
    Find number of paths to traverse a 'm x n' grid from the top left to the bottom right
    Allowed movements are right and down

    Args:
        m (int): number of rows
        n (int): number of columns
    """
    if m == 1 or n == 1:
        return 1
    return num_paths(m, n-1) + num_paths(m-1,n)

def num_paths_forbidden_cells(m: int, n: int, forbidden_cells: list):
    """
    Same as above but now some of the cells are forbidden
    """

    if (m, n) in forbidden_cells:
        return 0

    if m == 1 or n == 1:
        return 1

    return num_paths_forbidden_cells(m, n-1, forbidden_cells) + num_paths_forbidden_cells(m-1,n, forbidden_cells)


def paths(m: int, n: int):
    """
    Find paths to traverse a 'm x n' grid from the top left to the bottom right
    Allowed movements are right and down
    Length of the paths is m+n-1

    Args:
        m (int): number of rows
        n (int): number of columns
    """
    if m == 1:
        return [[(1,i) for i in range(1,n+1)]]

    if n == 1:
        return [[(i,1) for i in range(1,m+1)]]

    return [path + [(m,n)] for path in (paths(m, n-1) + paths(m-1,n))]


def paths_forbidden_cells(m: int, n: int, forbidden_cells: list):
    """
    Same as above but now some of the cells are forbidden
    """

    if (m,n) in forbidden_cells:
        return [[(0,0)]]

    if m == 1:
        return [[(1,i) for i in range(1,n+1)]]

    if n == 1:
        return [[(i,1) for i in range(1,m+1)]]

    return [path + [(m,n)] for path in (paths_forbidden_cells(m, n-1,forbidden_cells) + paths_forbidden_cells(m-1,n,forbidden_cells)) if (0,0) not in path]


if __name__ == '__main__':
    print(paths_forbidden_cells(4,5,[(2,2),(2,5),(3,4)]))

