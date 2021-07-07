
class Stack:
    def __init__(self, arr: list):
        self.arr = arr

    def push(self, x):
        if len(self.arr) > 0 and self.arr[-1] <= x:
            raise ValueError("too large a disk!")
        self.arr.append(x)

    def pop(self):
        return self.arr.pop()

    def __len__(self):
        return len(self.arr)


def solve(tower1: Stack, tower2: Stack, tower3: Stack) -> Stack:
    """
    Solves the problem of the towers of Hanoi: moves elements from tower1 to tower3 using auxiliary tower2 to make
    sure that, during the process, smaller disks are always on top of larger ones

    Args:
        tower1 (Stack): list of numbers representing the relative size of each element in descending order

    Returns:
        Stack: list of numbers representing the relative size of each element in ascending order
    """

    # base case
    if len(tower1) == 2:
        tower2.push(tower1.pop())
        tower3.push(tower1.pop())
        tower3.push(tower2.pop())
        return

    # Split tower1 to solve the smaller problem with n-1 disks
    smaller_case = Stack(tower1.arr[1:len(tower1.arr)])
    for _ in range(len(tower1)-1):
        tower1.pop()
    solve(smaller_case, tower2, tower3)

    tower2.push(tower1.pop())
    solve(tower3, tower2, tower1)
    tower3.push(tower2.pop())
    solve(tower1, tower2, tower3)
    return
