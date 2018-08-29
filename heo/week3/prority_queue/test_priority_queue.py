import priority_queue_heap as pqh
import priority_queue_array as pqa
import unittest
import timeit

class TestPriorityQueue(unittest.TestCase):

    def test_insert(self):
        test_queue = pqh.PriorityQueueHeap()
        test_queue.insert(3)
        self.assertEqual(test_queue.heap, [0,3])
        test_queue.insert(2)
        self.assertEqual(test_queue.heap, [0, 2, 3])
        test_queue.insert(1)
        self.assertEqual(test_queue.heap, [0, 1, 3, 2])

        test_queue_array = pqa.PriorityQueueArray()
        test_queue_array.insert(3)
        test_queue_array.insert(1)
        self.assertEqual(test_queue_array.array, [1,3])
        

    def test_delete(self):
        test_queue = pqh.PriorityQueueHeap()
        test_queue.insert(3)
        test_queue.insert(2)
        test_queue.insert(1)
        test_queue.delete()
        self.assertEqual(test_queue.heap, [0, 2, 3])

        test_queue_array = pqa.PriorityQueueArray()
        test_queue_array.insert(3)
        test_queue_array.insert(1)
        test_queue_array.insert(5)
        test_queue_array.delete()
        self.assertEqual(test_queue_array.array, [3,5])

    def test_build_heap(self):
        test_queue = pqh.PriorityQueueHeap()
        test_queue.build_heap([9, 3, 2, 1, 7])
        self.assertEqual(test_queue.heap, [0, 1, 3, 2, 9, 7])

    def test_performance(self):
        # insert performance
        test_queue_heap = pqh.PriorityQueueHeap()
        start_time = timeit.default_timer()
        for i in range(10000, 0, -1):
            test_queue_heap.insert(i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[insert]Heap based Priority Queue', total_time)

        test_queue_array = pqa.PriorityQueueArray()
        start_time = timeit.default_timer()
        for i in range(10000, 0, -1):
            test_queue_array.insert(i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[insert]Array based Priority Queue', total_time)

        # delete performance
        start_time = timeit.default_timer()
        for i in range(10000, 0, -1):
            test_queue_heap.delete()
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('\n[delete]Heap based Priority Queue', total_time)

        start_time = timeit.default_timer()
        for i in range(10000, 0, -1):
            test_queue_array.delete()
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[delete]Array based Priority Queue', total_time)


if __name__ == '__main__':
    unittest.main()