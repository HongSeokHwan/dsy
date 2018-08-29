import priority_queue as pq

class Scheduler:
    # Constructor
    def __init__(self):
        self.queue = pq.PriorityQueueHeap()

    def prompt(self):
        command = 'add 10:20 job'
        self.parser(command)
        command = 'add 9:20 alarm'
        self.parser(command)
        command = 'add 7:20 method'
        self.parser(command)
        command = 'add 5:20 method'
        self.parser(command)
        command = 'list'
        self.parser(command)

    # Parsing the command
    def parser(self, command):
        command_tokens = command.split(' ')

        if command_tokens[0] == 'add':
            self.add(command_tokens[1], command_tokens[2])
        elif command_tokens[0] == 'list':
            self.list()

    # Add the job to the scheduler
    def add(self, time, job_name):
        time = int(time.replace(':', ''))
        self.queue.insert(time, job_name)

    # Show pending jobs
    def list(self):
        # print('[Job Scheduler]\n')
        print('Rank\t     Job')
        new_queue = pq.PriorityQueueHeap()
        new_queue.heap = self.queue.heap[:]
        new_queue.size = self.queue.size
        th = 1
        while(1):
            if new_queue.size == 0:
                break
            showing_job = new_queue.delete()
            str_time = str(showing_job[0])
            str_time = str_time[:-2] + ':' + str_time[-2:]
            print(' ', th, '\t', str_time, showing_job[1])
            th += 1

    def time_check(self):
        pass

    def run(self):
        pass

if __name__ == '__main__':
    sched = Scheduler()
    sched.prompt()
    # print(sched.queue.delete())
    # print(sched.queue.delete())
    # print(sched.queue.delete())
    # print(sched.queue.delete())
    # print(sched.queue.delete())
    # while(1):
    #     newline = sched.prompt()
    #     print(newline)
    #     if newline == 'exit\n':
    #         break