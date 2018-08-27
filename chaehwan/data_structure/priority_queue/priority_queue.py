import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import linked_list.linked_list as linked_list
import heap.heap as heap

class Priority_queue(heap.Heap):
    def __init__(self, data=[-1]):
        super().__init__(data)

    def increase_key(self, element, key):
        if key < self.heap[element]:
            return
        else:
            self.heap[element] = key
            current_index = element
            current_node = self.heap[current_index]
            parent_index = self.get_parent_index(current_index)
            parent_node = self.heap[parent_index]
            root_index = 1
            while current_index != root_index and parent_node < current_node:
                swap(current_index, parent_index)
                current_index = self.get_parent_index(current_index)