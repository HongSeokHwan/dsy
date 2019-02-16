def dummy_action():
    print('''
    asd
    fasd
    f
    wqe
    fqwe
    f
    asd
    fw
    qef
    qwe
    fa
    sdf
    asd
    fqw
    ef
    qwef
    qwe
    fqw
    ef
    ''')


class IEvent:
    def __init__(self):
        pass

    def run(self):
        assert False


class BackupPolicy(IEvent):
    def __init__(self):
        pass

    def run(self):
        dummy_action()


class ReportPolicy(IEvent):
    def __init__(self):
        pass

    def run(self):
        dummy_action()


class ReportPolicy2(IEvent):
    def __init__(self):
        pass

    def run(self):
        dummy_action()


class ISchedulePolicy:
    def __init__(self):
        pass

    def has_target(self):
        assert False

    def pop(self):
        assert False

    def add(self):
        assert False


class RoundRobinSchedulePolicy(ISchedulePolicy):
    def __init__(self):
        pass

    def has_target(self):
        # TODO
        pass

    def pop(self):
        # TODO
        pass

    def add(self):
        # TODO
        pass


class PriorityQueuePolicy(ISchedulePolicy):
    def __init__(self):
        pass

    def has_target(self):
        # TODO
        pass

    def pop(self):
        # TODO
        pass

    def add(self):
        # TODO
        pass


class Scheduler(object):
    def __init__(self, schedule_policy):
        self.schedule_policy = schedule_policy

    def loop(self):
        sp = self.schedule_policy
        while True:
            if sp.has_target():
                event = sp.pop()
                event.run()

    def add(self, event):
        sp = self.schedule_policy
        sp.add(event)


if __name__ == "__main__":
    # schedule_policy = RoundRobinSchedulePolicy()
    # schedule_policy = PriorityQueuePolicy()
    schedule_policy = PriorityQueuePolicy()
    Scheduler(schedule_policy).loop()



























