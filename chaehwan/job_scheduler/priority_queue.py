import math

class PriorityQueue(object):
    def __init__(self, 
                 data=[], 
                 compare_function = lambda a, b: a if (a<b) else b):
        self.queue = data
        self.queue_size = len(data)
        self.compare_function = compare_function

    def get_parent_index(self, node_index):
        return math.floor((node_index-1)/2) 

    def get_left_child_index(self, node_index):
        return 2 * node_index + 1

    def get_right_child_index(self, node_index):
        return 2 * node_index + 2

    def swap(self, node_a_index, node_b_index):
        temp = self.queue[node_a_index]
        self.queue[node_a_index] = self.queue[node_b_index]
        self.queue[node_b_index] = temp

    def compare(self, node_a, node_b):
        if self.compare_function(node_a, node_b) == node_a:
            return True
        else:
            return False

    def heapify(self, node_index):
        left_child_index = self.get_left_child_index(node_index)
        right_child_index = self.get_right_child_index(node_index)
        last_node_index = self.queue_size-1
        if last_node_index < left_child_index:
            return None
        else:
            if last_node_index < right_child_index:
                selected_child_index = left_child_index
            else:
                if self.compare(
                        self.queue[left_child_index], 
                        self.queue[right_child_index]):
                    selected_child_index = left_child_index
                else:
                    selected_child_index = right_child_index
            if (self.compare(
                    self.queue[node_index], 
                    self.queue[selected_child_index]) is False):
                self.swap(node_index, selected_child_index)
                self.heapify(selected_child_index)

    def build_heap(self):
        last_node_index = self.queue_size-1
        start_index = self.get_parent_index(last_node_index)
        for i in range(start_index, -1, -1):
            self.heapify(i)
    
    def find_position(self, current_index):
        current_node = self.queue[current_index]
        parent_index = self.get_parent_index(current_index)
        parent_node = self.queue[parent_index]
        root_index = 0
        while (self.compare(current_node, parent_node) and
               current_index != root_index):
            self.swap(current_index, 
                      self.get_parent_index(current_index))
            current_index = self.get_parent_index(current_index)

    def insert(self, item):
        self.queue_size += 1
        self.queue.append(item)
        if self.queue_size == 1:
            return None
        else:
            last_node_index = self.queue_size-1
            self.find_position(last_node_index)    

    def find_top(self):
        if self.queue_size == 0:
            return None
        return self.queue[0]

    def extract_top(self):
        if self.queue_size == 0:
            return None
        root = self.queue[0]
        last_node_index = self.queue_size-1
        self.swap(0, last_node_index)
        self.queue.pop()
        self.queue_size -= 1
        self.heapify(0)
        return root

    def delete(self, item_index):
        if self.queue_size == 0:
            return None
        last_node_index = self.queue_size-1
        self.swap(item_index, last_node_index)
        self.queue.pop()
        self.queue_size -= 1
        self.heapify(item_index)

    def empty(self):
        if self.queue_size == 0:
            return True
        else:
            return False
