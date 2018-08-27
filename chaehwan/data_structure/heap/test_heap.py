import unittest
import heap

class Test_heap(unittest.TestCase):
	def test_swap(self):
		binary_heap = heap.Heap([-1, 3, 4])
		binary_heap.swap(1, 2)
		self.assertEqual(binary_heap.heap, [-1, 4, 3])

	def test_max_heapify(self):
		# case : when the node has no child node
		binary_heap = heap.Heap([-1, 2])
		binary_heap.max_heapify(1)
		self.assertEqual(binary_heap.heap, [-1, 2])
		# case : when the node has at least one child node
		binary_heap = heap.Heap([-1, 1, 14, 16, 2, 8, 7])
		binary_heap.max_heapify(1)
		self.assertEqual(binary_heap.heap, [-1, 16, 14, 7, 2, 8, 1])
	
	def test_build_max_heap(self):
		test_set = [
			[-1, 1, 14, 16, 2, 8, 7],
			[-1, 8, 12, 6, 11, 10, 2, 3, 1],
			[-1, 2, 3],
			[-1, 5],
			[-1, 4, 7, 8, 9, 10]
		]
		answer_set = [
			[-1, 16, 14, 7, 2, 8, 1],
			[-1, 12, 11, 6, 8, 10, 2, 3, 1],
			[-1, 3, 2],
			[-1, 5],
			[-1, 10, 9, 8, 4, 7]
		]
		for i in range(len(test_set)):
			binary_heap = heap.Heap(test_set[i])
			binary_heap.build_max_heap()
			self.assertEqual(test_set[i], answer_set[i])

	def test_insert(self):
		binary_heap = heap.Heap()
		binary_heap.insert(3)
		self.assertEqual(binary_heap.heap, [-1, 3])
		binary_heap = heap.Heap([-1, 20, 10, 16, 8, 7, 13, 14, 2, 5, 6])
		binary_heap.insert(15)
		self.assertEqual(binary_heap.heap, [-1, 20, 15, 16, 8, 10, 13, 14, 2, 5, 6, 7])

	def test_extract_max(self):
		# test whether the return value of extract_max is the max value in the heap
		binary_heap = heap.Heap([-1, 20, 10, 16, 8, 7, 13, 14, 2, 5, 6])
		max_value = max(binary_heap.heap)
		self.assertEqual(binary_heap.extract_max(), max_value)
		# test the heap is organized properly after the binary heap removed the root
		self.assertEqual(binary_heap.heap, [-1, 16, 10, 14, 8, 7, 13, 6, 2, 5])
		

if __name__ == '__main__':
    unittest.main()
