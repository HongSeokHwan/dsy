class hashTable:
	def __init__(self):
		self.size = 10
		self.table = [[] for _ in range(self.size)]

	def hashfunc(self, key, size):
		return key % size

	def insert(self, key, value):
		position = self.hashfunc(key, self.size)
		key_exists = False
		bucket = self.table[position]
		# 동일 key 값 사용 여부 검사
		for i, kv in enumerate(bucket):
			k, v = kv
			if key == k:
				key_exists = True
				break
		# key 값 존재하는 경우 value replace
		if key_exists:
			bucket[i] = ((key, value))
		# 존재하지 않는 경우 key-value 쌍 추가
		else:
			bucket.append((key, value))

	def search(self, key):
		position = self.hashfunc(key, self.size)
		bucket = self.table[position]
		for i, kv in enumerate(bucket):
			k, v = kv
			if key == k:
				return v

	def delete(self, key):
		position = self.hashfunc(key, self.size)
		key_exists = False
		bucket = self.table[position]
		for i, kv in enumerate(bucket):
			k, v = kv
			if key == k:
				key_exists = True
				break
		if key_exists:
			del bucket[i]
			print('Key {} deleted'.format(key))
		else:
			print('Key {} not found'.format(key))