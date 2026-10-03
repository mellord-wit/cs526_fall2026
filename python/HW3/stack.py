"""
Stack reversal solution for HW3 (Problem 3).

The same stack is implemented three ways: on an array (a Python list), on a singly
linked list, and on a doubly linked list. Each class has a reverse() method that
reverses the stack in place using recursion.

to_list() returns the stack from bottom to top, so pushing 1..10 gives
1, 2, ..., 10 and reversing it gives 10, 9, ..., 1.
"""


class ArrayStack:
    """Stack stored in a Python list; the top of the stack is the end of the list."""

    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)

    def reverse(self):
        self._reverse(0, len(self.items) - 1)

    def _reverse(self, low, high):
        # Swap the two outer items, then reverse everything between them.
        if low >= high:
            return
        self.items[low], self.items[high] = self.items[high], self.items[low]
        self._reverse(low + 1, high - 1)


class Node:
    """Node for the singly linked list stack."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedListStack:
    """Stack stored in a singly linked list; head is the top of the stack."""

    def __init__(self):
        self.head = None
        self.count = 0

    def push(self, value):
        self.head = Node(value, self.head)
        self.count += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        value = self.head.value
        self.head = self.head.next
        self.count -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.head.value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.count

    def to_list(self):
        # Walk from the top down, then flip so the list reads bottom to top.
        values = []
        node = self.head
        while node is not None:
            values.append(node.value)
            node = node.next
        values.reverse()
        return values

    def reverse(self):
        self.head = self._reverse(self.head, None)

    def _reverse(self, node, previous):
        # Point this node back at the previous one, then move on to the rest of the list.
        # When the end is reached, the last node becomes the new head.
        if node is None:
            return previous
        next_node = node.next
        node.next = previous
        return self._reverse(next_node, node)


class DoublyNode:
    """Node for the doubly linked list stack."""

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class DoublyLinkedListStack:
    """Stack stored in a doubly linked list; head is the top and tail is the bottom."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def push(self, value):
        node = DoublyNode(value, None, self.head)
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self.count += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self.count -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.head.value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.count

    def to_list(self):
        # The tail is the bottom, so walk backwards from it to read bottom to top.
        values = []
        node = self.tail
        while node is not None:
            values.append(node.value)
            node = node.prev
        return values

    def reverse(self):
        self._reverse(self.head)
        self.head, self.tail = self.tail, self.head

    def _reverse(self, node):
        # Swap each node's prev and next links; the old next is now in prev.
        if node is None:
            return
        node.prev, node.next = node.next, node.prev
        self._reverse(node.prev)


def format_values(values):
    return ", ".join(str(value) for value in values)


def test_stack(stack_class):
    """Push 1..10, reverse the stack, and check the order before and after."""
    print(stack_class.__name__)

    stack = stack_class()
    for value in range(1, 11):
        stack.push(value)
    print("Input: ", format_values(stack.to_list()))
    assert stack.to_list() == list(range(1, 11))

    stack.reverse()
    print("Output:", format_values(stack.to_list()))
    assert stack.to_list() == list(range(10, 0, -1))
    assert stack.size() == 10
    assert stack.peek() == 1

    # After reversing, popping should give the values back in the order they were pushed.
    popped = []
    while not stack.is_empty():
        popped.append(stack.pop())
    assert popped == list(range(1, 11))

    # Reversing an empty stack or a single item stack leaves it unchanged.
    empty_stack = stack_class()
    empty_stack.reverse()
    assert empty_stack.to_list() == []

    single_stack = stack_class()
    single_stack.push(42)
    single_stack.reverse()
    assert single_stack.to_list() == [42]
    assert single_stack.pop() == 42
    assert single_stack.is_empty()

    print("passed")
    print()


def main():
    test_stack(ArrayStack)
    test_stack(LinkedListStack)
    test_stack(DoublyLinkedListStack)


if __name__ == "__main__":
    main()
