import networkx as nx
import matplotlib.pyplot as plt
import threading
from Node import Node


# Define the nodes and edges of the network
nodes = [ 1,2, 4, 5,6,7,8]
edges = [(1,4),(1,3),(2,4),(2,3),(3,5),(3,6),(4,7),(4,8)]

# Create the graph object
G = nx.Graph()

# Add nodes to the graph
G.add_nodes_from(nodes)

# Add edges to the graph
G.add_edges_from(edges)
pos = {1: (0, 0), 2: (1, 0), 3: (0, -2), 4: (1, -2), 5: (-3, -5), 6: (1, -5),7:(3,-5),8:(7,-5)}
# Draw the graph
nx.draw(G, pos,with_labels=True)
print(nx.is_eulerian(G))
# Show the graph
#plt.show()

node1 = Node("127.0.0.1",12345,[12347,12346])
node2 = Node("127.0.0.1",12348,[12347,12346])
node3 = Node("127.0.0.1",12347,[12345,12346])
node4 = Node("127.0.0.1",12346,[12345,12348])
node5 = Node("127.0.0.1",12349,[12347])
node6 = Node("127.0.0.1",12350,[12347])
node7 = Node("127.0.0.1",12351,[12351])
node8 = Node("127.0.0.1",12352,[12346])




#node4.listen();
#node1.listen();

#node3.sendData("Bonjour",12346)
#node4.readData();
#while True:
#  r = threading.Thread(target=node4.zmqRead1)
#  node4.zmqRead()

#  if r =="stop":
#     break
# Start a separate thread to read incoming messages
t = threading.Thread(target=node4.zmqRead, args=())
t.daemon = True
t.start()
#node4.zmqRead()

#t2 = threading.Thread(target=node3.zmqWrite, args=("Bonjour",12346))
#t2.daemon = True
#t2.start()
node3.zmqWrite("Bonjour",12346)
