import NetworkConfig
import time


def CheckConsensus(message):

    for i,node in enumerate(NetworkConfig.network.nodes):
        node.broadcastMessage(f"Broadcast{i+1}",node.ports,i+1)
        time.sleep(1)

    time.sleep(10)


    print("Pre-prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToString()
    print("]", flush=True)

    for node in NetworkConfig.network.nodes:
        node.checkMessagesBroadcast()
        time.sleep(1)


    for i, node in enumerate(NetworkConfig.network.nodes):
        if node.isValidBroadcast:
            node.broadcastMessage(f"Prepare{i + 1}", node.ports, i + 9)

    # dd

    time.sleep(30)


    print("Prepare Phase:", flush=True)

    print("nodes : [", flush=True)

    for node in NetworkConfig.network.nodes:
        node.ToString()


    print("]", flush=True)


    for node in NetworkConfig.network.nodes:
        node.checkMessagesPrepare()
        time.sleep(1)

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

    print("The Drop rate is:"+str(NetworkConfig.BitsOfMessagesDropped),flush=True )

    print("Storage:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ListToString()

    message
    print("]", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ListToString2()

    message
    print("]", flush=True)

    return True

CheckConsensus("test")