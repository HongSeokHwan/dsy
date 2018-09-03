import scheduler as sc
import unittest
import timeit

class TestScheduler(unittest.TestCase):

    def test_add(self):
        test_scheduler = sc.Scheduler()
        test_scheduler.add('17:00', 'alarm')
        self.assertEqual(test_scheduler.queue.heap, [0, [1700, 'alarm']])
        test_scheduler.add('14:00', 'crawling')
        self.assertEqual(test_scheduler.queue.heap, [0, [1400, 'crawling'],[1700, 'alarm']])
        test_scheduler.add('10:00', 'test')
        self.assertEqual(test_scheduler.queue.heap, [0, [1000, 'test'], [1700, 'alarm'],[1400, 'crawling']])

    def test_delete(self):
        test_scheduler = sc.Scheduler()
        test_scheduler.add('17:00', 'alarm')
        test_scheduler.add('14:00', 'crawling')
        test_scheduler.add('10:00', 'test')
        self.assertEqual(test_scheduler.queue.heap, [0, [1000, 'test'], [1700, 'alarm'],[1400, 'crawling']])
        test_scheduler.delete('test')
        self.assertEqual(test_scheduler.queue.heap, [0, [1700, 'alarm'],[1400, 'crawling']])
        test_scheduler.delete('crawling')
        self.assertEqual(test_scheduler.queue.heap, [0, [1700, 'alarm']])

    def test_run(self):
        test_scheduler = sc.Scheduler()
        test_scheduler.add('17:00', 'alarm')
        test_scheduler.add('14:00', 'crawling')
        test_scheduler.run('14:00')
        self.assertEqual(test_scheduler.queue.heap, [0, [1700, 'alarm']])
        test_scheduler.run('17:00')
        self.assertEqual(test_scheduler.queue.heap, [0])

if __name__ == '__main__':
    unittest.main()