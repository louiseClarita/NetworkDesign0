import NetworkConfig
import time


def CheckConsensus(message):

    for i,node in enumerate(NetworkConfig.network.nodes):
        node.broadcastMessage(f"Broadcast{i+1}",node.ports,i+1)

    time.sleep(30)


    print("Pre-prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToString()
    print("]", flush=True)

    for node in NetworkConfig.network.nodes:
        node.checkMessagesBroadcast()


    for i, node in enumerate(NetworkConfig.network.nodes):
        if node.isValidBroadcast:
            node.broadcastMessage(f"Prepare{i + 1}", node.ports, i + 9)



    time.sleep(30)


    print("Prepare Phase:", flush=True)

    print("nodes : [", flush=True)

    for node in NetworkConfig.network.nodes:
        node.ToString()


    print("]", flush=True)


    for node in NetworkConfig.network.nodes:
        node.checkMessagesPrepare()

    for i,node in enumerate(NetworkConfig.network.nodes):
            if node.isValidPrepare:
                node.broadcastMessage(f"Commit{i+1}",node.ports,i+17)


    time.sleep(30)

    print("Commit Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToString()

    message
    print("]", flush=True)

    return True

CheckConsensus("test")