import hash_table as ht
import unittest
import timeit

class TestHashTable(unittest.TestCase):

    def test_put(self):
        test_table = ht.HashTable(13)
        # Normal put
        test_table.put(10,20)
        self.assertEqual(test_table.table, [[],[],[],[],[],[],[],[],[],[],[(10,20)],[],[]])
        # Replace put
        test_table.put(10, 30)
        self.assertEqual(test_table.table, [[],[],[],[],[],[],[],[],[],[],[(10,30)],[],[]])
        # Chaining put
        test_table.put(23, 20)
        self.assertEqual(test_table.table, [[],[],[],[],[],[],[],[],[],[],[(10,30), (23,20)],[],[]])

    def test_search(self):
        test_table = ht.HashTable(13)
        test_table.put(10, 30)
        test_table.put(1, 20)
        # Normal search
        self.assertEqual(test_table.search(10), 30)
        # Non-exist key search
        self.assertEqual(test_table.search(2), None)

    def test_delete(self):
        test_table = ht.HashTable(13)
        test_table.put(10,20)
        self.assertEqual(test_table.table, [[],[],[],[],[],[],[],[],[],[],[(10,20)],[],[]])
        test_table.put(3, 7)
        self.assertEqual(test_table.table, [[],[],[],[(3,7)],[],[],[],[],[],[],[(10,20)],[],[]])
        # Normal delete
        test_table.delete(10)
        self.assertEqual(test_table.table, [[],[],[],[(3,7)],[],[],[],[],[],[],[],[],[]])
        # Non-exist key delete
        test_table.delete(2)
        self.assertEqual(test_table.table, [[],[],[],[(3,7)],[],[],[],[],[],[],[],[],[]])

    def test_performance(self):
        # linear put performance
        print('Linear Performance Test')
        test_table = ht.HashTable(10000)
        start_time = timeit.default_timer()
        for i in range(10000):
            test_table.put(i, i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[put]Performance of HashTable', total_time)

        test_dict = {}
        start_time = timeit.default_timer()
        for i in range(10000):
            test_dict[i] = i
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[put]Performance of Dictionary', total_time)

        # linear search performance
        start_time = timeit.default_timer()
        for i in range(10000):
            test_table.search(i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('\n[search]Performance of HashTable', total_time)

        start_time = timeit.default_timer()
        for i in range(10000):
            result = test_dict[i]
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[search]Performance of Dictionary', total_time)

        print('\nChaining Performance Test')
        # chaining put performance
        test_table = ht.HashTable(3)
        const = 3
        start_time = timeit.default_timer()
        for i in range(10000):
            a = const * i
            test_table.put(a, i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[put]Performance of HashTable', total_time)

        test_dict = {1:[]}
        dict_idx = 1
        start_time = timeit.default_timer()
        for i in range(10000):
            dict_idx *= 10
            dict_idx /= 10
            test_dict[dict_idx].append(i)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[put]Performance of Dictionary', total_time)

        # chaining search performance
        const = 3
        start_time = timeit.default_timer()
        for i in range(10000):
            a = const * i
            test_table.search(a)
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('\n[search]Performance of HashTable', total_time)

        dict_idx = 1
        start_time = timeit.default_timer()
        for i in range(10000):
            dict_idx *= 10
            dict_idx /= 10
            result = test_dict[dict_idx][i]
        end_time = timeit.default_timer()
        total_time = end_time - start_time
        print('[search]Performance of Dictionary', total_time)

if __name__ == '__main__':
    unittest.main()