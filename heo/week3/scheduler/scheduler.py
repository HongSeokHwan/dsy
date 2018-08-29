#from .. import priority_queue as pq

class Scheduler:

    def __init__(self):
        #self.priority_queue = pq.PriorityQueueHeap()
        print("Welcome to devfon's scheduler")
        self.status = None
        pass

    def prompt(self):
        command = input('>>> ')
        return command

    def parser(self):
        pass

    def add(self):
        pass

    def time_check(self):
        pass

    def list(self):
        pass

if __name__ == '__main__':
    sched = Scheduler()
    newline = sched.prompt()
    print(newline)
    # while(1):
    #     newline = sched.prompt()
    #     print(newline)
    #     if newline == 'exit\n':
    #         break