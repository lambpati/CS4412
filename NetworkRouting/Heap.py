import sys


def parent(i):
    return (i - 1) // 2


def child(i, n):
    return 2 * i + n


def isRoot(i):
    return i == 0

# Creates a binary heap of nodes and distances
class Heap:
    def __init__(self, nodes):
        self.array = [[node, sys.maxsize] for node in nodes]
        self.size = len(nodes)
        self.pos = [None] * self.size
        for i, node in enumerate(nodes):
            self.pos[node.node_id] = i
        self.heapify()

    # Set the distance of a node to 1 O(1)
    def weight(self, i):
        return self.array[i][1]

    # Heapify and update all nodes when they are swapped position O(|V|)
    def heapify(self):
        for i in reversed(range(self.size)):
            if self.weight(i) < self.weight(parent(i)):
                self.swapNode(self, i, parent(i))

    # Swap two nodes of a heap O(log |V|)
    def swapNode(self, a, b):
        self.array[a], self.array[b] = self.array[b], self.array[a]
        c = self.array[a][0].node_id
        d = self.array[b][0].node_id
        self.pos[c], self.pos[d] = self.pos[d], self.pos[c]

    # Tests if the node of the heap is a child O(1)
    def isChild(self, i):
        return 0 <= i < self.size

    # Tests if the node of the heap is a branch O(1)
    def isLeaf(self, i):
        return self.isChild(i) and not self.isChild(child(i, 1))

    # Push a branch down to being a child O(log |V|)
    def bubbleDown(self, i):
        while self.isChild(i) and not self.isLeaf(i):
            lowest = i
            if self.weight(child(i, 1)) < self.weight(lowest):
                lowest = child(i, 1)
            if self.isChild(child(i, 2)) and self.weight(child(i, 2)) < self.weight(lowest):
                lowest = child(i, 2)
            if lowest == i:
                return
            self.swapNode(i, lowest)
            i = lowest

    # Push the child up to being a branch O(log |V|)
    def bubbleUp(self, i):
        while not isRoot(i):
            if self.weight(i) >= self.weight(parent(i)):
                break
            self.swapNode(i, parent(i))
            i = parent(i)

    # Extract the minimum node from the heap O(log |V|)
    def extractMin(self):
        if self.isEmpty():
            return
        self.swapNode(0, self.size - 1)
        root, _ = self.array.pop()

        self.size -= 1
        self.bubbleDown(0)

        return root

    # Checks if the heap is empty O(1)
    def isEmpty(self):
        return self.size == 0

    # Swap node with its parent O(log |V|)
    def decreaseKey(self, v, dist):
        i = self.pos[v]
        if i >= self.size:
            return
        self.array[i][1] = dist
        self.bubbleUp(i)
