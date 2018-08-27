import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import linked_list.linked_list as linked_list
import math

class Hash_table(object):
    def __init__(self, table_size=0):
        self.table_size = table_size
        bucket = linked_list.Linked_list()
        self.hash_table = [bucket] * table_size
        self.input_size = 0
        
    def hash(self, key):
        '''
            This method uses the multiplication method
            and returns the slot with the hash result
        '''
        if type(key) == str:
            result = 0
            for char in key:
                result += ord(char)
            key = result
        floating_number = 0.987729
        fraction_part = key * floating_number - int(key * floating_number)
        hash_result = math.floor(fraction_part * self.table_size)
        return hash_result

    def search(self, key):
        hash_result = self.hash(key)
        slot = self.hash_table[hash_result]
        return slot.search(key)

    def insert(self, key):
        hash_result = self.hash(key)
        slot = self.hash_table[hash_result]
        if slot.search(key) is None:
            slot.insert(key)
        self.input_size += 1
        if self.input_size == self.table_size:
            self.resize()

    def delete(self, key):
        hash_result = self.hash(key)
        slot = self.hash_table[hash_result]
        slot.delete(key)

    def resize(self):
        self.table_size = self.table_size * 2
        bucket = linked_list.Linked_list()
        new_table = [bucket] * self.table_size
        for i in range(len(self.hash_table)):
            new_table[i] = self.hash_table[i]
        self.hash_table = new_table

    def reshape_bucket(self):
        pass
