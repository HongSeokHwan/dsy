class PriorityQueueHeap:
    def __init__(self):
        self.size = 0
        self.heap = [0]

    def heapify(self, i):
        if i == self.size:
            while i // 2 > 0:
                if self.heap[i] < self.heap[i // 2]:
                    tmp = self.heap[i]
                    self.heap[i] = self.heap[i // 2]
                    self.heap[i // 2] = tmp
                i = i // 2
        else:
            while i * 2 <= self.size:
                minimum_child = self.find_min_child(i)
                if self.heap[i] > self.heap[minimum_child]:
                    tmp = self.heap[i]
                    self.heap[i] = self.heap[minimum_child]
                    self.heap[minimum_child] = tmp
                i = minimum_child

    def insert(self, i):
        self.heap.append(i)
        self.size = self.size + 1
        self.heapify(self.size)

    def delete(self):
        highest = self.heap[1]
        self.heap[1] = self.heap[self.size]
        self.heap.pop()
        self.size = self.size - 1
        self.heapify(1)
        return highest

    def find_min_child(self, i):
        if i * 2 == self.size:
            return i * 2
        else:
            if self.heap[i * 2] < self.heap[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def build_heap(self, input_list):
        i = len(input_list) // 2
        self.size = len(input_list)
        self.heap = [0] + input_list[:]
        while i > 0:
            self.heapify(i)
            i = i - 1