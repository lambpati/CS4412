class Array:
	def __init__(self, nodes):
		self.arrayQ = []
		self.size = 0
		self.pos = []

		for v in range(nodes):
			nodes.array.append(nodes.newArrayNode(v, self.dist[v]))
			nodes.pos.append(v)

	def newArrayNode(self, v, dist):
		newArrayNode = [v,dist]
		return newArrayNode

	def swapNode(self,a,b):
		t = self.arrayQ[a]
		self.arrayQ[a] = self.arrayQ[b]
		self.arrayQ[b] = t

	def addValues(self,v,dist):
		index = self.size
		self.arrayQ.append(self.newArrayNode(v,dist))

		while self.arrayQ[index][1] < self.arrayQ[index - 1][1] and index - 1 >= 0:
			self.swap(index, index - 1)
			index -= 1

	def decreaseKey(self,v,dist):
		i = self.pos[v]

		while i > 0 and self.arrayQ[i][1] < self.arrayQ[(i - 1) / 2][1]:
			self.pos[self.arrayQ[i][0]] = (i - 1) / 2
			self.pos[self.arrayQ[(i - 1) / 2][0]] = i
			self.swapNode(i, (i - 1) / 2)

			i = (i - 1) / 2

	def isEmpty(self):
		return True if self.size == 0 else False

	def extractMin(self):
		if self.size == 0:
			return
		lastNode = self.arrayQ.pop(0)
		return lastNode