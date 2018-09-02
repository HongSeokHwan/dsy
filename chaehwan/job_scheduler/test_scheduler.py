import unittest
from datetime import datetime
from datetime import timedelta
import gc

import scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_search_event(self):
        scheduling_queue = scheduler.Scheduler()
        # Set up the test set between 2018.08.31 17:45 ~ 2018.08.31 18:05
        # with one minute interval
        sample_time = datetime.strptime("2018.08.31 17:45", "%Y.%m.%d %H:%M")
        for i in range(20):
            minute = timedelta(minutes=i) 
            scheduling_queue.register_event(sample_time+minute)
        scheduling_queue.show_event()

        # Verify search_event doesn't return None 
        # when the element is already in the queue 
        search_result = scheduling_queue.search_event("2018.08.31 17:45")
        assert search_result != None
        # Verify it returns correct number of result
        # when the end_time parameter is given
        search_result = scheduling_queue.search_event(end_time="2018.08.31 17:46")
        result_count = len(search_result)
        assert result_count == 2  
        # Verify it returns correct number of result
        # when the start_time and end_time parameters are given
        search_result = scheduling_queue.search_event(
                "2018.08.31 17:45",
                "2018.08.31 17:48")
        result_count = len(search_result)
        assert result_count == 4 
       
    def test_register_event(self):
        scheduling_queue = scheduler.Scheduler()
        # Set up the test set between 2018.08.31 17:45 ~ 2018.08.31 18:04
        # with one minute interval
        sample_time = datetime.strptime("2018.08.31 17:45", "%Y.%m.%d %H:%M")
        for i in range(20):
            minute = timedelta(minutes=i) 
            scheduling_queue.register_event(sample_time+minute)
        scheduling_queue.show_event()

        # Verify the result of register_event is in queue
        # after the register_event is executed
        top = scheduling_queue.search_upcoming_event()
        self.assertEqual(top.time, sample_time)
        # Verify the result of register_event keeps proper
        # position in the scheduling queue
        sample_time = datetime.strptime("2018.08.31 17:44", "%Y.%m.%d %H:%M")
        scheduling_queue.register_event("2018.08.31 17:44")
        top = scheduling_queue.search_upcoming_event()
        self.assertEqual(top.time, sample_time)

        sample_time = datetime.strptime("2018.08.31 18:05", "%Y.%m.%d %H:%M")
        scheduling_queue.register_event("2018.08.31 18:05")

    def test_update_event(self):
        scheduling_queue = scheduler.Scheduler()
        # Set up the test set between 2018.08.31 17:45 ~ 2018.08.31 18:04
        # with one minute interval
        sample_time = datetime.strptime("2018.08.31:17:45", "%Y.%m.%d:%H:%M")
        for i in range(20):
            minute = timedelta(minutes=i) 
            scheduling_queue.register_event(sample_time+minute)
        # Verify the result of updated new value is in queue
        # after the update_event is executed
        scheduling_queue.update_event("2018.08.31:17:45", "action", "shutdown")
        search_result = scheduling_queue.search_event("2018.08.31:17:45")
        assert search_result.action == "shutdown"
        # Verify the result of update_event keeps proper position in the queue
        # after the update_event is executed : root
        scheduling_queue.update_event("2018.08.31:17:50",
                                      "time", "2018.08.20:00:00")
        sample_time = datetime.strptime("2018.08.20:00:00", "%Y.%m.%d:%H:%M")
        top = scheduling_queue.search_upcoming_event()
        self.assertEqual(top.time, sample_time)

    def test_delete_event(self):
        scheduling_queue = scheduler.Scheduler()
        # Set up the test set between 2018.08.31 17:45 ~ 2018.08.31 18:04
        # with one minute interval
        sample_time = datetime.strptime("2018.08.31 17:45", "%Y.%m.%d %H:%M")
        for i in range(20):
            minute = timedelta(minutes=i) 
            scheduling_queue.register_event(sample_time+minute)
        scheduling_queue.show_event()

        # Verify the result of delete_event is not in queue
        # after the delete_event is executed
        sample_time = datetime.strptime("2018.08.31:17:45", "%Y.%m.%d:%H:%M")
        scheduling_queue.delete_event("2018.08.31:17:45")
        assert scheduling_queue.search_event("2018.08.31:17:45") is None
        # Verify the result of delete_event keeps proper position
        # after the delete_event is executed
        sample_time = datetime.strptime("2018.08.31:17:46", "%Y.%m.%d:%H:%M")
        scheduling_queue.register_event("2018.08.31:17:46")
        top = scheduling_queue.search_upcoming_event()
        self.assertEqual(top.time, sample_time)

    def tearDown(self):
        gc.collect()


if __name__ == "__main__":
    unittest.main()
