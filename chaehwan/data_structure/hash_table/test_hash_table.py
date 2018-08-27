import unittest
import hash_table
import timeit

class Test_hash_table(unittest.TestCase):
    def test_hash(self):
        # test whether the hash_result is between 0 and table_size
        sample_hash_table = hash_table.Hash_table(10)
        hash_result = sample_hash_table.hash(3)
        assert hash_result <= sample_hash_table.table_size

        sample_hash_table = hash_table.Hash_table(50)
        hash_result = sample_hash_table.hash(1000)
        assert hash_result <= sample_hash_table.table_size

        # test when the string input is given
        sample_hash_table = hash_table.Hash_table(100)
        hash_result = sample_hash_table.hash("hashing")
        assert hash_result <= sample_hash_table.table_size
        
    def test_insert(self):
        # setup
        sample_hash_table = hash_table.Hash_table(10)
        sample_hash_table.insert(3)
        hash_result = sample_hash_table.hash(3)
        slot = sample_hash_table.hash_table[hash_result]
        # test
        self.assertEqual(slot.head.key, 3)
        sample_hash_table.insert(5)
        self.assertEqual(slot.head.key, 5)

    def test_search(self):
        sample_hash_table = hash_table.Hash_table(10)
        sample_hash_table.insert(3)
        sample_hash_table.insert(5)
        sample_hash_table.insert(7)
        self.assertEqual(sample_hash_table.search(3).key, 3)
        self.assertEqual(sample_hash_table.search(5).key, 5)
        self.assertEqual(sample_hash_table.search(7).key, 7)

    def test_delete(self):
        sample_hash_table = hash_table.Hash_table(10)
        sample_hash_table.insert(3)
        hash_result = sample_hash_table.hash(3)
        slot = sample_hash_table.hash_table[hash_result]
        # before deletion
        self.assertEqual(slot.head.key, 3)
        # after deletion
        sample_hash_table.delete(3)
        self.assertEqual(slot.head, None)

    def test_resize(self):
        sample_hash_table = hash_table.Hash_table(2)
        # test the state before the resizing
        self.assertEqual(len(sample_hash_table.hash_table), 2)
        sample_hash_table.insert(3)
        self.assertEqual(sample_hash_table.hash_table[1].head.key, 3)
        sample_hash_table.insert(5)
        # test the state after the resizing
        self.assertEqual(len(sample_hash_table.hash_table), 4)
        self.assertEqual(sample_hash_table.hash_table[1].head.key, 3)

    def test_reshape_bucket(self):
        pass

    def test_performance(self):
        # test the performance of hashing
        # n : 1,000,000 m : 100,000
        sample_hash_table = hash_table.Hash_table(100000)
        for i in range(1000000):
            sample_hash_table.insert(i)
        start = timeit.default_timer()
        print(sample_hash_table.search(70000).key)
        end = timeit.default_timer()
        hashing_performance = end - start
        print("hashing_performance: ", hashing_performance)
        
        # test the performance of sequential search
        # n : 1,000,000 m : 100,000
        search_space = []
        for i in range(1000000):
            search_space.append(i)
        start = timeit.default_timer()
        for i in range(1000000):
            if search_space[i] == 70000:
                print(search_space[i])
                break
        end = timeit.default_timer()
        sequential_search_performance = end - start
        print("sequential_search_performance: ", sequential_search_performance)

if __name__ == '__main__':
    unittest.main()
