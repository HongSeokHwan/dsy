class Node(object):
    def __init__(self, prev, key, next):
        self.prev = prev
        self.key = key
        self.next = next

class Linked_list(object):
    def __init__(self):
        self.head = None
    
    def insert(self, key):
        node = Node(None, key, None)
        node.next = self.head
        if self.head != None:
            self.head.prev = node
        self.head = node
        node.prev = None

    def search(self, key):
        current_node = self.head
        while current_node != None and current_node.key != key:
            current_node = current_node.next
        return current_node

    def delete(self, key):
        node = self.search(key)
        if node.prev != None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next != None:
            node.next.prev = node.prev

    def traverse(self):
        visited = []
        current_node = self.head
        while current_node != None:
            visited.append(current_node.key)
            current_node = current_node.next
        return visited