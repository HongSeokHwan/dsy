# Bubble
a = [3,4,1,2,7,9,10]
size = len(a)

for j in range(size-1, 1, -1):
	for i in range(0, j):
		if a[i] > a[i+1]:
			tmp = a[i]
			a[i] = a[i+1]
			a[i+1] = tmp


# Selection
b = [3,4,1,2,7,9,10]
size_b = len(b)

for i in range(0, size_b-1):
	min_var = min(b[i:])
	idx = b.index(min_var)

	b[i], b[idx] = b[idx], b[i]


# Selection2
c = [3,4,1,2,7,9,10]
size_c = len(c)

for i in range(0, size_c-1):
	tmp_min = c[-1]
	idx = -1

	for j in range(i, size_c-1):
		if c[j] < tmp_min:
			tmp_min = c[j]
			idx = j

	c[i], c[idx] = c[idx], c[i]
