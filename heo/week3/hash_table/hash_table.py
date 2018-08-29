class HashTable:
    def __init__(self, size):
        self.table = [[] for _ in range(size)] 
        self.size = size

    def hash_function(self, key):
        return key % self.size

    def put(self, key, value):
        index = self.hash_function(key)
        bucket = self.table[index]
        flag = None
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                bucket[i] = (key, value)
                flag = True
        if not flag:
            bucket.append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                return v
        print("search Error: Key {} doesn't exist".format(key))

    def delete(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        flag = None
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                del bucket[i]
                flag = True

        if not flag:
            print("delete Error: Key {} doesn't exist".format(key))