import unittest
import priority_queue
import priority_queue_by_array
import timeit

class Test_priority_queue(unittest.TestCase):
    def test_insert(self):
        # heap based priority queue test
        heap_based_priority_queue = priority_queue.Priority_queue()
        heap_based_priority_queue.insert(3)
        self.assertEqual(heap_based_priority_queue.heap, [-1, 3])
        heap_based_priority_queue.insert(5)
        self.assertEqual(heap_based_priority_queue.heap, [-1, 5, 3])
        # array based priority queue test
        array_based_priority_queue = priority_queue_by_array.Priority_queue()
        array_based_priority_queue.insert(3)
        self.assertEqual(array_based_priority_queue.queue, [3])
        array_based_priority_queue.insert(5)
        self.assertEqual(array_based_priority_queue.queue, [3, 5])

    def test_find_max(self):
        # heap based priority queue test
        heap_based_priority_queue = priority_queue.Priority_queue([-1, 10, 8, 7, 3])
        self.assertEqual(heap_based_priority_queue.find_max(), 10)

        # array based priority queue test
        array_based_priority_queue = priority_queue_by_array.Priority_queue([-1, 10, 8, 7, 3])
        self.assertEqual(array_based_priority_queue.find_max(), 10)


    def test_extract_max(self):
        # heap based priority queue test
        heap_based_priority_queue = priority_queue.Priority_queue([-1, 10, 8, 7, 3])
        self.assertEqual(heap_based_priority_queue.extract_max(), 10)
        self.assertEqual(heap_based_priority_queue.heap, [-1, 8, 3, 7])

        # array based priority queue test
        array_based_priority_queue = priority_queue_by_array.Priority_queue([-1, 10, 8, 7, 3])
        self.assertEqual(array_based_priority_queue.extract_max(), 10)
        self.assertEqual(array_based_priority_queue.queue, [-1, 8, 7, 3])

    def increase_key(self):
        heap_based_priority_queue = priority_queue.Priority_queue([-1, 3, 7, 5])
        heap_based_priority_queue.increase_key(3, 8)
        self.assertEqual(heap_based_priority_queue.heap, [-1, 8, 3, 7])
        heap_based_priority_queue.insert(10)
        self.assertEqual(heap_based_priority_queue.heap, [-1, 10, 8, 7, 3])

    def test_performance(self):
        # test the performance of priority_queue
        # n : 1,000,000
        heap_based_priority_queue = priority_queue.Priority_queue()
        for i in range(1000000):
            heap_based_priority_queue.insert(i)
        start = timeit.default_timer()
        print(heap_based_priority_queue.extract_max())
        end = timeit.default_timer()
        priority_queue_performance = end - start
        print("priority_queue_performance: ", priority_queue_performance)
        
        # test the performance of sequential search
        # n : 1,000,000
        array_based_priority_queue = priority_queue_by_array.Priority_queue()
        for i in range(1000000):
            array_based_priority_queue.insert(i)
        start = timeit.default_timer()
        print(array_based_priority_queue.extract_max())
        end = timeit.default_timer()
        sequential_search_performance = end - start
        print("sequential_search_performance: ", sequential_search_performance)

if __name__ == '__main__':
    unittest.main()
