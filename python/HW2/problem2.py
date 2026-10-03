class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __str__(self):
        if self.length == 0:
            return "(empty)"
        return " -> ".join(str(value) for value in self)

    def _check_index(self, index, upper):
        if index < 0 or index > upper:
            raise IndexError("index " + str(index) + " out of range")

    def _node_at(self, index):
        self._check_index(index, self.length - 1)
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

    # ---------- Create ----------

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.length = self.length + 1

    def prepend(self, value):
        new_node = Node(value, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.length = self.length + 1

    def insert(self, index, value):
        self._check_index(index, self.length)
        if index == 0:
            self.prepend(value)
        elif index == self.length:
            self.append(value)
        else:
            prev = self._node_at(index - 1)
            prev.next = Node(value, prev.next)
            self.length = self.length + 1

    # ---------- Read ----------

    def get(self, index):
        return self._node_at(index).value

    def find(self, value):
        for index, cur_value in enumerate(self):
            if cur_value == value:
                return index
        return -1

    # ---------- Update ----------

    def update(self, index, value):
        self._node_at(index).value = value

    # ---------- Delete ----------

    def delete(self, value):
        prev = None
        cur = self.head
        while cur is not None:
            if cur.value == value:
                self._unlink(prev, cur)
                return True
            prev = cur
            cur = cur.next
        return False

    def delete_at(self, index):
        self._check_index(index, self.length - 1)
        prev = None if index == 0 else self._node_at(index - 1)
        cur = self.head if prev is None else prev.next
        self._unlink(prev, cur)
        return cur.value

    def _unlink(self, prev, cur):
        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next
        if cur is self.tail:
            self.tail = prev
        self.length = self.length - 1

    # ---------- Print ----------

    def print_list(self):
        print(self)


if __name__ == "__main__":
    my_list = SinglyLinkedList()
    my_list.append(12)
    my_list.append(3)
    my_list.append(5)
    my_list.append(2)
    my_list.print_list()                    # 12 -> 3 -> 5 -> 2

    my_list.prepend(1)
    my_list.insert(2, 99)
    my_list.print_list()                    # 1 -> 12 -> 99 -> 3 -> 5 -> 2

    print("get(2):", my_list.get(2))        # 99
    print("find(5):", my_list.find(5))      # 4
    print("find(42):", my_list.find(42))    # -1

    my_list.update(2, 100)
    my_list.print_list()                    # 1 -> 12 -> 100 -> 3 -> 5 -> 2

    my_list.delete(100)
    my_list.delete_at(0)
    my_list.delete(2)
    my_list.print_list()                    # 12 -> 3 -> 5
    print("length:", len(my_list))          # 3
