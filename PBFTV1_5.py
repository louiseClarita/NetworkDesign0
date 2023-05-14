import threading

import NetworkConfig
import time

threads = []
threadsPrepare = []

start_time = 0
convergence_time =0

def validateMsg(stop_event):
    while not stop_event:

        doneMsgsNbr = 0
        for node in NetworkConfig.network.nodes:
          if bool(node.state):
            if node.state["1"] == "done":
                doneMsgsNbr += 1

        if doneMsgsNbr > (NetworkConfig.num_nodes * 2) / 3:
            print("msg is validated.....", flush=True)
            global convergence_time, start_time
            convergence_time = time.time() - start_time
            printTheValuesNeeded()
            stop_event = True

def printTheValuesNeeded():

    print("Pre-prepare Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToStringBroadcast()
    print("]", flush=True)


    print("Prepare Phase:", flush=True)

    print("nodes : [", flush=True)

    for node in NetworkConfig.network.nodes:
        node.ToStringPrepare()


    print("]", flush=True)


    print("Commit Phase:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ToStringCommit()


    print("]", flush=True)

    print("The Number Of Messages Dropped in bits is: " + str(NetworkConfig.BitsNumberOfMessagesDropped), flush=True)
    print("The Number Of Messages in bits is: "+str(NetworkConfig.TotalBitsNumberOfMessages),flush=True )

    print("The Number Of Messages Dropped is: " + str(NetworkConfig.NumberOfMessagesDropped), flush=True)
    print("The Number Of Messages  is: " + str(NetworkConfig.TotalNumberOfMessages), flush=True)

    print(f"Convergence time: {convergence_time} seconds", flush=True)


    print("Storage:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ListToString()


    print("]", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ListToString2()


    print("]", flush=True)

    print("RCVD:", flush=True)

    print("nodes : [", flush=True)
    for node in NetworkConfig.network.nodes:
        node.ListToString()

    print("]", flush=True)


def CheckConsensus(message):

    print("PBFT algorithm is running...")
    global start_time
    start_time = time.time()
    for i,node in enumerate(NetworkConfig.network.nodes):
        node.broadcastMessage("Broadcast",node.ports,i+1)


    for i,node in enumerate(NetworkConfig.network.nodes):
        # Create a new thread object
        stop_event = False  # This event will be used to signal the thread to stop
        thread = threading.Thread(target=node.checkMessagesBroadcast, args=(stop_event,i+1,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    for i,node in enumerate(NetworkConfig.network.nodes):
        stop_event = False  # This event will be used to signal the thread to stop
        thread = threading.Thread(target=node.checkMessagesPrepare, args=(stop_event,i+1,))
        thread.daemon = True
        threadsPrepare.append(thread)
        thread.start()

    for i,node in enumerate(NetworkConfig.network.nodes):
        stop_event = False  # This event will be used to signal the thread to stop
        thread = threading.Thread(target=node.checkMessagesCommit, args=(stop_event,))
        thread.daemon = True
        threadsPrepare.append(thread)
        thread.start()

    stop_event =False
    validateMsg(stop_event)


    return True




CheckConsensus("test")