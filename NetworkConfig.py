import threading
from threading import Semaphore
from NodeClassV1_3 import NodeClass as Node
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt

SemaphoreTuple = namedtuple('Semaphore', ['Semaphore', 'Nodes'])
dropMessagesWhenQIsFull = False

class Network:
    nodes: Node
    semaphores = [SemaphoreTuple]
    def __init__(self,nodes):
        self.nodes=nodes


    def nodeCounterReset(self):
        for i in self.nodes:
            i.broadcastCounter = 0
            i.inputNodesList = []

    def getNodeByPort(self,node):
        for i in self.nodes:
            if i.ports == node:
                return i
        else:
            return -1
    # def displayTangle(self):
    #
    #     for i in self.nodes:
    #      i.tangle.display_tangle()

    def printNetwork(self):
        print("nodes : [", flush=True)
        count = 0
        for i in self.nodes:
            print("node "+ str(count) + " : \n")
            i.ToString()
            count=count+1
            print("\n")
        print("]", flush=True)

    def StartThreadingOnAll(self):
        threads = []
        for i in self.nodes:
         t = threading.Thread(target=i.zmqRead2, args=())
         t.daemon = True
         threads.append(t)
         t.start()


    def initSemaphores(self,semaphoreValue):
        for node in self.nodes:
            for neighborPort in node.neighbors:
                if any(semaphore.Nodes == [node.ports, neighborPort] or semaphore.Nodes == [neighborPort,node.ports] for semaphore in self.semaphores):
                    print('The ports are already in the semaphores list!')
                else:
                    Network.semaphores.append(SemaphoreTuple(Semaphore(semaphoreValue), [node.ports, neighborPort]))
                    print('Semaphore added!! :) ')

  # Define the nodes and edges of the network
    nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    edges = [(1, 4), (1, 3), (2, 4), (2, 3), (3, 5),(5,6), (3, 6), (4, 7), (4, 8)]

    # Create the graph object
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(nodes)

    # Add edges to the graph
    G.add_edges_from(edges)

    # pos = nx.spring_layout(G)
    pos = {1: (0, 0), 2: (2, 0), 3: (0, -2), 4: (2, -2), 5: (-3, -5), 6: (1, -5), 7: (3, -5), 8: (7, -5)}



    labeldict = {}
    labeldict[1] = "60345"
    labeldict[2] = "60348"
    labeldict[3] = "60347"
    labeldict[4] = "60346"
    labeldict[5] = "60349"
    labeldict[6] = "60350"
    labeldict[7] = "60351"
    labeldict[8] = "60352"

    # Draw the graph
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels=labeldict)
    # nx.draw(G, pos,with_labels=True)


    # Show the graph
    plt.show()

node1 = Node("127.0.0.1",60345,[60347,60346],1)
node2 = Node("127.0.0.1",60348,[60347,60346],1)
node3 = Node("127.0.0.1",60347,[60345,60348,60349,60350],1)
node4 = Node("127.0.0.1",60346,[60345,60348,60351,60352],1)
node5 = Node("127.0.0.1",60349,[60347,60350],1)
node6 = Node("127.0.0.1",60350,[60347,60349],1)
node7 = Node("127.0.0.1",60351,[60346],1)
node8 = Node("127.0.0.1",60352,[60346],1)
network = Network([node1,node2,node3,node4,node5,node6,node7,node8])
network.StartThreadingOnAll()
network.initSemaphores(50)
print("semaphoressss:  "+ str(network.semaphores))







    #self.semaphores.append({'Semaphore': Semaphore(4), 'Nodes': [node1.ports,node1.neighbors]})

