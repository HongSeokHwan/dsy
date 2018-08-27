# priority_queue_by_array
class Priority_queue(object):
    def __init__(self, data=[]):
        self.queue = data
    
    def insert(self, key):
        self.queue.append(key)

    def find_max(self):
        maximum = self.queue[0]
        for i in range(len(self.queue)):
            if maximum < self.queue[i]:
                maximum = self.queue[i]
        return maximum

    def extract_max(self):
        max_value = self.find_max()
        self.queue.remove(max_value)
        return max_value

    def increase_key(self, element, key):
        if key < self.queue[element]:
            return
        else:
            self.queue[element] = key