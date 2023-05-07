# echo-server.py
import hashlib
import json
import socket
import NetworkConfig
import time
import zmq
import threading
from IOTATransaction1 import dict_to_transaction, calculate_transaction_weight, to_dict, IOTATransactionEncoder
from Tangle1 import Tangle
import queue
import iota
from iota import Transaction, TransactionTrytes, TransactionHash, ProposedTransaction, TryteString, Bundle
import random
variable_mutex = threading.Lock()
class Node:

  currentSendingNode = 0
  messageRCVD = 0
  broadcastCounter = 0
  # Generate a random seed.
  myseed = iota.crypto.types.Seed.random()
  # Get an address generator.
  address_generator = iota.crypto.addresses.AddressGenerator(myseed)
  addys = address_generator.get_addresses(1, count=2)
  api = iota.Iota("https://nodes.thetangle.org:443", myseed, local_pow=True)
  LinkLimit = {}
  tangleCounter = 0
  limit = 2
  def __init__(self,host,ports,neighbors,tangle):
    self.host = host
    self.ports = ports
    self.neighbors = neighbors
    #global tangle
    self.tangle = tangle
    global messageRCVD
    self.currentSendingNode
    self.inputNodesList = []
    self.sending_socket = None
    self.sending_socket2 = None
    self.socket = None
    self.LinkLimitationCounter = {}
    self.initialize_linkCounter()
    self.initialize_linkLimitations()
    self.MessageReceivedCounter = 0
    self.status = 1
    self.PendingQ = queue.Queue()
    self.SendingQ = queue.Queue()



  def listen(self):
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          for port1 in self.ports:
              s.bind((self.host, port1))
              s.listen()

  def getTangle(self):
      return self.tangle

  def turnON(self):
      self.checkForPendingQ()
      self.status = 1

  def checkForPendingQ(self):
      if not self.PendingQ.empty():
        while not self.PendingQ.empty():
          try:

               message = self.pendingQ.get()
               if self.LinkLimitationCounter[self.currentSendingNode] < self.LinkLimit[self.currentSendingNode]:
                  # self.LinkLimitationCounter[self.currentSendingNode] = self.LinkLimitationCounter[self.currentSendingNode] + 1
                  self.messageRCVD = message.decode()
                  self.LinkLimitationCounter[self.currentSendingNode] = self.LinkLimitationCounter[self.currentSendingNode] + 1
                  self.MessageReceivedCounter = self.MessageReceivedCounter + 1
                  socket.send_string("rcvd on " + str(self.ports))
                  if (self.tangle.confirmMessage(self.messageRCVD)):
                      txs = json.loads(self.messageRCVD)
                      transaction = dict_to_transaction(txs)
                      if transaction_exists(transaction, self.tangle):
                          print("already existing in this dag")
                      else:
                          start_time = time.time()
                          if transaction.validate():

                              txhash = transaction.get_transaction_hash()
                              transaction.calculate_weight(txhash)
                              if self.tangle.select_tips(5) is not None:
                                  trunk_hash, branch_hash = self.tangle.select_tips(5)
                                  transaction.setTrunk(trunk_hash)
                                  transaction.setBranch(branch_hash)
                                  trunk_tx_hash = transaction.trunk_transaction_hash
                                  branch_tx_hash = transaction.branch_transaction_hash

                                  self.tangle.add_transaction1(transaction)
                                  self.tangleCounter = self.tangleCounter + 1
                                  end_time = time.time()
                                  convergence_time = end_time - start_time
                                  # print("\n Convergence time on " + str(self.ports) + ":", convergence_time)
                                  # sender = socket.getsockopt(zmq.RCVPROTONAME).split("://")[1]
                                  sender = socket.getsockopt(zmq.SNDHWM)
                                  print(" sender is " + str(sender) + " current sending node is " + str(
                                      self.currentSendingNode))
                                  time.sleep(10)
                                  self.MessageReceivedCounter = self.MessageReceivedCounter - 1
                                  self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)


                              else:
                                  transaction_hash = transaction.get_transaction_hash()
                                  # self.tangle.add_transaction(transaction_hash, calculate_transaction_weight(transaction),
                                  #                             {1})
                                  self.tangle.add_transaction1(transaction)
                                  self.tangleCounter = self.tangleCounter + 1
                                  #sender = socket.getsockopt(zmq.RCVPROTONAME).split("://")[1]
                                  print(" sender is " + sender + " current sending node is " + self.currentSendingNode)
                                  self.MessageReceivedCounter = self.MessageReceivedCounter - 1
                                  self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)

                          else:
                              print('Transaction is not yet confirmed.', flush=True)
               else:
                  print("link is at capacity, Link nbre is:" + str(self.currentSendingNode))
          except KeyError as e:
              print(" errors on " + str(self.ports) + " : " + str(e))
              exit(1)
        print("All pending messages are treated!")
  def turnOFF(self):
      self.status = 0
  def readData(self):

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("after socket")
        for port1 in self.ports:
          s.bind((self.host, port1))
          s.listen()
          conn, addr = s.accept()
          with conn:
            print(f"Connected by {addr}")
            while True:
             data2 = conn.recv(1024).decode()
             print(data2)
             messageRCV = "Message is received"
             conn.sendall(messageRCV.encode())
             conn.close()
            if not data2:
             break

  def initialize_linkCounter(self):
      for neighbor in self.neighbors:
          self.LinkLimitationCounter[neighbor] = 0
          #print("Port "+str(self.ports)+"LinkLimitationCounter["+str(neighbor)+"] = "+str(self.LinkLimitationCounter[neighbor]))
      self.LinkLimitationCounter[0] = 0
      self.LinkLimitationCounter[self.ports] = 0

  def initialize_linkLimitations(self):
        for neighbor in self.neighbors:
            self.LinkLimit[neighbor] = self.limit
        self.LinkLimit[0] = self.limit
  def BroadCastData(self,data):
      for p in self.ports:
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
              s.connect((self.host, p))
              s.sendall(data.encode())
              data2 = s.recv(1024).decode()
              print(f"Received {data2!r} from {p!r}")


  def sendData(self,data3,port):

      if port not in self.ports:
          print("node is out of range!")
          return

      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.connect((self.host, port))
          s.sendall(data3.encode())
          data4 = s.recv(1024).decode()

  def zmqRead(self):
       try:
           context = zmq.Context()
           self.socket = context.socket(zmq.REP)

           self.socket.bind("tcp://*:"+str(self.ports))
           while True:

                     message = self.socket.recv()
                     self.socket.send_string("ACK : rcvd on " + str(self.ports))
                     if self.status == 0:
                         self.PendingQ.put(message)
                         print("This node is off " + str(self.ports))
                     print("Result on "+str(self.ports)+"  with sender& = " + str(self.currentSendingNode))
                     self.MessageReceivedCounter = self.MessageReceivedCounter + 1
                     t = threading.Thread(target=self.processMessages, args=(message,self.currentSendingNode,))
                     t.daemon = True
                     t.start()
                     '''
                     try:
                             if self.LinkLimitationCounter[self.currentSendingNode] < self.LinkLimit[self.currentSendingNode]:
                                 #self.LinkLimitationCounter[self.currentSendingNode] = self.LinkLimitationCounter[self.currentSendingNode] + 1
                                 self.messageRCVD = message.decode()
                                 NetworkConfig.network.ReStartThreadingOnOne(self.ports)
                                 self.LinkLimitationCounter[self.currentSendingNode] = self.LinkLimitationCounter[self.currentSendingNode] + 1
                                 self.MessageReceivedCounter = self.MessageReceivedCounter + 1
                                 socket.send_string("ACK : rcvd on " + str(self.ports))
                                 if(self.tangle.confirmMessage(self.messageRCVD)):
                                  txs = json.loads(self.messageRCVD)
                                  transaction = dict_to_transaction(txs)
                                  if transaction_exists(transaction, self.tangle):
                                      print("already existing in this dag")
                                  else:
                                      start_time = time.time()
                                      if transaction.validate():

                                       txhash = transaction.get_transaction_hash()
                                       transaction.calculate_weight(txhash)
                                       if self.tangle.select_tips(5) is not None:
                                        trunk_hash, branch_hash = self.tangle.select_tips(5)
                                        transaction.setTrunk(trunk_hash)
                                        transaction.setBranch(branch_hash)
                                        trunk_tx_hash = transaction.trunk_transaction_hash
                                        branch_tx_hash = transaction.branch_transaction_hash

                                        self.tangle.add_transaction1(transaction)
                                        self.tangleCounter = self.tangleCounter + 1
                                        end_time = time.time()
                                        convergence_time = end_time - start_time
                                        #print("\n Convergence time on " + str(self.ports) + ":", convergence_time)
                                       # sender = socket.getsockopt(zmq.RCVPROTONAME).split("://")[1]
                                        sender = socket.getsockopt(zmq.SNDHWM)
                                        print(" sender is " + str(sender) + " current sending node is " + str(self.currentSendingNode))
                                        time.sleep(1)
                                        self.MessageReceivedCounter = self.MessageReceivedCounter - 1
                                        self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)


                                       else:
                                           transaction_hash = transaction.get_transaction_hash()
                                          # self.tangle.add_transaction(transaction_hash, calculate_transaction_weight(transaction),
                                          #                             {1})
                                           self.tangle.add_transaction1(transaction)
                                           self.tangleCounter = self.tangleCounter + 1
                                           sender = socket.getsockopt(zmq.RCVPROTONAME).split("://")[1]
                                           print(" sender is " + sender + " current sending node is " + self.currentSendingNode)
                                           self.MessageReceivedCounter = self.MessageReceivedCounter - 1
                                           self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)
                                           
                                      else:
                                         print('Transaction is not yet confirmed.', flush=True)
                             else:
                                 print("link is at capacity, Link nbre is:"+ str(self.currentSendingNode))
                                
                     except KeyError as e:
                                 print(" errors on "+ str(self.ports) +" : " + str(e))
                                 exit(1)
                     '''
       except zmq.ZMQError as e:
         print(" errors in read mssg"+ str(self.ports) +": " +str(e.args) + str(e.errno) + str(e.strerror))
         #exit(1)

  def processMessages(self,message,port):
    start_time = time.time()
    try:
        print("je suis là ,person that sent me is : "+str(port)+"\n")
        if len(self.inputNodesList) != 0:
            sentby = port
        else:
            sentby = port

        if NetworkConfig.network.droppackets == 1:
           if self.LinkLimitationCounter[sentby] < self.LinkLimit[sentby]:
            self.iotaAlgorithmProcess(message,sentby)
           else:
            print("Link is at capacity"+ str(self.LinkLimitationCounter[port])+", will try to retransmit after 5 seconds:" + str(port) + "on " + str(self.ports) )
            #time.sleep(10)
            #t = threading.Thread(target=self.processMessages, args=(message, port,))
            #t.daemon = True
            #t.start()
        else:
          self.iotaAlgorithmProcess(message, sentby)
            #return
    except KeyError as e:
        print("errors in process message on " + str(self.ports) + " : " + str(e))

    end_time = time.time()
    convergence_time = end_time - start_time
    print(" convergence time for "+ str(self.ports) + " for message " + str(message) + " is "+ str(convergence_time))


  def iotaAlgorithmProcess(self,message,sentby):

      self.messageRCVD = message.decode()

      print("Incrementing " + str(sentby) + " on " + str(self.ports))
      self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] + 1
      if self.LinkLimitationCounter[sentby] == 2:
          print("this node has reached capacity, it should decrement on " + str(self.ports) + " by  " + str(sentby))

      if (self.tangle.confirmMessage(self.messageRCVD)):
          txs = json.loads(self.messageRCVD)
          transaction = dict_to_transaction(txs)
          if transaction_exists(transaction, self.tangle):
              print("already existing in this dag")
              self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] - 1
          else:

              if transaction.validate():
                  print("valid")
                  txhash = transaction.get_transaction_hash()
                  transaction.calculate_weight(txhash)
                  if self.tangle.select_tips(5) is not None:
                      trunk_hash, branch_hash = self.tangle.select_tips(5)
                      transaction.setTrunk(trunk_hash)
                      transaction.setBranch(branch_hash)
                      trunk_tx_hash = transaction.trunk_transaction_hash
                      branch_tx_hash = transaction.branch_transaction_hash

                      self.tangle.add_transaction1(transaction)
                      self.tangleCounter = self.tangleCounter + 1

                      print("decrementing " + str(sentby) + " on " + str(self.ports))

                      self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)


                  else:
                      transaction_hash = transaction.get_transaction_hash()
                      # self.tangle.add_transaction(transaction_hash, calculate_transaction_weight(transaction),
                      #                             {1})
                      self.tangle.add_transaction1(transaction)
                      self.tangleCounter = self.tangleCounter + 1
                      sender = self.socket.getsockopt(zmq.RCVPROTONAME).split("://")[1]
                      print(" sender is " + sender + " current sending node is " + self.currentSendingNode)
                      print("decrementing " + str(sentby) + " on " + str(self.ports))
                      self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] - 1
                      self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)

              else:
                  print('Transaction is not yet confirmed.', flush=True)
                  self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] - 1
                  return
              self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] - 1
      else:
          self.LinkLimitationCounter[sentby] = self.LinkLimitationCounter[sentby] - 1
          print('Transaction is not yet confirmed.', flush=True)
  def zmqRead2(self):

     #print("Listening1")
     context = zmq.Context()
     socket = context.socket(zmq.REP)
     #print("Listening2")
     socket.bind("tcp://*:"+str(self.ports))
     while True:

          #  Wait for next request from client
           print("Listening3............", flush=True)
           #time.sleep(3)
           #print("awake...........")
           message = socket.recv()
           #self.messageRCVD = message.decode()
           self.messageRCVD = message
           print(f"Received request: {message}", flush=True)
           if(self.tangle.confirmMessage(messageRCVD)):
               print(f"message confirmed, adding to tangle, and broadcasting", flush=True)
               self.tangle.add_transaction(messageRCVD, {1})

               self.zmqBroadCast(message.decode(), self.currentSendingNode)

           break

  def zmqRead1(self):

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        for port1 in self.ports:
                socket.connect("tcp://*:"+str(self.ports))
        #    while True:
                #  Wait for next request from client
                message = socket.recv()

                print(f"Received request: {message}")
                #  Send reply back to client
                socket.send(b"World")
         #       break

  def zmqWrite(self,data,port,sendingPort):
    if port not in self.neighbors:
        print("node is out of range!")
        return
    context = zmq.Context()
    self.broadcastCounter = 0
    try:

            self.currentSendingNode = sendingPort
            self.sending_socket = context.socket(zmq.REQ)
            self.sending_socket.connect("tcp://127.0.0.1:"+str(port))
            NeighboringNode = NetworkConfig.network.getNodeByPort(node=port)
            if NeighboringNode == -1:
                print("node was not found")
                exit(1)
            #NeighboringNode.currentSendingNode = self.ports
            #NeighboringNode.inputNodesList.append(self.ports)
            # Convert dictionary to JSON string
            json_string = json.dumps(data, cls=IOTATransactionEncoder)
            # Set up poller



            print("Sent", flush=True)
            self.sending_socket.send_string(json_string)
            t8 = threading.Thread(target=self.zmqRCV, args=(json_string,))
            t8.daemon = True
            t8.start()

#          return
    except zmq.ZMQError as e:
        print(" errors on write: "+ str(e))
        #exit(1)



  def zmqRCV(self,messages):
      poller = zmq.Poller()
      timeout = 500000000
      retries = 5
      #time.sleep(5)
      try:
       message = self.sending_socket.recv()
       print("message")
      except zmq.ZMQError as e:
        print(" errors on rcv on : "+ str(self.ports) + str(e.__traceback__) +  str(e.strerror) )



  def zmqBroadCast(self, data,currentSendingNode1):
    context = zmq.Context()
    if self.broadcastCounter > 5:
        print("this node already sent her own broadcast, It will not send another!")
        return
    else:
        self.broadcastCounter = self.broadcastCounter + 1
    i = 0

    try:
        for neighbor in self.neighbors:

           print("neighbor :"+ str(neighbor) + " in input nodes list :" + str(self.inputNodesList))
           if neighbor in self.inputNodesList:
                    print("\nThis is the sender we will not send it back1 and the neighbor i am attempting to reach out to is"+ str(neighbor), flush=True)
           elif neighbor not in self.inputNodesList:

             if neighbor != currentSendingNode1:
              self.sending_socket = context.socket(zmq.REQ)
              self.sending_socket.connect("tcp://localhost:"+str(neighbor))
              print(" I am "+ str(self.ports)+"currentSendingNode : "+ str(self.currentSendingNode) + ",/n currentsendingNode1 : " + str(currentSendingNode1))
              print("broadcast from" + str(self.ports) + " ->" + str(neighbor), flush=True)
              # Convert the transaction to trytes
              #tx_trytes = data.as_tryte_string()
              #self.currentSendingNode = neighbor
              # Convert the trytes to bytes
              #tx_bytes = self.trytes_to_bytes(tx_trytes)
              #socket.send(tx_bytes)
              NeighboringNode  = NetworkConfig.network.getNodeByPort(node=neighbor)
              if NeighboringNode == -1:
                  print("node was not found")
                  exit(1)
              NeighboringNode.currentSendingNode=self.ports
              NeighboringNode.inputNodesList.append(self.ports)
              json_string = json.dumps(data, cls=IOTATransactionEncoder)
              self.sending_socket.send_string(json_string)
              print("Sent Broadcast", flush=True)
              i = i + 1
              t = threading.Thread(target=self.zmqRCV, args=(json_string,))
              t.daemon = True
              t.start()



           t2 = threading.Thread(target=self.closeSocket, args=(neighbor,))
           t2.daemon = True
           t2.start()


    except zmq.ZMQError as e:
     print(" errors on broadcast on : "+ str(self.ports) + str(e))
     exit(1)


  def closeSocket(self,port):

#      if not self.sending_socket.closed:
   #  time.sleep(60)
    # self.sending_socket.close()
     print("not closing this socket:)")





  def zmqWrite1(self,data,port,sendingPort):
    if port not in self.neighbors:
        print("node is out of range!")
        #            return
    variable_mutex.acquire()
    context = zmq.Context()
    try:
     #  Socket to talk to server
     #print(f"Connecting to hello world server from {sendingPort}")
        self.currentSendingNode = sendingPort
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:"+str(port))
        # Convert dictionary to JSON string
        json_string = json.dumps(data)
        socket.send_string(json_string)
        print("Sent", flush=True)
    except zmq.ZMQError as e:
        print(" errors : "+ str(e))
    finally:
        # release the mutex to allow other threads to access the object variable
        variable_mutex.release()


  def zmqBroadCast1(self, data,currentSendingNode1):
    context = zmq.Context()

    #  Socket to talk to server
    #print("Connecting to hello world server…")
    i = 0
    # create a mutex to synchronize access to the object variable
    variable_mutex = threading.Lock()
    # acquire the mutex to access the object variable
    variable_mutex.acquire()
    try:
        for neighbor in self.neighbors:
         if neighbor is not currentSendingNode1:
          socket = context.socket(zmq.REQ)
          socket.connect("tcp://localhost:"+str(neighbor))
          print("broadcast from" + str(self.ports) + " ->" +str(neighbor), flush=True)
          self.currentSendingNode = neighbor
          json_string = json.dumps(data)
          socket.send_string(json_string)

         # socket.send(bytes(data))
          print("Sent Broadcast", flush=True)
          i = i + 1
         else:
            print("This is the sender we will not send it back", flush=True)

    except zmq.ZMQError as e:
     print(" errors : " + e)

    finally:
     # release the mutex to allow other threads to access the object variable
     variable_mutex.release()

  def ToString(self):
    print(" Node : { port:" + str(self.ports)+ " ,"
                                                "Message Received Counter : "+ str(self.MessageReceivedCounter) + " "
                                               "Neighbors : "+ str(self.neighbors) + " "
                                                                                "CurrentData : "+ str(self.messageRCVD) + ""
                                                                                                                             "Current Tangle Index : "+ str(self.tangleCounter) + ""
                                                                                                                                                                                  "\n"
                                                                                                                                                                                  
                                                                                                                                                                       
                                                                                                                     #+ "Tangle "+ self.tangle.to_string()+"  "
                                                                                                                                                          
                                                                                                                                                          "}" , flush=True)


  def trytes_to_bytes(trytes):
    # The IOTA tryte alphabet
    TRYTE_ALPHABET = '9ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Convert each tryte to a byte
    bytes_ = []
    for i in range(0, len(trytes), 2):
        tryte_pair = trytes[i:i + 2]
        byte = TRYTE_ALPHABET.index(tryte_pair[0]) + TRYTE_ALPHABET.index(tryte_pair[1]) * 27
        bytes_.append(byte)

    return bytes(bytes_)

def transaction_exists(transaction, dag : Tangle):
    for t in dag.transactions:
        if t.bundle_hash == transaction.bundle_hash:
            return True
    return False
