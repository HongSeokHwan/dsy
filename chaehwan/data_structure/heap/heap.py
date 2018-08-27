import math

class Heap(object):
    def __init__(self, data=[-1]):
        self.heap = data
        self.heap_size = len(data) - 1

    def get_parent_index(self, node_index):
        return int(math.floor(node_index/2))

    def get_left_child_index(self, node_index):
        return node_index * 2

    def get_right_child_index(self, node_index):
        return node_index * 2 + 1
    
    def find_larger_node_index(self, node_a_index, node_b_index):
        if self.heap[node_a_index] > self.heap[node_b_index]:
            return node_a_index
        else:
            return node_b_index

    def swap(self, node_a_index, node_b_index):
        if node_a_index < 1 or node_b_index < 1:
            return
        else:
            temp = self.heap[node_a_index]
            self.heap[node_a_index] = self.heap[node_b_index]
            self.heap[node_b_index] = temp

    def max_heapify(self, node_index):
        left_child_index = self.get_left_child_index(node_index)
        right_child_index = self.get_right_child_index(node_index)
        if self.heap_size < left_child_index:
            return
        else:
            if self.heap_size < right_child_index:
                larger_child_index = left_child_index
            else:
                larger_child_index = self.find_larger_node_index(left_child_index, right_child_index)
            if self.heap[node_index] >= self.heap[larger_child_index]:
                return
            else:
                self.swap(node_index, larger_child_index)
                self.max_heapify(larger_child_index)
    
    def build_max_heap(self):
        starting_node_index = self.get_parent_index(self.heap_size)
        for i in range(starting_node_index, 0, -1):
            self.max_heapify(i)

    def insert(self, node):
        self.heap_size += 1
        self.heap.append(node)
        if self.heap_size == 1:
            return
        else:
            current_index = self.heap_size
            current_node = self.heap[current_index]
            parent_index = self.get_parent_index(current_index)
            parent_node = self.heap[parent_index]
            root_index = 1
            while current_node > parent_node and current_index != root_index:
                self.swap(current_index, parent_index)
                current_index = self.get_parent_index(current_index)

    def find_max(self):
        return self.heap[1]

    def extract_max(self):
        if self.heap_size < 1:
            return
        root = self.heap[1]
        self.swap(1, self.heap_size)
        self.heap.pop()
        self.heap_size -= 1
        self.max_heapify(1)
        return root
