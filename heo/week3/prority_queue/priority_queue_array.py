class PriorityQueueArray:
    def __init__(self):
        self.size = 0
        self.array = []

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def insert(self, item):
        if self.is_empty():
            self.array.append(item)
            self.size = self.size + 1

        else:
            self.array.append(item)
            self.size = self.size + 1

            for i, elem in enumerate(self.array):
                if elem > item:
                    # when insert item at last priority just pass
                    # when insert item at first priority
                    if i == 0:
                        for idx in range(self.size-1, 0, -1):
                            self.array[idx] = self.array[idx-1]
                        self.array[0] = item
                        break
                    # when insert item at middle priority
                    elif i > 1:
                        for idx in range(self.size-1, i, -1):
                            self.array[idx] = self.array[idx-1]
                            print(idx, i)
                        self.array[i] = item
                        break

    def delete(self):
        if self.is_empty():
            print("Priority Queue is empty !")
        else:
            result = self.array[0]
            for i in range(self.size-1):
                self.array[i] = self.array[i+1]
            self.array.pop()
            self.size = self.size - 1
            return result