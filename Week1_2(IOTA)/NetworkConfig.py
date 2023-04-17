import threading
from NodeV1_2 import Node
from Tangle1 import Tangle


def initialize_tangle():
    # Initialize the tangle object here
    tangle = Tangle()
    return tangle
class Network:
    nodes : Node
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
    def displayTangle(self):

        for i in self.nodes:
         i.tangle.display_tangle()

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
         t = threading.Thread(target=i.zmqRead, args=())
         t.daemon = True
         threads.append(t)
         t.start()



nodes = [ 1,2,3, 4, 5,6,7,8]
edges = [(1,4),(1,3),(2,4),(2,3),(3,5),(3,6),(4,7),(4,8)]
#pos = nx.spring_layout(G)
pos = {1: (0, 0), 2: (2, 0), 3: (0, -2), 4: (2, -2), 5: (-3, -5), 6: (1, -5), 7: (3, -5), 8: (7, -5)}


labeldict = {}
labeldict[1] = "12345"
labeldict[2] = "12348"
labeldict[3] = "12347"
labeldict[4] = "12346"
labeldict[5] = "12349"
labeldict[6] = "12350"
labeldict[7] = "12351"
labeldict[8] = "12352"

tangle1 = initialize_tangle()
tangle2 = initialize_tangle()
tangle3 = initialize_tangle()
tangle4 = initialize_tangle()
tangle5 = initialize_tangle()
tangle6 = initialize_tangle()
tangle7 = initialize_tangle()
tangle8 = initialize_tangle()

node1 = Node("127.0.0.1",12345,[12347,12346],tangle1,)
node2 = Node("127.0.0.1",12348,[12347,12346],tangle2)
node3 = Node("127.0.0.1",12347,[12345,12348,12349,12350],tangle3)
node4 = Node("127.0.0.1",12346,[12345,12348,12351,12352],tangle4)
node5 = Node("127.0.0.1",12349,[12347,12350],tangle5)
node6 = Node("127.0.0.1",12350,[12347,12349],tangle6)
node7 = Node("127.0.0.1",12351,[12346],tangle7)
node8 = Node("127.0.0.1",12352,[12346],tangle8)
network = Network([node1,node2,node3,node4,node5,node6,node7,node8])
network.StartThreadingOnAll()