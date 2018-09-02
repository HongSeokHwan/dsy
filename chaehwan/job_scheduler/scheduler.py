import os
import sys
import threading
import time
import cmd
from datetime import datetime
from datetime import timedelta

import priority_queue

class Event(object):
    def __init__(self, time=datetime.now(), 
                       priority="mid", action="python", 
                       parameter=None, flag=None):
        self.time = time
        self.priority = priority
        self.action = action
        self.parameter = parameter
        self.flag = flag

    def __str__(self):
        info = ''
        for attribute in self.__dict__:
            if self.__dict__[attribute] is not None:
                info += str(self.__dict__[attribute]) + ' '
        return info

    def __lt__(self, other):
        if self.time < other.time:
            return True 
        elif self.time == other.time:
            if self.priority > self.priority:
                return True
        else:
            return False

class Scheduler(object):
    def __init__(self):
        self.scheduling_queue = priority_queue.PriorityQueue()
        self.priority_level = {"high": 3, "mid": 2, "low" : 1}
        self.flag_set = ["--once", "--daily", "--weekly", "--monthly"]

    def convert_into_time(self, time):
        try:
            if isinstance(time, datetime) is False:
                time = datetime.strptime(time, "%Y.%m.%d:%H:%M")
        except:
            print("Please type again. It doesn't match time format")
        return time

    def set_priority(self, priority):
        if priority in self.priority_level:
            priority = self.priority_level[priority]
        else:
            priority = self.priority_level["mid"]
        return priority

    def set_flag(self, flag):
        if flag not in self.flag_set:
            flag = "--once"
        return flag

    def register_event(self, time=datetime.now(),
                             priority="mid", action="python", 
                             parameter=None, flag="--once"):
        time = self.convert_into_time(time)
        priority = self.set_priority(priority)
        flag = self.set_flag(flag)
        event = Event(time, priority, action, parameter, flag)
        self.scheduling_queue.insert(event)

    def search_event(self, start_time=None, end_time=None):
        if end_time is None:
            start_time = self.convert_into_time(start_time)
            for event in self.scheduling_queue.queue:
                if event.time == start_time:
                    return event
        elif start_time is None:
            end_time = self.convert_into_time(end_time)
            matched_event = []
            for event in self.scheduling_queue.queue:
                if event.time <= end_time:
                    matched_event.append(event)
            return matched_event
        else:
            matched_event = []
            start_time = self.convert_into_time(start_time)
            end_time = self.convert_into_time(end_time)
            for event in self.scheduling_queue.queue:
                if event.time >= start_time and event.time <= end_time:
                    matched_event.append(event)
            return matched_event 

    def search_event_index(self, time):
        time = self.convert_into_time(time)
        event_list = self.scheduling_queue.queue
        for i in range(len(event_list)):
            if event_list[i].time == time:
                return i
        return None

    def search_upcoming_event(self):
        return self.scheduling_queue.find_top()
   
    def extract_upcoming_event(self):
        return self.scheduling_queue.extract_top()

    def find_key(self, event, key):
        for attribute in event.__dict__:
            if attribute == key:
                return attribute
        return None

    def preprocess(self, key, value):
        if key == "time":
            value = self.convert_into_time(value)
        if key == "priority":
            value = self.set_priority(value)
        if key == "flag":
            value = self.set_flag(value)
        return value

    def update_event(self, time, key, value):
        time = self.convert_into_time(time)
        event_list = self.scheduling_queue.queue
        event_index = self.search_event_index(time)
        if event_index is None:
            return None
        event = event_list[event_index]
        old_key = self.find_key(event, key)
        value = self.preprocess(key, value)
        if old_key is not None:
            old_value = event.__dict__[old_key]
            event.__dict__[key] = value
            if old_value > value:
                self.scheduling_queue.find_position(event_index)
            elif old_value < value:
                self.scheduling_queue.heapify(event_index)
            else:
                return None

    def delete_event(self, time):
        time = self.convert_into_time(time)
        if self.scheduling_queue.empty():
            return None
        else:
            event_index = self.search_event_index(time)
            if event_index is not None:
                self.scheduling_queue.delete(event_index)

    def show_event(self, time=None):
        if time is not None:
            event = self.search_event(time)
            if event is not None:
                print(event)
        else:
            for event in self.scheduling_queue.queue:
                print(event)

    def check_time(self, event):
        if event.time > datetime.now():
            return True
        return False

    def run(self):
        upcoming_event = self.search_upcoming_event()
        if upcoming_event is not None:
            if self.check_time(upcoming_event):
                if event.parameter is None:
                    action_command = event.action
                else:
                    action_command = event.action + ' ' + event.parameter
                os.system(action_command)
                self.extract_upcoming_event()
   

class CommandPrompt(cmd.Cmd):
    def __init__(self):
        self.intro = "도움말을 보시려면 help <command>를 입력하세요"
        self.prompt = "(Scheduler)"
        super().__init__()
        self.app = Scheduler()

    def do_register(self, args):
        self.app.register_event(*self.parse(args))

    def help_register(self):
        print("다음의 형식으로 입력하세요.")
        print("register <time> <priority> <action> <parameter> <flag>")
        print("ex)", end="")
        print("""register 2018.09.01:17:45 python test_scheduler.py 
            --high --daily""")
    
    def do_update(self, args):
        self.app.update_event(*self.parse(args))

    def help_update(self):
        print("다음의 형식으로 입력하세요.")
        print("update <time> <key> <value>")
        print("ex) update 2018.08.31:17:45 parameter test_scheduler.py")

    def do_cancel(self, args):
        self.app.delete_event(*self.parse(args))

    def help_cancel(self):
        print("다음의 형식으로 입력하세요.")
        print("cancel <time>")
        print("ex) cancel 2018.08.31:17:45")
    
    def do_show(self, args):
        self.app.show_event(*self.parse(args))

    def help_show(self):
        print("이 명령어는 해당 시간의 일정을 출력합니다.")
        print("다음의 형식으로 입력하세요.")
        print("show <time> ex) show 2018.08.31:17:45")
        print("시간을 입력하지 않으면 등록된 모든 일정을 출력합니다.")
        print("show")
        
    def do_exit(self):
        pass

    def process_command(self):
        self.lock.acquire()
        self.cmdloop()
        self.lock.release()

    def execute(self):
        self.lock.acquire()
        self.app.run()
        self.lock.release()

    def parse(self, arguments):
        return tuple(arguments.split())


if __name__=="__main__":
    command_prompt = CommandPrompt()
    prompt_execution = threading.Thread(
                target=command_prompt.process_command)
    time_check_execution = threading.Thread(
                target=command_prompt.execute)
    prompt_execution.start()
    time_check_execution.start()

    
