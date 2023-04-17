import networkx as nx
import matplotlib.pyplot as plt
import threading
import NetworkConfig
import time
import importlib
import sys




def CheckConsensus(message):
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


    # reRunThreads()
    # reRunThreads()
    # for i in range(8):
    #
    #     print(i, flush=True)
    #     reRunThreads()
    #     nodesList[i].zmqBroadCast2("pre-prepare", nodesList[i].ports)
    #     time.sleep(20)
    #     reRunThreads()


    # NetworkConfig.network.nodeCounterReset()
    # for i,node in enumerate(NetworkConfig.network.nodes):
    #     node.zmqBroadCast(f"broadcast{i+1}",node.ports)
    #     NetworkConfig.network.nodeCounterReset()
    #


    NetworkConfig.node1.zmqBroadCast("Broadcast1", 60345)

    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node2.zmqBroadCast("Broadcast2", 60348)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node3.zmqBroadCast("Broadcast3", 60347)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node4.zmqBroadCast("Broadcast4", 60346)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node5.zmqBroadCast("Broadcast5", 60349)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node6.zmqBroadCast("Broadcast6", 60350)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node7.zmqBroadCast("Broadcast7", 60351)
    time.sleep(15)

    NetworkConfig.network.nodeCounterReset()
    NetworkConfig.node8.zmqBroadCast("Broadcast8", 60352)


    time.sleep(25)


    print("Pre-prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    NetworkConfig.node1.ToString()
    NetworkConfig.node2.ToString()
    NetworkConfig.node3.ToString()
    NetworkConfig.node4.ToString()
    NetworkConfig.node5.ToString()
    NetworkConfig.node6.ToString()
    NetworkConfig.node7.ToString()
    NetworkConfig.node8.ToString()
    print("]", flush=True)

    # NetworkConfig.node1.messageRCVD.clear()
    # NetworkConfig.node2.messageRCVD.clear()
    # NetworkConfig.node3.messageRCVD.clear()
    # NetworkConfig.node4.messageRCVD.clear()
    # NetworkConfig.node5.messageRCVD.clear()
    # NetworkConfig.node6.messageRCVD.clear()
    # NetworkConfig.node7.messageRCVD.clear()
    # NetworkConfig.node8.messageRCVD.clear()

    #
    # for i,node in enumerate(nodesList):
    #  if node.checkMessagesBroadcast():
    #      node.zmqBroadCast2(f"Prepare{i}", node.ports)
    #      time.sleep(15)
    #      reRunThreads()
    #  else:
    #      print("not true", flush=True)
    #


    # for i,node in enumerate(NetworkConfig.network.nodes):
    #         if NetworkConfig.node.checkMessagesBroadcast():
    #             print("msgs checked", flush=True)
    #             node.zmqBroadCast(f"Prepare{i+1}",node.ports)
    #             NetworkConfig.network.nodeCounterReset()
    #

    NetworkConfig.node1.checkMessagesBroadcast()
    NetworkConfig.node2.checkMessagesBroadcast()
    NetworkConfig.node3.checkMessagesBroadcast()
    NetworkConfig.node4.checkMessagesBroadcast()
    NetworkConfig.node5.checkMessagesBroadcast()
    NetworkConfig.node6.checkMessagesBroadcast()
    NetworkConfig.node7.checkMessagesBroadcast()
    NetworkConfig.node8.checkMessagesBroadcast()




    if NetworkConfig.node1.isValidBroadcast:
        # reRunThreads()
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node1.zmqBroadCast("Prepare1", 60345)
        time.sleep(25)




    if NetworkConfig.node2.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node2.zmqBroadCast("Prepare2", 60348)
        time.sleep(25)


    if NetworkConfig.node3.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node3.zmqBroadCast("Prepare3", 60347)
        time.sleep(25)


    if NetworkConfig.node4.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node4.zmqBroadCast("Prepare4", 60346)
        time.sleep(25)


    if NetworkConfig.node5.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node5.zmqBroadCast("Prepare5", 60349)
        time.sleep(25)

    if NetworkConfig.node6.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node6.zmqBroadCast("Prepare6", 60350)
        time.sleep(25)


    if NetworkConfig.node7.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node7.zmqBroadCast("Prepare7", 60351)
        time.sleep(25)


    if NetworkConfig.node8.isValidBroadcast:
        print("msgss checked", flush=True)
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node8.zmqBroadCast("Prepare8", 60352)
        time.sleep(25)



    print("Prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    NetworkConfig.node1.ToString()
    NetworkConfig.node2.ToString()
    NetworkConfig.node3.ToString()
    NetworkConfig.node4.ToString()
    NetworkConfig.node5.ToString()
    NetworkConfig.node6.ToString()
    NetworkConfig.node7.ToString()
    NetworkConfig.node8.ToString()
    print("]", flush=True)

    # NetworkConfig.node1.messageRCVD.clear()
    # NetworkConfig.node2.messageRCVD.clear()
    # NetworkConfig.node3.messageRCVD.clear()
    # NetworkConfig.node4.messageRCVD.clear()
    # NetworkConfig.node5.messageRCVD.clear()
    # NetworkConfig.node6.messageRCVD.clear()
    # NetworkConfig.node7.messageRCVD.clear()
    # NetworkConfig.node8.messageRCVD.clear()
    #
    # for i,node in enumerate(NetworkConfig.network.nodes):
    #         if NetworkConfig.node.checkMessagesBroadcast():
    #             print("msgs checked", flush=True)
    #             node.zmqBroadCast(f"Commit{i+1}",node.ports)
    #             NetworkConfig.network.nodeCounterReset()


    NetworkConfig.node1.checkMessagesPrepare()
    NetworkConfig.node2.checkMessagesPrepare()
    NetworkConfig.node3.checkMessagesPrepare()
    NetworkConfig.node4.checkMessagesPrepare()
    NetworkConfig.node5.checkMessagesPrepare()
    NetworkConfig.node6.checkMessagesPrepare()
    NetworkConfig.node7.checkMessagesPrepare()
    NetworkConfig.node8.checkMessagesPrepare()

    NetworkConfig.network.nodeCounterReset()
    if NetworkConfig.node1.isValidPrepare:
        NetworkConfig.network.nodeCounterReset()
        NetworkConfig.node1.zmqBroadCast("Commit1", 60345)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()
    if  NetworkConfig.node2.checkMessagesPrepare():
        NetworkConfig.node2.zmqBroadCast("Commit2", 60348)
        time.sleep(25)

        NetworkConfig.network.nodeCounterReset()
    if NetworkConfig.node3.isValidPrepare:
         NetworkConfig.node3.zmqBroadCast("Commit3", 60347)
         time.sleep(25)
         NetworkConfig.network.nodeCounterReset()

    if NetworkConfig.node4.isValidPrepare:
        NetworkConfig.node4.zmqBroadCast("Commit4", 60346)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()

    if NetworkConfig.node5.isValidPrepare:
        NetworkConfig.node5.zmqBroadCast("Commit5", 60349)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()

    if NetworkConfig.node6.isValidPrepare:
        NetworkConfig.node6.zmqBroadCast("Commit6", 60350)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()

    if NetworkConfig.node7.isValidPrepare:
        NetworkConfig.node7.zmqBroadCast("Commit7", 60351)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()

    if NetworkConfig.node8.isValidPrepare:
        NetworkConfig.node8.zmqBroadCast("Commit8", 60352)
        time.sleep(25)
        NetworkConfig.network.nodeCounterReset()


    print("Commit Phase:", flush=True)

    print("nodes : [", flush=True)
    NetworkConfig.node1.ToString()
    NetworkConfig.node2.ToString()
    NetworkConfig.node3.ToString()
    NetworkConfig.node4.ToString()
    NetworkConfig.node5.ToString()
    NetworkConfig.node6.ToString()
    NetworkConfig.node7.ToString()
    NetworkConfig.node8.ToString()

    message
    print("]", flush=True)





    return True
