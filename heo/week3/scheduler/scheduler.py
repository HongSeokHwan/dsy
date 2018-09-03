import priority_queue as pq
import time
import threading
from datetime import datetime


class Scheduler:
    # Constructor
    def __init__(self):
        self.queue = pq.PriorityQueueHeap()

    # Get command from user
    def prompt(self):
        command = input()
        result = self.parser(command)

        if result == -1:
            print('Good-bye')
            return -1
        else:
            threading.Timer(1.0, self.prompt).start()

    # Parsing the command
    def parser(self, command):
        command_tokens = command.split(' ')

        if command_tokens[0] == 'add':
            self.add(command_tokens[1], command_tokens[2])
        elif command_tokens[0] == 'list':
            self.list()
        elif command_tokens[0] == 'delete':
            self.delete(command_tokens[1])
        elif command_tokens[0] == 'exit':
            return -1

    # Add the job to the scheduler
    def add(self, time, job_name):
        time = int(time.replace(':', ''))
        self.queue.insert(time, job_name)

    # Show pending jobs
    def list(self):
        if self.queue.size == 0:
            print('Job Queue is empty!')
        else:
            print('[Job Scheduler]\n')
            print('Rank\t     Job')
            new_queue = pq.PriorityQueueHeap()
            new_queue.heap = self.queue.heap[:]
            new_queue.size = self.queue.size
            rank = 1
            while(1):
                if new_queue.size == 0:
                    break
                showing_job = new_queue.delete()
                str_time = str(showing_job[0])
                str_time = str_time[:-2] + ':' + str_time[-2:]
                print(' ', rank, '\t', str_time, showing_job[1])
                rank += 1

    # Delete a specific job in Job queue
    def delete(self, name):
        self.queue.delete_arbitary(name)

    # Compare time between target time and now(thread)
    def time_check(self):
        now = datetime.now()
        str_min = now.minute

        if str_min < 10:
            str_min = '0' + str(str_min)

        str_now = str(now.hour)  + ':' + str(str_min)
            
        if self.queue.size >= 1:
            target_time = str(self.queue.heap[1][0])
            target_time = target_time[:-2] + ':' + target_time[-2:]

            if str_now == str(target_time):
                print(str_now + ' is ' + target_time + '\n')
                self.run(target_time)
            else:
                print(str_now + ' is not ' + target_time+ '\n')
        else:
            print('Job Queue is empty!')

        threading.Timer(15.0, self.time_check).start()

    # Run job at target time
    def run(self, target_time):
        job = self.queue.delete()
        time.sleep(3)
        print(target_time, job[1], 'complted!')


def main():
    sched = Scheduler()
    sched.prompt()
    sched.time_check()


if __name__ == '__main__':
    main()