
import queue

import zmq
import threading

import NetworkConfig


class NodeClass:
  currentSendingNode =None
  broadcastCounter = 0

  #messageRCVD = {}
  def __init__(self,host,ports,neighbors,maxQueueCapacity):
    self.host = host
    self.ports = ports
    self.neighbors = neighbors
    self.isValidBroadcast = False
    self.isValidPrepare = False
    self.sending_socket = None
    self.inputNodesList = []
    self.isValidBroadcast = False
    self.isValidPrepare = False
    self.maxQueueCapacity = maxQueueCapacity
    self.nodeStorageList = []
    self.mutexReadWriteInputNodes = threading.Lock
    self.state = {"1":" "}



    self.messageRCVD ={}
    self.messageRCVD = {}
    self.messagesBroadcastReceived = {}
    self.messagesPrepareReceived = {}
    self.messagesCommitReceived = {}
    global currentSendingNode
    global semaphores

    self.messageQueue = queue.Queue(maxsize=maxQueueCapacity)
    self.sendThread = threading.Thread(target=self.sendMessages)
    self.sendThread.daemon = True
    self.sendThread.start()

    self.messagesDropped = []
    self.broadcastNbr = [[[],0] for _ in range(NetworkConfig.num_nodes * 3)]
# [[63237,],[],[],[]]


  def getNeighbors(self,i):
      return self.neighbors[i]

  def zmqRead(self):

       context = zmq.Context()
       socket = context.socket(zmq.REP)

       socket.bind("tcp://*:"+str(self.ports))
       while True:
            #  Wait for next request from client

             message = socket.recv()
             socket.send_string("rcvd on " + str(self.ports))
             #socket.send(message.decode())
             self.messageRCVD[message.decode()] = message.decode()
             self.zmqBroadCast(message.decode(),self.currentSendingNode)
             #self.currentSendingNode = None
             #socket.close()

             break


  def zmqRead2(self):


      context = zmq.Context()
      socket = context.socket(zmq.REP)

      socket.bind("tcp://*:" + str(self.ports))
      while True:

          #  Wait for next request from client

          message = socket.recv()
          data = eval(message.decode())


          socket.send_string("received " + str(self.ports))
          if not (data[1] in self.messageRCVD.keys()):



            for semaphore in NetworkConfig.network.semaphores:
                    # if semaphore.Nodes == [self.ports, neighborPort] or semaphore.Nodes == [neighborPort,self.ports]:
                    if id(semaphore) == data[3]:

                        semaphore.Semaphore.release()

            NetworkConfig.TotalBitsNumberOfMessages = NetworkConfig.TotalBitsNumberOfMessages + len(data[0])
            NetworkConfig.TotalNumberOfMessages = NetworkConfig.TotalNumberOfMessages + 1

            # this if statement check if the dropMessagesWhenQIsFull = True to drop the msgs
            if NetworkConfig.dropMessagesWhenQIsFull:

                # this if statement check if the Q is full so we drop the packet
                    if not self.messageQueue.full():


                        if str(data[0]) == "Broadcast":
                            self.messageRCVD[data[1]] = data[0]
                            self.messagesBroadcastReceived[data[1]] = data[0]
                        elif str(data[0]) == "Prepare":
                            self.messageRCVD[data[1]] = data[0]
                            self.messagesPrepareReceived[data[1]] = data[0]
                        elif str(data[0]) == "Commit":
                            self.messageRCVD[data[1]] = data[0]
                            self.messagesCommitReceived[data[1]] = data[0]
                        self.messageQueue.put(data)
                        self.nodeStorageList.append(data)

                    else:
                        self.messagesDropped.append(data[0])
                        NetworkConfig.NumberOfMessagesDropped = NetworkConfig.NumberOfMessagesDropped + 1
                        NetworkConfig.BitsNumberOfMessagesDropped = NetworkConfig.BitsNumberOfMessagesDropped + len(data[0])
            else:

                NetworkConfig.TotalBitsNumberOfMessages = NetworkConfig.TotalBitsNumberOfMessages + len(data[0])
                NetworkConfig.TotalNumberOfMessages = NetworkConfig.TotalNumberOfMessages + 1

                if str(data[0]) == "Broadcast":
                    self.messageRCVD[data[1]] = data[0]
                    self.messagesBroadcastReceived[data[1]] = data[0]
                elif str(data[0]) == "Prepare":
                    self.messageRCVD[data[1]] = data[0]
                    self.messagesPrepareReceived[data[1]] = data[0]
                elif str(data[0]) == "Commit":
                    self.messageRCVD[data[1]] = data[0]
                    self.messagesCommitReceived[data[1]] = data[0]
                self.messageRCVD[data[1]] = data[0]
                self.messageQueue.put(data)
                self.nodeStorageList.append(data)
                #self.nodeStorageList.append(threading.current_thread())

  def sendMessages(self):
      while True:
          [message,broadcastNbr,currentSendingNode1,sem_id] = self.messageQueue.get()
          self.zmqBroadCast(message, currentSendingNode1,broadcastNbr)


  def broadcastMessage(self,message,currentSendingNode, broadcastNbr):
          self.messageQueue.put([message,broadcastNbr,currentSendingNode,0])


  def zmqReadrunning(self):
      context = zmq.Context()
      socket = context.socket(zmq.REP)
      socket.bind("tcp://*:" + str(self.ports))
      while True:


          message = socket.recv()



          socket.send_string("received " + str(self.ports))
          self.messageRCVD[message.decode()] = message.decode()

          self.zmqBroadCast(message.decode(), self.currentSendingNode)
          self.currentSendingNode = None


  def zmqBroadCast(self, data, currentSendingNode1,broadcastNbr):
    context = zmq.Context()

    if self.broadcastNbr[broadcastNbr-1][1] != 0:

        return
    else:
        self.broadcastNbr[broadcastNbr-1][1] = self.broadcastNbr[broadcastNbr-1][1] + 1

    i = 0
    try:
        for neighbor in self.neighbors:


            NeighboringNode0 = NetworkConfig.Network.getNodeByPort(NetworkConfig.network, node=neighbor)
            if neighbor in self.broadcastNbr[broadcastNbr-1][0]:
               Nothing =0



            elif neighbor not in self.broadcastNbr[broadcastNbr-1][0]:

                if neighbor != currentSendingNode1 and currentSendingNode1 not in NeighboringNode0.broadcastNbr[broadcastNbr-1][0] :



                    NeighboringNode = NetworkConfig.Network.getNodeByPort(NetworkConfig.network, node=neighbor)

                    if NeighboringNode == -1:
                        print("node was not found")
                        exit(1)

                    NeighboringNode.currentSendingNode = self.ports



                    NeighboringNode.broadcastNbr[broadcastNbr-1][0].append(self.ports)
                    sem_id = 0

                    for semaphore in NetworkConfig.network.semaphores:
                            if semaphore.Nodes == [self.ports, neighbor] or semaphore.Nodes == [neighbor,
                                                                                                    self.ports]:


                                semaphore.Semaphore.acquire()

                                sem_id = id(semaphore)



                    self.sending_socket = context.socket(zmq.REQ)
                    self.sending_socket.connect("tcp://localhost:" + str(neighbor))



                    message = [data, broadcastNbr,self.ports, sem_id]
                    self.sending_socket.send_string(str(message))

                    # socket.send(bytes(data))

                    # self.sending_socket = socket
                    i = i + 1
                    t = threading.Thread(target=self.zmqRCV, args=(neighbor,))
                    t.daemon = True
                    t.start()

            t2 = threading.Thread(target=self.closeSocket, args=(neighbor,))
            t2.daemon = True
            t2.start()

    except zmq.ZMQError as e:
        print(" errors : " + str(e))
        exit(1)


  def closeSocket(self, port):
        nothing =0


  def zmqRCV(self, port):
    message = self.sending_socket.recv()



  def ToStringBroadcast(self):
    self.messagesBroadcastReceived = dict(sorted(self.messagesBroadcastReceived.items()))
    print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
        self.messagesBroadcastReceived) + "}", flush=True)

  def ToStringPrepare(self):
      self.messagesPrepareReceived = dict(sorted(self.messagesPrepareReceived.items()))
      print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
          self.messagesPrepareReceived) + "}", flush=True)
  def ToStringCommit(self):
      self.messagesCommitReceived = dict(sorted(self.messagesCommitReceived.items()))
      print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
          self.messagesCommitReceived) + "}", flush=True)
  def ListToString(self):
    print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
        self.nodeStorageList) + "}", flush=True)

  def ListToString2(self):
      print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
          self.broadcastNbr) + "}", flush=True)

  def ListToStringRCVD(self):
      print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
              self.messageRCVD) + "}", flush=True)


  def checkMessagesBroadcast(self, stop_event,i,msg):
    while not stop_event:
          if (len(self.messagesBroadcastReceived) >= (NetworkConfig.num_nodes * 2) / 3):
            broadcastMsgNumber = 0

            for nbr in list(self.messagesBroadcastReceived):
                if "Broadcast" in self.messagesBroadcastReceived[nbr]:
                    broadcastMsgNumber += 1

            if (broadcastMsgNumber >= (NetworkConfig.num_nodes * 2) / 3):
                self.state["1"] = "prepare"
                print("Sending prepare message from node " +str(self.ports), flush=True)

                self.broadcastMessage(msg, self.ports, i)

                stop_event = True  # Signal the event to stop the thread
            else:
                print("Pre-prepare messages are less then 2/3 number of nodes in this node: " + str(self.ports), flush=True)
            # The event is set, so the thread stops here


    return

  import threading

  def checkMessagesPrepare(self, stop_event, i,msg):
      while not stop_event:
          if len(self.messagesPrepareReceived) >= (NetworkConfig.num_nodes * 2) / 3:
              prepareMsgNumber = 0

              for nbr in list(self.messagesPrepareReceived):
                  if "Prepare" in self.messagesPrepareReceived[nbr]:
                      prepareMsgNumber += 1
              if prepareMsgNumber >= (NetworkConfig.num_nodes * 2) / 3:
                  self.state["1"] = "commit"
                  print("Sending commit message from node "+str(self.ports), flush=True)
                  self.broadcastMessage(msg, self.ports, i )
                  self.isValidPrepare = True
                  stop_event = True  # Signal the event to stop the thread
              else:
                  print("Prepare messages are less then 2/3 number of nodes in this node: " + str(self.ports),
                        flush=True)
              # The event is set, so the thread stops here

      return


  def checkMessagesCommit(self, stop_event):
      while not stop_event:
          if len(self.messagesCommitReceived) >= (NetworkConfig.num_nodes * 2) / 3:
              commitMsgNumber = 0

              for nbr in list(self.messagesCommitReceived):
                  if "Commit" in self.messagesCommitReceived[nbr]:
                      commitMsgNumber += 1
              if commitMsgNumber >= (NetworkConfig.num_nodes * 2) / 3:
                  #1 = msg id
                  self.state["1"] = "done"

                  stop_event = True  # Signal the event to stop the thread
              else:
                  print("commit messages are less then 2/3 number of nodes in this node: " + str(self.ports),
                        flush=True)

      return

