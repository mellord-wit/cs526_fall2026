# hw6 heap.py

import random
import sys

'''
Solution to Problem 2, implementing a heap.

What a heap is
--------------
A (binary) min-heap is a complete binary tree in which every node's value
is less than or equal to the values of its children. "Complete" means
every level is full except possibly the last, which is filled from the
left. Two things follow:
    - The smallest value is always at the root.
    - The tree has height floor(log2 n), so walking from the root to a
      leaf or back takes O(log n) steps.

Storing the tree in a list
--------------------------
Because the tree is complete, it is stored in a plain list with no node
objects or pointers. The root is at index 0 and the levels follow one
after another, left to right. For the node at index i:
    left child  = 2 * i + 1
    right child = 2 * i + 2
    parent      = (i - 1) // 2
For example, the list [3, 8, 5, 12, 9, 7] is the tree
            3
          /   \\
         8     5
        / \\   /
      12   9 7

The two repair operations
-------------------------
Every heap operation makes one change that may put a single value in the
wrong place, then moves that value until the heap order holds again.
    sift_up(i):   while the value at i is smaller than its parent, swap it
                  with its parent. Used after adding a value at the bottom.
    sift_down(i): while the value at i is larger than its smaller child,
                  swap it with that child. Used after putting a value at
                  the top. Swapping with the smaller child is what keeps
                  the order correct: the child that moves up is then
                  smaller than both values below it.
Each moves along one root-to-leaf path, so each is O(log n).

Operations
----------
    insert(value)   Add the value at the end of the list (the next free
                    spot on the bottom level), then sift_up. O(log n)
    peek()          Return the root, the smallest value. O(1)
    extract_min()   Remove and return the root. The last value in the list
                    is moved to the root to keep the tree complete, then
                    sift_down. O(log n)
    delete(value)   Remove any one copy of a value. Find its index (O(n),
                    since a heap is not ordered for searching), move the
                    last value into that spot, then sift_up or sift_down,
                    whichever is needed. O(n)
    build(values)   Turn a whole list into a heap at once. O(n), see below.
    heap_sort()     Return the values in increasing order by extracting
                    the minimum n times from a copy. O(n log n)

Building a heap in O(n)
-----------------------
Inserting n values one at a time costs O(n log n). build instead copies
the values into the list as they are and calls sift_down on every node
that has a child, from the last such node (index n // 2 - 1) back to the
root. Going backwards means that when a node is sifted down, both of its
subtrees are already heaps, so sift_down finishes the job for that node.
Most nodes are near the bottom and can only move a step or two, which is
why the total work adds up to O(n) rather than O(n log n).

The demonstration
-----------------
main generates a random set of 5 to 50 values between 1 and 1000, builds a
heap from it, and prints the heap after every operation: inserts (new
values), extract_min, delete of a value that is in the heap, and delete of
a value that is not. It finishes with heap_sort, and checks the heap order
after every step. Pass a number on the command line to use it as the
random seed, so a run can be repeated:
    python3 heap.py          (different values every run)
    python3 heap.py 526      (the same values every time)
'''


class MinHeap:
    '''Binary min-heap stored in a list.'''

    def __init__(self, values=None):
        self.items = []
        if values:
            self.build(values)

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self.items[0]

    def insert(self, value):
        self.items.append(value)
        self._sift_up(len(self.items) - 1)

    def extract_min(self):
        if self.is_empty():
            raise IndexError("extract_min from an empty heap")
        smallest = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._sift_down(0)
        return smallest

    def delete(self, value):
        '''Remove one copy of value; return False if it is not in the heap.'''
        if value not in self.items:
            return False
        index = self.items.index(value)
        last = self.items.pop()
        if index < len(self.items):
            self.items[index] = last
            # the moved value may belong above or below its new spot
            self._sift_up(index)
            self._sift_down(index)
        return True

    def build(self, values):
        self.items = list(values)
        for index in range(len(self.items) // 2 - 1, -1, -1):
            self._sift_down(index)

    def heap_sort(self):
        copy = MinHeap()
        copy.items = list(self.items)
        result = []
        while not copy.is_empty():
            result.append(copy.extract_min())
        return result

    def is_valid(self):
        for index in range(1, len(self.items)):
            if self.items[index] < self.items[(index - 1) // 2]:
                return False
        return True

    def _swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.items[index] >= self.items[parent]:
                break
            self._swap(index, parent)
            index = parent

    def _sift_down(self, index):
        size = len(self.items)
        while True:
            smallest = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < size and self.items[child] < self.items[smallest]:
                    smallest = child
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def print_heap(self):
        '''Print the list, then the tree one level per line.'''
        print("  list:", self.items)
        if self.is_empty():
            print("  (empty heap)")
            return
        start = 0
        level = 0
        while start < len(self.items):
            end = min(2 * start + 1, len(self.items))
            print("  level %d:" % level, " ".join(str(v) for v in self.items[start:end]))
            start = end
            level += 1


def show(heap, title):
    print()
    print(title)
    heap.print_heap()
    print("  size: %d, valid heap: %s" % (len(heap), heap.is_valid()))


def main():
    if len(sys.argv) > 1:
        random.seed(int(sys.argv[1]))

    size = random.randint(5, 50)
    values = [random.randint(1, 1000) for _ in range(size)]
    print("Input set (%d values):" % size, values)

    heap = MinHeap(values)
    show(heap, "Initial heap built from the input set:")
    print("  peek (smallest value):", heap.peek())

    for _ in range(3):
        value = random.randint(1, 1000)
        heap.insert(value)
        show(heap, "After insert(%d):" % value)

    for _ in range(2):
        smallest = heap.extract_min()
        show(heap, "After extract_min() returned %d:" % smallest)

    present = random.choice(heap.items)
    heap.delete(present)
    show(heap, "After delete(%d) (value was in the heap):" % present)

    missing = random.randint(1, 1000)
    while missing in heap.items:
        missing = random.randint(1, 1000)
    found = heap.delete(missing)
    print()
    print("delete(%d): value not in the heap, deleted = %s" % (missing, found))

    print()
    print("heap_sort():", heap.heap_sort())

main()
