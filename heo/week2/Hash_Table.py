class HashTable:
	def __init__(self):
		self.size = 11
		self.slots = [None] * self.size
		self.data = [None] * self.size


	def put(self, key, data):
		hashvalue = self.hashfunc(key, len(self.slots))

		if self.slots[hashvalue] == None:
			self.slots[hashvalue] = key
			self.data[hashvalue] = data
		else:
			if self.slots[hashvalue] == key:
				self.data[hashvalue] = data
			else:
				nextslot = self.rehash(hashvalue, len(self.slots))
				while self.slots[nextslot] != None and \
								self.slots[nextslot] != key:
					nextslot = self.rehash(nextslot, len(self.slots))

				if self.slots[nextslot] == None:
					self.slots[nextslot] = key
					self.data[nextslot] = data
				else:
					self.data[nextslot] = data


	def hashfunc(self, key, size):
		return key % size


	def rehash(self, oldhash, size):
		return (oldhash+1) % size	


	def get(self, key):
		startslot = self.hashfunc(key, len(self.slots))

		data = None
		position = startslot
		while self.slots[position] != None:
			if self.slots[position] == key:
				data = self.data[position]
				break
			else:
				position = self.rehash(position, len(self.slots))
				if position == startslot:
					break
		return data


	def __getitem__(self, key):
		return self.get(key)


	def __setitem__(self, key, data):
		self.put(key, data)


H = HashTable()
H[54] = "cat"
H[26] = "dog"
H[93] = "lion"
H[17] = "tiger"
H[77] = "bird"
H[31] = "cow"
print(H.slots)
print(H.data)
print(H[31])
