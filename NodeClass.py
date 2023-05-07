# echo-server.py
import random
import socket
import time
import zmq
import threading
class NodeClass:
  currentSendingNode =None
  #messageRCVD = {}
  def __init__(self,host,ports,neighbors):
    self.host = host
    self.ports = ports
    self.neighbors = neighbors
    self.isValidBroadcast = False
    self.isValidPrepare = False




    self.messageRCVD ={}
    global currentSendingNode


  def getNeighbors(self,i):
      return self.neighbors[i]

  def listen(self):
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          for port1 in self.ports:
              s.bind((self.host, port1))
              s.listen()




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
        #  print(f"Received {data4!r} from {p!r}")



  def zmqRead(self, arg):

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
             #socket.send(message.decode())
             self.messageRCVD[message.decode()] = message.decode()
             print(f"Received request: {message.decode()}\n", flush=True)
             self.zmqBroadCast(message.decode(),self.currentSendingNode)
             self.currentSendingNode = None
             #socket.close()

             break

  def zmqRead2(self,arg):

      # print("Listening1")
      context = zmq.Context()
      socket = context.socket(zmq.REP)
      # print("Listening2")
      socket.bind("tcp://*:" + str(self.ports))
      while True:
          #  Wait for next request from client
          print(f"Listeningfrom2....{self.ports}", flush=True)
          # time.sleep(3)
          # print("awake...........")
          message = socket.recv()
          self.messageRCVD[message.decode()] = message.decode()
          print(f"I'm {self.ports} I Received request: {message.decode()}\n", flush=True)
          self.zmqBroadCast(message.decode(), self.currentSendingNode)
          self.currentSendingNode = None
          #socket.close()

          #break





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

      #  Socket to talk to server
      #print(f"Connecting to hello world server from {sendingPort}")
      self.currentSendingNode = sendingPort
      socket = context.socket(zmq.REQ)
      socket.connect("tcp://localhost:"+str(port))
      #  Do 10 requests, waiting each time for a response
      #for request in range(10):
      #print(f"Sending request 1 …")
      socket.send(data.encode())
      print("Sent", flush=True)

      return

  def zmq_BroadCast(self, data,currentSendingNode1):
      context = zmq.Context()
      i = 0
      if self.currentSendingNode == None: self.currentSendingNode = self.ports
      for neighbor in self.neighbors:
       if neighbor is not currentSendingNode1:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(neighbor))
      #  Do 10 requests, waiting each time for a response
      # for request in range(10):
        print("broadcast from" + str(self.ports) + " ->" +str(neighbor), flush=True)
       # self.currentSendingNode = neighbor
        socket.send(data.encode())
        print("Sent Broadcast", flush=True)
        i = i + 1

      #else:
          #print("This is the sender we will not send it back", flush=True)

  def zmqBroadCast(self, data, current_sending_node=None):
      context = zmq.Context()
      if current_sending_node is None:
          current_sending_node = self.ports
      for neighbor in self.neighbors:
          if neighbor != current_sending_node:
              socket = context.socket(zmq.REQ)
              socket.connect(f"tcp://localhost:{neighbor}")
              print(f"Broadcast from {self.ports} -> {neighbor}", flush=True)
              socket.send(data.encode())
              print("Sent broadcast", flush=True)
              socket.close()

      # Update the current sending node to the last neighbor that was sent to
      self.currentSendingNode = neighbor



  def ToString(self):
      print(" Node : { port:" + str(self.ports)+ " ,"
                                                 "Neighbors : "+ str(self.neighbors) + " "
                                                                                  "CurrentData : "+ str(self.messageRCVD) + ""
                                                                                                                       "}", flush=True)

  def PBFT(self,message):
      random.choice( self.neighbors)
      self.zmqBroadCast(message.decode(), self)



  def zmqBroadCast2(self, data,currentSendingNode1):
      context = zmq.Context()
      self.currentSendingNode = None
      #  Socket to talk to server
      #print("Connecting to hello world server…")
      i = 0
      for neighbor in self.neighbors:

       if neighbor is not currentSendingNode1:
          socket = context.socket(zmq.REQ)
          socket.connect("tcp://localhost:"+str(neighbor))
          #  Do 10 requests, waiting each time for a response
          # for request in range(10):
          print("broadcast from" + str(self.ports) + " ->" +str(neighbor), flush=True)
          self.currentSendingNode = neighbor
          socket.send(data.encode())
          print("Sent Broadcast", flush=True)
          i = i + 1
          # Close the socket
          socket.close()
          #context.term()
       else:
          print("This is the sender we will not send it back", flush=True)

  def zmqBroadCast4(self, data,currentSendingNode1):
      context = zmq.Context()
      self.currentSendingNode = None
      #  Socket to talk to server
      #print("Connecting to hello world server…")
      i = 0
      for neighbor in self.neighbors:

       if neighbor is not currentSendingNode1:
          socket = context.socket(zmq.REQ)
          socket.connect("tcp://localhost:"+str(neighbor))
          #  Do 10 requests, waiting each time for a response
          # for request in range(10):
          print("broadcast from" + str(self.ports) + " ->" +str(neighbor), flush=True)
          self.currentSendingNode = neighbor
          socket.send(data.encode())
          print("Sent Broadcast", flush=True)
          i = i + 1
          # Close the socket
          socket.close()
          #context.term()
       else:
          print("This is the sender we will not send it back", flush=True)



  def PBFT(self, data, currentSendingNode):
        context = zmq.Context()
        sockets = {}

        # Create a REQ socket for each neighbor (except the current sender)
        for neighbor in self.neighbors:
            if neighbor != currentSendingNode:
                socket = context.socket(zmq.REQ)
                socket.connect("tcp://localhost:" + str(neighbor))
                sockets[neighbor] = socket

        # Send the message to all connected neighbors
        print(f"Node {self.ports} broadcasting message: {data}")
        for neighbor, socket in sockets.items():
            socket.send(data.encode())
            print(f"Node {self.ports} sent message to neighbor {neighbor}")

        # Close the sockets
        for socket in sockets.values():
            socket.close()
        context.term()

        def zmqBroadCast3(self, data, currentSendingNode):
            context = zmq.Context()
            sockets = {}

            # Create a REQ socket for each neighbor (except the current sender)
            for neighbor in self.neighbors:
                if neighbor != currentSendingNode:
                    socket = context.socket(zmq.REQ)
                    socket.connect("tcp://localhost:" + str(neighbor))
                    sockets[neighbor] = socket

            # Send the message to all connected neighbors
            print(f"Node {self.ports} broadcasting message: {data}")
            for neighbor, socket in sockets.items():
                socket.send(data.encode())
                print(f"Node {self.ports} sent message to neighbor {neighbor}")

            # Close the sockets
            for socket in sockets.values():
                socket.close()
            context.term()


  def checkMessageBroadcast(self):
      broadcastMsgNumber = 0
      for msg in self.messageRCVD:
          print(self.messageRCVD[msg])
          if "broadcast" in self.messageRCVD[msg]:
              print(f"{self.messageRCVD[msg]} contains Broadcast")
              broadcastMsgNumber += 1

      if (broadcastMsgNumber>4):
          self.messageRCVD.clear()
          return True
      else:
          self.messageRCVD.clear()
          return False




  def checkMessagesPrepare(self):
      prepareMsgNumber = 0
      for msg in self.messageRCVD:
          print(msg)
          if "prepare" in msg:
              print(f"{msg} is in prep")
              prepareMsgNumber += 1

      if (prepareMsgNumber > 4):
          self.messageRCVD.clear()
          return True
      else:
          self.messageRCVD.clear()
          return False












  def checkMessagesBroadcast(self):
     return True