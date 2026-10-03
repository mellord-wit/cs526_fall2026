class Node:
    def __init__(self, value=None, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class SortedDoublyLinkedList:
    """A doubly linked list that always keeps its values in ascending order.

    The list is walked with recursive helpers. Each helper handles one node and
    calls itself on node.next, so a very long list (about 1000 nodes or more)
    will hit Python's recursion limit.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def __str__(self):
        if self.head is None:
            return "(empty)"
        return self._to_string(self.head)

    # ---------- Recursive helpers ----------

    def _to_string(self, node):
        if node.next is None:
            return str(node.value)
        return str(node.value) + " <-> " + self._to_string(node.next)

    def _first_greater(self, node, value):
        # First node whose value is greater than value, or None if there is none.
        if node is None or node.value > value:
            return node
        return self._first_greater(node.next, value)

    def _find(self, node, value):
        # First node holding value. The list is sorted, so stop as soon as the
        # values pass value.
        if node is None or node.value > value:
            return None
        if node.value == value:
            return node
        return self._find(node.next, value)

    def _node_at(self, node, index):
        if index == 0:
            return node
        return self._node_at(node.next, index - 1)

    def _total(self, node):
        if node is None:
            return 0
        return node.value + self._total(node.next)

    def _count(self, node, value):
        # Sorted, so once the values pass value there are no more matches.
        if node is None or node.value > value:
            return 0
        match = 1 if node.value == value else 0
        return match + self._count(node.next, value)

    # ---------- CRUD ----------

    def add(self, value):
        new_node = Node(value)
        # Insert before the first larger value, so equal values stay in the
        # order they were added.
        after = self._first_greater(self.head, value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        elif after is None:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        elif after is self.head:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            new_node.prev = after.prev
            new_node.next = after
            after.prev.next = new_node
            after.prev = new_node

        self.length = self.length + 1

    def delete(self, value):
        node = self._find(self.head, value)
        if node is None:
            return False

        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        self.length = self.length - 1
        return True

    def exists(self, value):
        return self._find(self.head, value) is not None

    def print_list(self):
        print(self)

    # ---------- Additional methods ----------

    def total(self):
        return self._total(self.head)

    def sum_middle_three(self):
        if self.length < 3:
            raise ValueError("sum_middle_three needs at least 3 nodes")
        mid = self.length // 2
        # odd: mid-1, mid, mid+1    even: mid-2, mid-1, mid
        first = mid - 1 if self.length % 2 == 1 else mid - 2
        node = self._node_at(self.head, first)
        return node.value + node.next.value + node.next.next.value

    def median(self):
        if self.length == 0:
            raise ValueError("median of an empty list")
        mid = self.length // 2
        if self.length % 2 == 1:
            return self._node_at(self.head, mid).value
        node = self._node_at(self.head, mid - 1)
        return (node.value + node.next.value) / 2

    def count(self, value):
        return self._count(self.head, value)


if __name__ == "__main__":
    my_list = SortedDoublyLinkedList()

    print("add 10, 4, 29, 8, 2, 15, 41")
    for value in [10, 4, 29, 8, 2, 15, 41]:
        my_list.add(value)
    my_list.print_list()                                    # 2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41
    print("total: ", my_list.total())                       # 109
    print("sum_middle_three: ", my_list.sum_middle_three()) # 33
    print("median: ", my_list.median())                     # 10

    print("\ndelete 41")
    my_list.delete(41)
    my_list.print_list()                                    # 2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29
    print("total: ", my_list.total())                       # 68
    print("sum_middle_three: ", my_list.sum_middle_three()) # 22
    print("median: ", my_list.median())                     # 9.0

    print("\nadd 8")
    my_list.add(8)
    my_list.print_list()                                    # 2 <-> 4 <-> 8 <-> 8 <-> 10 <-> 15 <-> 29
    print("count(8): ", my_list.count(8))                   # 2
    print("count(5): ", my_list.count(5))                   # 0
    print("exists(15): ", my_list.exists(15))               # True
    print("exists(5): ", my_list.exists(5))                 # False
    print("delete(5): ", my_list.delete(5))                 # False
