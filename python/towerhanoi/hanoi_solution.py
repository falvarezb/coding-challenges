
class Stack:
    """
    Stack implementation based on a list
    The end of the list is the top of the stack
    The elements of the stack must be comparable as the implementation does not allow to push an element on top of a smaller one
    """

    empty_stack = None

    def __init__(self, arr: list):
        self._arr = arr

    def push(self, x):
        if len(self._arr) > 0 and self._arr[-1] <= x:
            raise ValueError("too large a disk!")
        self._arr.append(x)

    def pop(self):
        return self._arr.pop()

    def __len__(self):
        return len(self._arr)

    def __getitem__(self, position):
        return self._arr[position]

    def __eq__(self, value):
        return self._arr.__eq__(value._arr)

    @staticmethod
    def factory_n(n: int):
        stack = Stack(list(range(n, 0, -1)))
        return stack

    @staticmethod
    def empty():
        return Stack([])


def move_disks(tower1: Stack, tower2: Stack, tower3: Stack):
    """
    Solves the problem of the towers of Hanoi: to move disks from tower1 to tower3 using "buffer" tower2 to make
    sure that, during the process, smaller disks are always on top of larger ones.

    Disks are represented as integers representing the relative size of each element, so that disk 'm' is larger than disk 'n'
    iff m > n
    """
    # Recursive algorithm
    # base case
    if len(tower1) == 1:
        tower3.push(tower1.pop())
        return

    # recursive calls
    for _ in range(len(tower1)-1):
        tower1.pop()

    move_disks(tower1[1:len(tower1)], tower3, tower2)
    tower3.push(tower1.pop())
    move_disks(tower2, tower1, tower3)
