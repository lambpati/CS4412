import sys

# Creates a priority queue array of nodes and distances
class Array:
    def __init__(self, nodes):
        self.array = [[node, sys.maxsize] for node in nodes]
        self.size = len(nodes)
        self.pos = [None] * self.size
        for i, node in enumerate(nodes):
            self.pos[node.node_id] = i

    # Set the distance of a node to 1 O(1)
    def weight(self, i):
        return self.array[i][1]

    # Swap nodes a and b O(1)
    def swapNode(self, a, b):
        self.array[a], self.array[b] = self.array[b], self.array[a]
        c = self.array[a][0].node_id
        d = self.array[b][0].node_id
        self.pos[c], self.pos[d] = self.pos[d], self.pos[c]

    # Swap node with the node below it O(1)
    def decreaseKey(self, v, dist):
        i = self.pos[v]
        if i >= self.size:
            return
        self.array[i][1] = dist

    # Checks if the array is empty O(1)
    def isEmpty(self):
        return self.size == 0

    # Extract the minimum node from the array O(|V|)
    def extractMin(self):
        if self.size == 0:
            return
        i = min(range(self.size), key=self.weight)
        self.swapNode(i, self.size - 1)
        node, _ = self.array.pop()
        self.size -= 1
        return node
