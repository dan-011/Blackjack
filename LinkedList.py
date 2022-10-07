class Node:
    def __init__(self, _item, _next = None):
        self._item = _item
        self._next = _next
    
    def __str__(self):
        if self._next is not None:
            return "Node(item = {}, next._item = {})".format(self._item, self._next._item) #doesn't work for tail node (no next for teail node)
        return "Node(item = {}, next = None)".format(self._item)

class ModifiedLinkedList:
    def __init__(self):
        self.head = None
        self.len = 0

    def add_first(self, item):
        node = Node(item, self.head)
        self.head = node
        self.len += 1
    
    

    def remove_first(self):
        if self.len == 0:
            raise RuntimeError
        else:
            item = self.head._item
            self.head = self.head._next
            self.len -= 1
            return item

    def remove_last(self):
        if self.len == 0:
            raise RuntimeError
        elif self.len == 1:
            return self.remove_first()
        else:
            current_node = self.head
            while current_node._next._next is not None:
                current_node = current_node._next
            item = current_node._next._item
            current_node._next = None
            self.len -= 1
            return item

    def __len__(self):
        return self.len

if __name__ == '__main__':
    ##########Test Node##########
    n1 = Node(1)
    assert(n1._item==1)
    n2 = Node(2, _next=n1)
    assert(n2._item == 2)
    assert(n2._next == n1)

    ##########Test LinkedList##########
    ll1 = LinkedList()
    assert(ll1.head == None)

    #add_first()
    for i in range(10):
        ll1.add_first(i*3)
        assert(ll1.head._item == i*3)

    #remove_first()
    for i in range(9,-1,-1):
        print(str(ll1.head))
        assert(ll1.remove_first() == i*3)
    