
class node:
    def __init__(self, next=None, prev=None, value=None):
        self.next = next
        self.prev = prev
        self.value = value

class dbl_linked_list:
    def __init__(self, value):
        new_node = node(None, None, value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def add(self, value):
        new_node = node(None, self.tail, value)
        self.tail.next = new_node
        self.tail = new_node
        self.length = self.length + 1

def doIt(node):
    if node is None:
        return
    doIt(node.next)
    print(node.value)

my_list = dbl_linked_list(12);
my_list.add(3);
my_list.add(5);
my_list.add(2);

doIt(my_list.head)





