#!/usr/bin/python3


from CS4412Graph import *
from Heap import *
from Array import *
import time
import sys


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        while destIndex != node.node_id:
            path_edges.append((self.network.nodes[self.prev[destIndex].loc,self.network.nodes[destIndex].loc], '{:.0f}'.format(self.dist[destIndex])))

            total_length += self.dist[destIndex]
            destIndex = self.prev[destIndex]

        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        V = self.network.nodes

        self.prev = {}
        self.dist = {}
        self.pos = {}

        if use_heap == True:
            priorityQ = Heap(V)
        else:
            priorityQ = Array(V)

        for i in V:
            self.dist[i.node_id] = sys.maxsize
            self.prev[i.node_id] = None

        priorityQ.pos[srcIndex] = srcIndex
        self.dist[srcIndex] = 0
        priorityQ.decreaseKey(srcIndex,self.dist[srcIndex])

        priorityQ.size = V

        while priorityQ.isEmpty() == False:

            newNode = priorityQ.extractMin()

            u = newNode[0]

            for edge in u.neighbors:
                if self.dist[edge.dest.node_id] > self.dist[u.node_id] + len(edge):
                    self.dist[edge.dest.node_id] = self.dist[u.node_id] + len(edge)
                    self.prev[edge.dest.node_id] = u.node_id

                    priorityQ.decreaseKey(edge.dest.node_id,self.dist[edge.dest.node_id])
                    self.pos[edge.dest.node_id] = len(edge)

        t2 = time.time()
        return (t2-t1)

