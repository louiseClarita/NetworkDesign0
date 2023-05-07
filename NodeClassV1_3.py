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



    self.messageRCVD ={}
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
             self.currentSendingNode = None
             #socket.close()

             break


  def zmqRead2(self):

      # print("Listening1")
      context = zmq.Context()
      socket = context.socket(zmq.REP)
      # print("Listening2")
      socket.bind("tcp://*:" + str(self.ports))
      while True:
          #  Wait for next request from client
          print(f"Listeningfrom2....{self.ports}", flush=True)
          message = socket.recv()
          data = eval(message.decode())
          print("this is the messagee receved:: "+ str(data),flush=True)
          socket.send_string("received " + str(self.ports))
          print("this is the messagee i want to put on Q:: " + str(data[0]) +" "+str(data[1]), flush=True)
          self.messageRCVD[data[1]] = data[0]
          self.messageQueue.put(data)
          print(f"I'm {self.ports} I Received request: {message.decode()}\n", flush=True)
          #self.zmqBroadCast(message.decode(), self.currentSendingNode)
          #self.currentSendingNode = None
          #socket.close()

          #break

  def sendMessages(self):
      while True:
          [message,broadcastNbr] = self.messageQueue.get()
          self.zmqBroadCast(message, self.currentSendingNode,broadcastNbr)
          self.currentSendingNode = None

  def broadcastMessage(self,message,currentSendingNode,broadcastNbr):
          self.currentSendingNode = currentSendingNode
          self.messageQueue.put([message,broadcastNbr])


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

            if neighbor in self.broadcastNbr[broadcastNbr-1][0]:
                print(
                    "\nThis is the sender we will not send it back1 and the neighbor i am attempting to reach out to is" + str(
                        neighbor), flush=True)
            elif neighbor not in self.broadcastNbr[broadcastNbr-1][0]:
                if neighbor != currentSendingNode1:




                    for neighborPort in self.neighbors:

                        for semaphore in NetworkConfig.network.semaphores:
                            if semaphore.Nodes == [self.ports, neighborPort] or semaphore.Nodes == [neighborPort,
                                                                                                    self.ports]:
                                print('we catch the semaphore that we want to lock:')
                                print(str(semaphore))
                                semaphore.Semaphore.acquire()
                                print('Semaphore locked')
                                print('remaining value is: '+ str(semaphore.Semaphore._value))




                    self.sending_socket = context.socket(zmq.REQ)
                    self.sending_socket.connect("tcp://localhost:" + str(neighbor))
                    print(" I am " + str(self.ports) + "currentSendingNode : " + str(
                        self.currentSendingNode) + ",/n currentsendingNode1 : " + str(currentSendingNode1))
                    print("broadcast from" + str(self.ports) + " ->" + str(neighbor), flush=True)
                    NeighboringNode = NetworkConfig.Network.getNodeByPort(NetworkConfig.network,node=neighbor)

                    if NeighboringNode == -1:
                        print("node was not found")
                        exit(1)

                    NeighboringNode.currentSendingNode = self.ports
                    NeighboringNode.broadcastNbr[broadcastNbr-1][0].append(self.ports)
                    #json_string = json.dumps(data)
                    #self.sending_socket.send_string(json_string)
                    message = [data, broadcastNbr]
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

        #      if not self.sending_socket.closed:
        #  time.sleep(60)
        # self.sending_socket.close()
        print("not closing this socket:)")


  def zmqRCV(self, port):
    message = self.sending_socket.recv()
    for neighborPort in self.neighbors:

        for semaphore in NetworkConfig.network.semaphores:
            if semaphore.Nodes == [self.ports, neighborPort] or semaphore.Nodes == [neighborPort,
                                                                                    self.ports]:
                print('we catch the semaphore that we want to unlock:')
                print(str(semaphore))
                semaphore.Semaphore.release()
                print('Semaphore unlocked')
                print('remaining value after the release: ' + str(semaphore.Semaphore._value))
    print(message)


  def ToString(self):
    print("Node: {port: " + str(self.ports) + ", Neighbors: " + str(self.neighbors) + ", CurrentData: " + str(
        self.messageRCVD) + "}", flush=True)


  def checkMessageBroadcast(self):
    return True


  def checkMessagesBroadcast(self):
      broadcastMsgNumber = 0
      for msg in self.messageRCVD:
          print(self.messageRCVD[msg])
          if "Broadcast" in self.messageRCVD[msg]:
              print(f"{self.messageRCVD[msg]} contains Broadcast")
              broadcastMsgNumber += 1

      if (broadcastMsgNumber>4):
          self.messageRCVD.clear()
          self.isValidBroadcast = True
      else:
          self.messageRCVD.clear()
          self.isValidBroadcast = False


  def checkMessagesPrepare(self):
      prepareMsgNumber = 0
      for msg in self.messageRCVD:
          print(msg)
          if "Prepare" in self.messageRCVD[msg]:
              print(f"{msg} is in prepare")
              prepareMsgNumber += 1

      if (prepareMsgNumber > 4):
          self.messageRCVD.clear()
          self.isValidPrepare = True
      else:
          self.messageRCVD.clear()
          self.isValidPrepare = False