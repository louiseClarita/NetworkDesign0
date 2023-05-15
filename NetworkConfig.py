import threading
from threading import Semaphore
from NodeClassV1_5 import NodeClass as Node
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
#dd

SemaphoreTuple = namedtuple('Semaphore', ['Semaphore', 'Nodes'])


num_nodes = 8
dropMessagesWhenQIsFull = True
maxQueueCapacity = 5
semaphoreMaxValue = 28
BitsNumberOfMessagesDropped = 0
NumberOfMessagesDropped = 0
TotalNumberOfMessages = 0
TotalBitsNumberOfMessages = 0
labeldict = {}


G = nx.Graph()
# pos = nx.spring_layout(G)
pos = {1: (0, 0), 2: (2, 0), 3: (0, -2), 4: (2, -2), 5: (-3, -5), 6: (1, -5), 7: (3, -5), 8: (7, -5)}
# pos = nx.spring_layout(G)
posLabels = {1: (-1, 0.3), 2: (3, 0.3), 3: (-1.3, -1.7), 4: (3.3, -1.7), 5: (-2.7, -4.7), 6: (0.7, -5.3),
             7: (3.7, -4.7), 8: (6.3, -5.3)}
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
                    nothing =0
                else:
                    Network.semaphores.append(SemaphoreTuple(Semaphore(semaphoreValue), [node.ports, neighborPort]))

    def drawNetwork(self):
            for i,node in enumerate(self.nodes):
                 labeldict[i+1].pop()
                 labeldict[i+1].append(node.state["1"])

            nx.draw_networkx_nodes(G, pos)
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, posLabels, labels=labeldict)
            # nx.draw(G, pos,with_labels=True)

            # Show the graph
            plt.show()
  # Define the nodes and edges of the network
    nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    edges = [(1, 4), (1, 3), (2, 4), (2, 3), (3, 5),(5,6), (3, 6), (4, 7), (4, 8)]

    # Create the graph object


    # Add nodes to the graph
    G.add_nodes_from(nodes)

    # Add edges to the graph
    G.add_edges_from(edges)





    labeldict[1] = ["60345",0]
    labeldict[2] = ["60348",0]
    labeldict[3] = ["60347",0]
    labeldict[4] = ["60346",0]
    labeldict[5] = ["60349",0]
    labeldict[6] = ["60350",0]
    labeldict[7] = ["60351",0]
    labeldict[8] = ["60352",0]

    # Draw the graph
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, posLabels, labels=labeldict)
    # nx.draw(G, pos,with_labels=True)


    # Show the graph
    plt.show()


node1 = Node("127.0.0.1",60345,[60347, 60346], maxQueueCapacity)
node2 = Node("127.0.0.1",60348,[60347, 60346],maxQueueCapacity)
node3 = Node("127.0.0.1",60347,[60345, 60348, 60349, 60350], maxQueueCapacity)
node4 = Node("127.0.0.1",60346,[60345,60348,60351,60352], maxQueueCapacity)
node5 = Node("127.0.0.1",60349,[60347,60350], maxQueueCapacity)
node6 = Node("127.0.0.1",60350,[60347,60349], maxQueueCapacity)
node7 = Node("127.0.0.1",60351,[60346], maxQueueCapacity)
node8 = Node("127.0.0.1",60352,[60346], maxQueueCapacity)
network = Network([node1,node2,node3,node4,node5,node6,node7,node8])
network.StartThreadingOnAll()
network.initSemaphores(semaphoreMaxValue)






    #self.semaphores.append({'Semaphore': Semaphore(4), 'Nodes': [node1.ports,node1.neighbors]})

