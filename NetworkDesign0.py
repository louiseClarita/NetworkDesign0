from NodeClass import NodeClass as Node
import networkx as nx
import matplotlib.pyplot as plt
import threading

import time


# Define the nodes and edges of the network
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
edges = [(1, 4), (1, 3), (2, 4), (2, 3), (3, 5), (3, 6), (4, 7), (4, 8)]

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

# Messages

messages = ["message1", "message2", "message3", "message4", "message5", "message6", "message7", "message8"]

# Draw the graph
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, labels=labeldict)
# nx.draw(G, pos,with_labels=True)
print("Graph Analysis")
print("Eulerin :" + str(nx.is_eulerian(G)))
betweenness_centrality = str(nx.betweenness_centrality(G))
print("Bridges? :" + betweenness_centrality)
print("Average shortest Path" + str(nx.closeness_centrality(G)))
print("Clustering Coefficient : " + str(nx.clustering(G)))

# Show the graph
plt.show()

node1 = Node("127.0.0.1", 60345, [60347, 60346])
node2 = Node("127.0.0.1", 60348, [60347, 60346])
node3 = Node("127.0.0.1", 60347, [60345, 60348, 60349, 60350])
node4 = Node("127.0.0.1", 60346, [60345, 60348, 60351, 60352])
node5 = Node("127.0.0.1", 60349, [60347])
node6 = Node("127.0.0.1", 60350, [60347])
node7 = Node("127.0.0.1", 60351, [60346])
node8 = Node("127.0.0.1", 60352, [60346])

nodesList = [node1, node2, node3, node4, node5, node6, node7, node8]

# Start a separate thread to read incoming messages
arg_value = 1
t = threading.Thread(target=node1.zmqRead, args=(arg_value,))
t.daemon = True
t.start()
arg_value = 2
t1 = threading.Thread(target=node2.zmqRead, args=(arg_value,))
t1.daemon = True
t1.start()
arg_value = 3
t2 = threading.Thread(target=node3.zmqRead, args=(arg_value,))
t2.daemon = True
t2.start()
arg_value = 4
t3 = threading.Thread(target=node4.zmqRead, args=(arg_value,))
t3.daemon = True
t3.start()
arg_value = 5
t4 = threading.Thread(target=node5.zmqRead, args=(arg_value,))
t4.daemon = True
t4.start()
arg_value = 6
t5 = threading.Thread(target=node6.zmqRead, args=(arg_value,))
t5.daemon = True
t5.start()
arg_value = 7
t6 = threading.Thread(target=node7.zmqRead, args=(arg_value,))
t6.daemon = True
t6.start()
arg_value = 8
t8 = threading.Thread(target=node8.zmqRead, args=(arg_value,))
t8.daemon = True
t8.start()


def reRunThreads():
    global t, t1, t2, t3, t4, t5, t6, t8
    if (not t.is_alive()):
        print("node 0: ")
        t.join()
        arg_value = 1
        t = threading.Thread(target=node1.zmqRead2, args=(arg_value,))
        t.daemon = True
        t.start()
    if (not t1.is_alive()):
        print("node 1: ")
        t1.join()
        arg_value = 2
        t1 = threading.Thread(target=node2.zmqRead2, args=(arg_value,))
        t1.daemon = True
        t1.start()
    if (not t2.is_alive()):
        print("node 2: ")
        t2.join()
        arg_value = 3
        t2 = threading.Thread(target=node3.zmqRead2, args=(arg_value,))
        t2.daemon = True
        t2.start()

    if (not t3.is_alive()):
        print("node 3: ", flush=True)
        t3.join()
        arg_value = 4
        t3 = threading.Thread(target=node4.zmqRead2, args=(arg_value,))
        t3.daemon = True
        t3.start()
    if (not t4.is_alive()):
        print("node 4: ", flush=True)
        t4.join()
        arg_value = 5
        t4 = threading.Thread(target=node5.zmqRead2, args=(arg_value,))
        t4.daemon = True
        t4.start()
    if (not t5.is_alive()):
        print("node 5: ", flush=True)
        t5.join()
        arg_value = 6
        t5 = threading.Thread(target=node6.zmqRead2, args=(arg_value,))
        t5.daemon = True
        t5.start()
    if (not t6.is_alive()):
        print("node 6: ", flush=True)
        t6.join()
        arg_value = 7
        t6 = threading.Thread(target=node7.zmqRead2, args=(arg_value,))
        t6.daemon = True
        t6.start()
    if (not t8.is_alive()):
        print("node 7: ", flush=True)
        t8.join()
        arg_value = 8
        t8 = threading.Thread(target=node8.zmqRead2, args=(arg_value,))
        t8.daemon = True
        t8.start()


print(f"list neibghors {node3.getNeighbors(0)}", flush=True)

# if node.messageRCVD.__len__() >= (nodesList.__len__()*2)/3:
# break

print("For loopp doneeeeee[")
reRunThreads()
reRunThreads()
# for i in range(8):
#
#     print(i, flush=True)
#     reRunThreads()
#     nodesList[i].zmqBroadCast2("pre-prepare", nodesList[i].ports)
#     time.sleep(20)
#     reRunThreads()



node1.zmqBroadCast("broadcast1", 60345)
reRunThreads()
time.sleep(15)
reRunThreads()
reRunThreads()
reRunThreads()
reRunThreads()
reRunThreads()

# node2.zmqBroadCast("broadcast2", 60348)
# time.sleep(15)
# reRunThreads()
# node3.zmqBroadCast("broadcast3", 60347)
# time.sleep(15)
# reRunThreads()
# node4.zmqBroadCast("broadcast4", 60346)
# time.sleep(15)
# reRunThreads()
# node5.zmqBroadCast("broadcast5", 60349)
# time.sleep(15)
# reRunThreads()
# node6.zmqBroadCast("broadcast6", 60350)
# time.sleep(15)
# reRunThreads()
# node7.zmqBroadCast("broadcast7", 60351)
# time.sleep(15)
# reRunThreads()
# node8.zmqBroadCast("broadcast8", 60352)
# reRunThreads()

time.sleep(25)


print("Pre-prepare Phase:", flush=True)

print("nodes : [", flush=True)
node1.ToString()
node2.ToString()
node3.ToString()
node4.ToString()
node5.ToString()
node6.ToString()
node7.ToString()
node8.ToString()

print("]", flush=True)

# node1.messageRCVD.clear()
# node2.messageRCVD.clear()
# node3.messageRCVD.clear()
# node4.messageRCVD.clear()
# node5.messageRCVD.clear()
# node6.messageRCVD.clear()
# node7.messageRCVD.clear()
# node8.messageRCVD.clear()











reRunThreads()
#
# for i,node in enumerate(nodesList):
#  if node.checkMessagesBroadcast():
#      node.zmqBroadCast2(f"Prepare{i}", node.ports)
#      time.sleep(15)
#      reRunThreads()
#  else:
#      print("not true", flush=True)
#

if node1.checkMessagesBroadcast():
    reRunThreads()
    print("msgss checked", flush=True)
    node1.zmqBroadCast("Prepare1", 60345)
    reRunThreads()
    reRunThreads()
    time.sleep(45)
    reRunThreads()
    reRunThreads()



# if node2.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node2.zmqBroadCast("Prepare2", 60348)
#     time.sleep(15)
#     reRunThreads()
#
# if node3.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node3.zmqBroadCast("Prepare3", 60347)
#     time.sleep(15)
#     reRunThreads()
#
# if node4.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node4.zmqBroadCast("Prepare4", 60346)
#     time.sleep(15)
#     reRunThreads()
#
# if node5.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node5.zmqBroadCast("Prepare5", 60349)
#     time.sleep(15)
#     reRunThreads()
# if node6.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node6.zmqBroadCast("Prepare6", 60350)
#     time.sleep(15)
#     reRunThreads()
#
# if node7.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node7.zmqBroadCast("Prepare7", 60351)
#     time.sleep(15)
#     reRunThreads()
#
# if node8.checkMessagesBroadcast():
#     print("msgss checked", flush=True)
#     node8.zmqBroadCast("Prepare8", 60352)
#     time.sleep(25)
#     reRunThreads()


print("Prepare Phase:", flush=True)

print("nodes : [", flush=True)
node1.ToString()
node2.ToString()
node3.ToString()
node4.ToString()
node5.ToString()
node6.ToString()
node7.ToString()
node8.ToString()

print("]", flush=True)

reRunThreads()
# node1.messageRCVD.clear()
# node2.messageRCVD.clear()
# node3.messageRCVD.clear()
# node4.messageRCVD.clear()
# node5.messageRCVD.clear()
# node6.messageRCVD.clear()
# node7.messageRCVD.clear()
# node8.messageRCVD.clear()

if node1.checkMessagesBroadcast():



    node1.zmqBroadCast("Commit1", 60345)
    time.sleep(60)
    reRunThreads()
    reRunThreads()
    reRunThreads()
    reRunThreads()
    reRunThreads()
    reRunThreads()

# if node2.checkMessagesBroadcast():
#     node2.zmqBroadCast("Commit2", 60348)
#     time.sleep(15)
#     reRunThreads()
#
# if node3.checkMessagesBroadcast():
#     node3.zmqBroadCast("Commit3", 60347)
#     time.sleep(15)
#     reRunThreads()
#
# if node4.checkMessagesBroadcast():
#     node4.zmqBroadCast("Commit4", 60346)
#     time.sleep(15)
#     reRunThreads()
#
# if node5.checkMessagesBroadcast():
#     node5.zmqBroadCast("Commit5", 60349)
#     time.sleep(15)
#     reRunThreads()
#
# if node6.checkMessagesBroadcast():
#     node6.zmqBroadCast("Commit6", 60350)
#     time.sleep(15)
#     reRunThreads()
#
# if node7.checkMessagesBroadcast():
#     node7.zmqBroadCast("Commit7", 60351)
#     time.sleep(25)
#     reRunThreads()
#
# if node8.checkMessagesBroadcast():
#     node8.zmqBroadCast("Commit8", 60352)
#     time.sleep(25)
#     reRunThreads()
#

print("Commit Phase:", flush=True)

print("nodes : [", flush=True)
node1.ToString()
node2.ToString()
node3.ToString()
node4.ToString()
node5.ToString()
node6.ToString()
node7.ToString()
node8.ToString()

print("]", flush=True)

print("Consensus has been reached!", flush=True)

print("End of program")
