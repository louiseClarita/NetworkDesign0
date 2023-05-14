# echo-server.py
import json
import queue
import random
import socket
import time
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



    self.messageRCVD ={}
    self.messagesBroadcastReceived = {}
    self.messagesPrepareReceived = {}
    self.messagesCommitReceived = {}
    global currentSendingNode
    global semaphores

    self.messageQueue = queue.Queue(maxsize=maxQueueCapacity)
    self.sendThread = threading.Thread(target=self.sendMessages)
    self.sendThread.daemon = True
    self.sendThread.start()

    self.broadcastNbr = [[[],0] for _ in range(8*3)]
# [[63237,],[],[],[]]


  def getNeighbors(self,i):
      return self.neighbors[i]

  def zmqRead(self):

       #print("Listening1")
       context = zmq.Context()
       socket = context.socket(zmq.REP)
       #print("Listening2")
       socket.bind("tcp://*:"+str(self.ports))
       while True:
            #  Wait for next request from client
             print("Listening3............", flush=True)

             message = socket.recv()
             socket.send_string("rcvd on " + str(self.ports))
             #socket.send(message.decode())
             self.messageRCVD[message.decode()] = message.decode()
             print(f"Received request: {message.decode()}\n", flush=True)
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
          print(f"Listeningfrom2....{self.ports}", flush=True)
          message = socket.recv()
          data = eval(message.decode())
          print("this is the messagee received:: "+ str(data),flush=True)

          socket.send_string("received " + str(self.ports))
          if not (data[1] in self.messageRCVD.keys()):

            NetworkConfig.TotalBitsNumberOfMessages = NetworkConfig.TotalBitsNumberOfMessages + len(data[0])
            NetworkConfig.TotalNumberOfMessages = NetworkConfig.TotalNumberOfMessages + 1

            for semaphore in NetworkConfig.network.semaphores:
                    # if semaphore.Nodes == [self.ports, neighborPort] or semaphore.Nodes == [neighborPort,self.ports]:
                    if id(semaphore) == data[3]:
                        print('we catch the semaphore that we want to unlock:')
                        print(str(semaphore))
                        semaphore.Semaphore.release()
                        print('remaining value after the release: ' + str(semaphore.Semaphore._value))

            # this if statement check if the dropMessagesWhenQIsFull = True to drop the msgs
            if NetworkConfig.dropMessagesWhenQIsFull:

                # this if statement check if the Q is full so we drop the packet
                    if not self.messageQueue.full():
                        print("this is the messagee i want to put on Q:: " + str(data[0]) + " " + str(data[1]), flush=True)
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
                        print(f"I'm {self.ports} I Received request: {message.decode()}\n", flush=True)
                    else:
                        NetworkConfig.NumberOfMessagesDropped = NetworkConfig.NumberOfMessagesDropped + 1
                        NetworkConfig.BitsNumberOfMessagesDropped = NetworkConfig.BitsNumberOfMessagesDropped + len(data[0])
            else:
                print("this is the messagee i want to put on Q:: " + str(data[0]) + " " + str(data[1]), flush=True)
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
                print(f"I'm {self.ports} I Received request: {message.decode()}\n", flush=True)
  def sendMessages(self):
      while True:
          [message,broadcastNbr,currentSendingNode1,sem_id] = self.messageQueue.get()
          print(f"this is the msg in sendmessages : {message, currentSendingNode1,broadcastNbr}\n", flush=True)
          self.zmqBroadCast(message, currentSendingNode1,broadcastNbr)
          #self.currentSendingNode = None

  def broadcastMessage(self,message,currentSendingNode, broadcastNbr):
          #self.currentSendingNode = currentSendingNode
          print(f"this is the msg in broadcastMessage : {message, currentSendingNode, broadcastNbr}\n", flush=True)
          self.messageQueue.put([message,broadcastNbr,currentSendingNode,0])


  def zmqReadrunning(self):
      context = zmq.Context()
      socket = context.socket(zmq.REP)
      socket.bind("tcp://*:" + str(self.ports))
      while True:
          #  Wait for next request from client
          print(f"Listeningfrom2....{self.ports}", flush=True)
          message = socket.recv()



          socket.send_string("received " + str(self.ports))
          self.messageRCVD[message.decode()] = message.decode()
          print(f"I'm {self.ports} I Received request: {message.decode()}\n", flush=True)
          self.zmqBroadCast(message.decode(), self.currentSendingNode)
          self.currentSendingNode = None


  def zmqBroadCast(self, data, currentSendingNode1,broadcastNbr):
    context = zmq.Context()

    if self.broadcastNbr[broadcastNbr-1][1] != 0:
        print("this node already sent her own broadcast, It will not send another!")
        return
    else:
        self.broadcastNbr[broadcastNbr-1][1] = self.broadcastNbr[broadcastNbr-1][1] + 1

    i = 0
    try:
        for neighbor in self.neighbors:
            print("je suis là\n")
            print("neighbor :" + str(neighbor) + " in input nodes list :" + str(self.broadcastNbr[broadcastNbr-1][0]))
            NeighboringNode0 = NetworkConfig.Network.getNodeByPort(NetworkConfig.network, node=neighbor)
            if neighbor in self.broadcastNbr[broadcastNbr-1][0]:
                print(
                    "\nThis is the sender we will not send it back1 and the neighbor i am attempting to reach out to is" + str(
                        neighbor), flush=True)



            elif neighbor not in self.broadcastNbr[broadcastNbr-1][0]:

                if neighbor != currentSendingNode1 and currentSendingNode1 not in NeighboringNode0.broadcastNbr[broadcastNbr-1][0] :

                    print("2neighbor:::"+ str(neighbor)+" != " +str(currentSendingNode1) +" annd" + str(currentSendingNode1) +" nott in" + str(NeighboringNode0.broadcastNbr[broadcastNbr-1][0]), flush=True)

                    NeighboringNode = NetworkConfig.Network.getNodeByPort(NetworkConfig.network, node=neighbor)

                    if NeighboringNode == -1:
                        print("node was not found")
                        exit(1)

                    NeighboringNode.currentSendingNode = self.ports


                    print("neighbor :" + str(neighbor) + "is not in this list :" + str(
                        self.broadcastNbr[broadcastNbr - 1][0])+ "so i will add it !")
                    NeighboringNode.broadcastNbr[broadcastNbr-1][0].append(self.ports)
                    sem_id = 0

                    for semaphore in NetworkConfig.network.semaphores:
                            if semaphore.Nodes == [self.ports, neighbor] or semaphore.Nodes == [neighbor,
                                                                                                    self.ports]:
                                print('we catch the semaphore that we want to lock:')
                                print(str(semaphore))
                                semaphore.Semaphore.acquire()
                                print('Semaphore locked')
                                print('remaining value is: '+ str(semaphore.Semaphore._value))
                                sem_id = id(semaphore)



                    self.sending_socket = context.socket(zmq.REQ)
                    self.sending_socket.connect("tcp://localhost:" + str(neighbor))
                    print(" I am " + str(self.ports) + "currentSendingNode : " + str(
                        currentSendingNode1) + ",/n currentsendingNode1 : " + str(currentSendingNode1))
                    print("broadcast from" + str(self.ports) + " ->" + str(neighbor), flush=True)


                    message = [data, broadcastNbr,self.ports, sem_id]
                    self.sending_socket.send_string(str(message))

                    # socket.send(bytes(data))
                    print("Sent Broadcast", flush=True)
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
        print("not closing this socket:)")


  def zmqRCV(self, port):
    message = self.sending_socket.recv()
    print(message)


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


  def checkMessagesBroadcast(self, stop_event,i):
    while not stop_event:
          if (len(self.messagesBroadcastReceived) >= 5):
            broadcastMsgNumber = 0

            for nbr in list(self.messagesBroadcastReceived):
                print(self.messagesBroadcastReceived[nbr])
                if "Broadcast" in self.messagesBroadcastReceived[nbr]:
                    print(f"{self.messagesBroadcastReceived[nbr]} contains Broadcast")
                    broadcastMsgNumber += 1

            if (broadcastMsgNumber>2):
                print(f"Prepare{self.ports, i + 8} is Broadcasted",flush=True)
                self.broadcastMessage("Prepare", self.ports, i + 8)
                self.isValidBroadcast = True
                stop_event = True  # Signal the event to stop the thread
            else:
                self.isValidBroadcast = False
            # The event is set, so the thread stops here
    return

  import threading

  def checkMessagesPrepare(self, stop_event,i):
      while not stop_event:
          if len(self.messagesPrepareReceived) >= 5:
              prepareMsgNumber = 0

              for nbr in list(self.messagesPrepareReceived):
                  print(self.messagesPrepareReceived[nbr])
                  if "Prepare" in self.messagesPrepareReceived[nbr]:
                      print(f"{self.messagesPrepareReceived[nbr]} is in Prepare")
                      prepareMsgNumber += 1
              print("listtttt" + str(self.messagesPrepareReceived))
              if prepareMsgNumber > 2:
                  self.broadcastMessage("Commit", self.ports, i + 8 * 2)
                  self.isValidPrepare = True
                  stop_event = True  # Signal the event to stop the thread
              else:
                  self.isValidPrepare = False

      # The event is set, so the thread stops here
      return




