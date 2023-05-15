import threading
import random
import numpy as np
import NetworkConfig
import time



threads = []
threadsPrepare = []
msgNumber = [0] * 24

start_time = 0
convergence_time =0

def validateMsg(stop_event):
    while not stop_event:

        doneMsgsNbr = 0
        for node in NetworkConfig.network.nodes:

          if bool(node.state):
            if node.state["1"] == "done":
                doneMsgsNbr += 1

        if doneMsgsNbr >= (NetworkConfig.num_nodes * 2) / 3:
            print("msg is validated.....", flush=True)
            global convergence_time, start_time
            convergence_time = time.time() - start_time
            printTheValuesNeeded()

            NetworkConfig.network.drawNetwork()

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

    print("The Number Of Messages Dropped in bits is: " + str(NetworkConfig.BitsNumberOfMessagesDropped), flush=True)
    print("The Number Of Messages in bits is: " + str(NetworkConfig.TotalBitsNumberOfMessages), flush=True)

    print("The Number Of Messages Dropped is: " + str(NetworkConfig.NumberOfMessagesDropped), flush=True)
    print("The Number Of Messages is: " + str(NetworkConfig.TotalNumberOfMessages), flush=True)

    print("The drop rate is: (" + str(NetworkConfig.BitsNumberOfMessagesDropped) + "/" + str(
        NetworkConfig.TotalBitsNumberOfMessages) + ")*100 = " + str(
        (NetworkConfig.NumberOfMessagesDropped / NetworkConfig.TotalNumberOfMessages) * 100), flush=True)

    print(f"Convergence time: {convergence_time} seconds", flush=True)

def addNoise(msg,noise,mean):
        noisy_msg = ""
        for c in msg:
            if random.random() < noise:
                noisy_msg += random.choice(list(set("abcdefghijklmnopqrstuvwxyz") - set(c.lower())))
            else:
                noisy_msg += c
        return noisy_msg
def CheckConsensus(message):


    print("PBFT algorithm is running...")
    global start_time
    start_time = time.time()
    # choose a random index from the list
    index = random.randint(0, len(msgNumber) - 1)
    msgNumber[index] = 1
    for i,node in enumerate(NetworkConfig.network.nodes):
        print("Sending preprepare message from node "+str(node.ports), flush=True)
        if(msgNumber[i] == 0):
            node.broadcastMessage("Broadcast",node.ports,i+1)
        else:
            msg = addNoise("Broadcast", 0.1, 0)
            node.broadcastMessage(msg, node.ports, i + 1)
            print("msg after noise " + str(msg))
    for i,node in enumerate(NetworkConfig.network.nodes):

        stop_event = False  # This event will be used to signal the thread to stop
        if (msgNumber[i + NetworkConfig.num_nodes ] == 0):
            thread = threading.Thread(target=node.checkMessagesBroadcast, args=(stop_event,i + 1 + NetworkConfig.num_nodes,"Prepare"))
        else:
            msg = addNoise("Prepare", 0.1, 0)
            thread = threading.Thread(target=node.checkMessagesBroadcast,args=(stop_event, i + 1 + NetworkConfig.num_nodes, "Prepare"))
            print("msg after noise " + str(msg))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    for i,node in enumerate(NetworkConfig.network.nodes):
        stop_event = False  # This event will be used to signal the thread to stop
        if (msgNumber[i + NetworkConfig.num_nodes * 2] == 0):
            thread = threading.Thread(target=node.checkMessagesPrepare,args=(stop_event, i + 1 + NetworkConfig.num_nodes * 2, "Commit"))
        else:
            msg = addNoise("Commit", 0.1, 0)
            thread = threading.Thread(target=node.checkMessagesPrepare,args=(stop_event, i + 1 + NetworkConfig.num_nodes * 2, msg))
            print("msg after noise "+str(msg))
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