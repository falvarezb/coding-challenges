
class Stack:
    """
    Stack implementation based on a list
    The end of the list is the top of the stack
    The elements of the stack must be comparable as the implementation does not allow to push an element on top of a smaller one
    """
    def __init__(self):
        self.arr = []

    def push(self, x):
        if len(self.arr) > 0 and self.arr[-1] <= x:
            raise ValueError("too large a disk!")
        self.arr.append(x)

    def pop(self):
        return self.arr.pop()

    def __len__(self):
        return len(self.arr)

    @staticmethod
    def factory_n(n: int):
        stack = Stack()
        for i in range(n,0,-1):
            stack.push(i)
        return stack

    @staticmethod
    def factory_arr(arr: list):
        stack = Stack()
        for i in arr:
            stack.push(i)
        return stack


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

    # Split tower1 to solve the smaller problem with n-1 disks    
    smaller_case = Stack.factory_arr((tower1.arr[1:len(tower1.arr)]))
    for _ in range(len(tower1)-1):
        tower1.pop()

    # recursive calls
    move_disks(smaller_case, tower3, tower2)
    tower3.push(tower1.pop())
    move_disks(tower2, tower1, tower3)