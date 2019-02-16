import unittest

import priority_queue

def check_priority_order(sample_queue):
     last_node_index = sample_queue.queue_size-1
     for current_index in range(last_node_index, 0, -1):
         current_node = sample_queue.queue[current_index]
         parent_index = sample_queue.get_parent_index(current_index)
         parent_node = sample_queue.queue[parent_index]
         assert sample_queue.compare(parent_node, current_node)

def test_check_priority_order(self):
    pass

class TestPriorityQueue(unittest.TestCase):
    def test_swap(self):
        pq = priority_queue.PriorityQueue([3, 4])
        pq.swap(0,1)
        self.assertEqual(pq.queue, [4, 3])

    def test_compare(self):
        pq = priority_queue.PriorityQueue([3, 4, 2])
        self.assertEqual(pq.compare(pq.queue[0], pq.queue[1]), True)
        self.assertEqual(pq.compare(pq.queue[1], pq.queue[2]), False)
    
    def test_heapify(self):
        # Verify each node of the result keeps proper position
        # by checking heap property
        test_input = [
            [2],
            [5, 11, 8],
            [7, 5, 6, 11, 8, 9, 10],
            [8, 3, 1, 5, 6, 4, 2],
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.heapify(0)
            check_priority_order(pq)
    
    def test_build_heap(self):
        # Verify each node of the result keeps proper position
        # by checking heap property
        test_input = [
            [2],
            [3, 4],
            [3, 5, 4],
            [16, 14, 7, 2, 8, 1],
            [12, 11, 6, 8, 10, 2, 3, 1],
            [8, 3, 1, 5, 6, 4, 2]
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.build_heap()
            check_priority_order(pq)
        
    def test_insert(self):
        # Verify the value which is smaller than the root of min heap 
        # is new root after it is inserted
        test_input = [
            [2],
            [3, 4],
            [3, 5, 4],
            [16, 14, 7, 2, 8, 1],
            [12, 11, 6, 8, 10, 2, 3, 1],
            [8, 3, 1, 5, 6, 4, 2]
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.build_heap()
            new_min = min(test_input[i])-1
            pq.insert(new_min)
            self.assertEqual(pq.find_top(), new_min)
        # Verify the value which is larger than the root of min heap 
        # is the leaf node after it is inserted
        test_input = [
            [2],
            [3, 4],
            [3, 5, 4],
            [16, 14, 7, 2, 8, 1],
            [12, 11, 6, 8, 10, 2, 3, 1],
            [8, 3, 1, 5, 6, 4, 2]
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.build_heap()
            new_max = max(test_input[i])+1
            pq.insert(new_max)
            self.assertEqual(pq.queue[pq.queue_size-1], new_max)

    def test_find_top(self):
        # Verify the result of find_top method in min heap is 
        # same as the minimum of the array
        test_input = [
            [2],
            [3, 4],
            [3, 5, 4],
            [16, 14, 7, 2, 8, 1],
            [12, 11, 6, 8, 10, 2, 3, 1],
            [8, 3, 1, 5, 6, 4, 2]
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.build_heap()
            self.assertEqual(pq.find_top(), min(test_input[i]))
    
    def test_extract_top(self):
        # Verify the result of find_top method in min heap is 
        # same as the minimum of the array and it's properly removed
        test_input = [
            [2],
            [3, 4],
            [3, 5, 4],
            [16, 14, 7, 2, 8, 1],
            [12, 11, 6, 8, 10, 2, 3, 1],
            [8, 3, 1, 5, 6, 4, 2]
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.build_heap()
            min_value = min(test_input[i])
            self.assertEqual(pq.extract_top(), min_value)
            assert min_value not in pq.queue

    def test_delete(self):
        # Verify each node of the result keeps proper position
        # by checking heap property
        test_input = [
            [1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5],
            [4, 9, 8, 11, 12, 13, 15],
        ]
        for i in range(len(test_input)):
            pq = priority_queue.PriorityQueue(test_input[i])
            pq.delete(1)
            check_priority_order(pq)

    '''
    def test_update(self):
        pass
    '''
if __name__ == '__main__':
    unittest.main()

