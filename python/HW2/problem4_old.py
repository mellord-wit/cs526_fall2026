
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

    def SumOfMiddle3(self):
        curHead = self.head
        curTail = self.tail

        while curHead != curTail:
            curHead = curHead.next
            curTail = curTail.prev

        sum = curHead.value + curHead.next.value + curHead.prev.value
        return(sum)

def doIt(node):
    if node is None:
        return
    doIt(node.next)
    print(node.value)

my_list = dbl_linked_list(2);
my_list.add(3);
my_list.add(8);
my_list.add(14);
my_list.add(15);
my_list.add(25);
my_list.add(41);

my_list.add(67);
my_list.add(72);


print("Middle Sum: ", my_list.SumOfMiddle3())




