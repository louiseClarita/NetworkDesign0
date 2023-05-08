import NetworkConfig
import time


def CheckConsensus(message):

    for i,node in enumerate(NetworkConfig.network.nodes):
        node.broadcastMessage(f"Broadcast{i+1}",node.ports,i+1)


    time.sleep(4)


    print("Pre-prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToString()
    print("]", flush=True)

    for node in NetworkConfig.network.nodes:
        node.checkMessagesBroadcast()



    for i, node in enumerate(NetworkConfig.network.nodes):
        if node.isValidBroadcast:
            node.broadcastMessage(f"Prepare{i + 1}", node.ports, i + 1 + 8)



    time.sleep(4)


    print("Prepare Phase:", flush=True)

    print("nodes : [", flush=True)

    for node in NetworkConfig.network.nodes:
        node.ToString()


    print("]", flush=True)


    for node in NetworkConfig.network.nodes:
        node.checkMessagesPrepare()


    for i,node in enumerate(NetworkConfig.network.nodes):
            if node.isValidPrepare:
                node.broadcastMessage(f"Commit{i+1}", node.ports, i + 1 + 2 * 8)


    time.sleep(4)

    print("Commit Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToString()

    message
    print("]", flush=True)

    print("The Number Of Messages Dropped in bits is: " + str(NetworkConfig.BitsNumberOfMessagesDropped), flush=True)
    print("The Number Of Messages in bits is: "+str(NetworkConfig.TotalBitsNumberOfMessages),flush=True )

    print("The Number Of Messages Dropped is: " + str(NetworkConfig.NumberOfMessagesDropped), flush=True)
    print("The Number Of Messages  is: " + str(NetworkConfig.TotalNumberOfMessages), flush=True)


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