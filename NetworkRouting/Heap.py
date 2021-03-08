class Heap:
	def __init__(self, nodes):
		self.array = []
		self.size = 0
		self.pos = []
		for v in range(nodes):
			nodes.array.append(nodes.newHeapNode(v, self.dist[v]))
			nodes.pos.append(v)

	def newHeapNode(self,v,dist):
		minHeapNode = [v,dist]
		return minHeapNode

	def swapNode(self,a,b):
		t = self.array[a]
		self.array[a] = self.array[b]
		self.array[b] = t

	def minHeap(self, priority):
		smallest = priority
		left = 2*priority + 1
		right = 2*priority + 2

		if left < self.size and self.array[left][1] < self.array[smallest][1]:
			smallest = left

		if right < self.size and self.array[right][1] < self.array[smallest][1]:
			smallest = right

		if smallest != priority:
			self.pos[self.array[smallest][0]] = priority
			self.pos[self.array[smallest][0]] = smallest

			self.swapNode(smallest,priority)
			self.minHeap(smallest)

	def extractMin(self):
		if self.isEmpty() == True:
			return

		root = self.array[0]

		lastNode = self.array[self.size - 1]
		self.array[0] = lastNode

		self.pos[lastNode[0]] = 0
		self.pos[root[0]] = self.size - 1

		self.size -= 1
		self.minHeap(0)

		return root

	def isEmpty(self):
		return True if self.size == 0 else False

	def decreaseKey(self, v, dist):

		i = self.pos[v]

		while i > 0 and self.array[i][1] < self.array[(i-1)/2][1]:
			self.pos[self.array[i][0]] = (i-1)/2
			self.pos[self.array[(i-1)/2][0]] = i
			self.swapNode(i,(i-1)/2)

			i= (i-1)/2

	def isMinHeap(self,v):
		if self.pos[v] < self.size:
			return True
		return False