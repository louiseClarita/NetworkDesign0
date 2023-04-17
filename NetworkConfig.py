import threading
from NodeClassV1_2 import NodeClass as Node
#from Tangle1 import Tangle


# def initialize_tangle():
#     # Initialize the tangle object here
#     tangle = Tangle()
#     return tangle
class Network:
    nodes: Node
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




nodes = [ 1,2,3, 4, 5,6,7,8]
edges = [(1,4),(1,3),(2,4),(2,3),(3,5),(3,6),(4,7),(4,8)]
#pos = nx.spring_layout(G)
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

# tangle1 = initialize_tangle()
# tangle2 = initialize_tangle()
# tangle3 = initialize_tangle()
# tangle4 = initialize_tangle()
# tangle5 = initialize_tangle()
# tangle6 = initialize_tangle()
# tangle7 = initialize_tangle()
# tangle8 = initialize_tangle()

node1 = Node("127.0.0.1",60345,[60347,60346])
node2 = Node("127.0.0.1",60348,[60347,60346])
node3 = Node("127.0.0.1",60347,[60345,60348,60349,60350])
node4 = Node("127.0.0.1",60346,[60345,60348,60351,60352])
node5 = Node("127.0.0.1",60349,[60347,60350])
node6 = Node("127.0.0.1",60350,[60347,60349])
node7 = Node("127.0.0.1",60351,[60346])
node8 = Node("127.0.0.1",60352,[60346])
network = Network([node1,node2,node3,node4,node5,node6,node7,node8])
network.StartThreadingOnAll()