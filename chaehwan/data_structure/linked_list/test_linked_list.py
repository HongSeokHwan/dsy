import unittest
import linked_list

class Test_linked_list(unittest.TestCase):
    def test_insert(self):
        sample_linked_list = linked_list.Linked_list()
        sample_linked_list.insert(3)
        self.assertEqual(sample_linked_list.head.key, 3)
        sample_linked_list.insert(5)
        self.assertEqual(sample_linked_list.head.key, 5)
        self.assertEqual(sample_linked_list.head.next.key, 3)
        sample_linked_list.insert(7)
        self.assertEqual(sample_linked_list.head.key, 7)
        self.assertEqual(sample_linked_list.head.next.key, 5)
        self.assertEqual(sample_linked_list.head.next.next.key, 3)

    def test_search(self):
        sample_linked_list = linked_list.Linked_list()
        for i in range(10):
            sample_linked_list.insert(i)
        self.assertEqual(sample_linked_list.head.key, 9)
        self.assertEqual(sample_linked_list.head.next.next.key, 7)
        self.assertEqual(sample_linked_list.head.next.next.next.next.key, 5)

    def test_delete(self):
        sample_linked_list = linked_list.Linked_list()
        for i in range(10):
            sample_linked_list.insert(i)
        sample_linked_list.delete(9)
        self.assertEqual(sample_linked_list.head.key, 8)
        sample_linked_list.delete(5)
        self.assertEqual(sample_linked_list.head.next.next.next.next.key, 3)

    def test_traverse(self):
        sample_linked_list = linked_list.Linked_list()
        for i in range(10):
            sample_linked_list.insert(i)
        self.assertEqual(sample_linked_list.traverse(), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

if __name__ == '__main__':
    unittest.main()
