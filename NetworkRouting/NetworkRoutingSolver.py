#!/usr/bin/python3


from CS4412Graph import *
from NetworkRouting.Heap import *
from NetworkRouting.Array import *
import time
import sys


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS4412Graph)
        self.network = network

    # Returns shortest path between current node and destination node
    def getShortestPath(self, destIndex):
        self.dest = destIndex

        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        while destIndex != node.node_id:
            path_edges.append((self.network.nodes[self.prev[destIndex]].loc, self.network.nodes[destIndex].loc,
                               '{:.0f}'.format(self.dist[destIndex])))

            total_length += self.dist[destIndex]
            destIndex = self.prev[destIndex]

        return {'cost': total_length, 'path': path_edges}

    # Runs Dijkstra's Algorithm using a heap or an array
    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        V = self.network.nodes

        self.prev = {}
        self.dist = {}
        self.pos = {}

        # Complexity using heap: O((|V| + |E|)log |V|)
        if use_heap == True:
            priorityQ = Heap(V)

        # Complexity using array: O(|V|^2)
        else:
            priorityQ = Array(V)

        for i in V:
            self.dist[i.node_id] = sys.maxsize
            self.prev[i.node_id] = None

        priorityQ.pos[srcIndex] = srcIndex
        self.dist[srcIndex] = 0
        priorityQ.decreaseKey(srcIndex, self.dist[srcIndex])

        while not priorityQ.isEmpty():

            u = priorityQ.extractMin()

            for edge in u.neighbors:
                if self.dist[edge.dest.node_id] > self.dist[u.node_id] + edge.length:
                    self.dist[edge.dest.node_id] = self.dist[u.node_id] + edge.length
                    self.prev[edge.dest.node_id] = u.node_id

                    priorityQ.decreaseKey(edge.dest.node_id, self.dist[edge.dest.node_id])
                    self.pos[edge.dest.node_id] = edge.length

        t2 = time.time()
        return (t2 - t1)
