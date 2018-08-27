class Node(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

class Binary_search_tree(object):
    def __init__(self):
        self.root = None

    def search(self, node, key):
        if node == None or node.key == key:
            return node
        if node.key < key:
            return self.search(node.right, key)
        else:
            return self.search(node.left, key)

    def get_parent(self, node, key):
        previous_node = None
        current_node = node
        if node == self.root:
            return None
        while current_node != None and current_node.key != key:
            previous_node = current_node
            if current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return previous_node
                
    def insert(self, key):
        node = Node(key)
        current_node = self.root
        previous_node = None
        while current_node != None:
            previous_node = current_node
            if node.key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        if previous_node == None:
            self.root = node
        else:
            if node.key < previous_node.key:
                previous_node.left = node
            else:
                previous_node.right = node

    def get_minimum(self, node):
        while node.left != None:
            node = node.left
        return node

    def get_maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    def get_successor(self, node):
        pass        

    def delete(self, key):
        pass