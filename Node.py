# echo-server.py

import socket
import time
import zmq
import threading
class Node:

  def __init__(self,host,ports,neighbors):
    self.host = host
    self.ports = ports
    self.neighbors = neighbors

  def listen(self):
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          for port1 in self.ports:
              s.bind((self.host, port1))
              s.listen()




  def readData(self):

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    print("before socket")
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
          print(f"Received {data4!r} from {p!r}")



  def zmqRead(self):

       print("Listening1")
       context = zmq.Context()
       socket = context.socket(zmq.REP)
       for port1 in self.ports:
         print("Listening2")
         socket.bind("tcp://*:12346")
         while True:
            #  Wait for next request from client
             print("Listening3............")
             time.sleep(3)
             print("awake...........")
             message = socket.recv()
             print(f"Received request: {message}")
             zmqBroadCast(message,port)
             break

  def zmqRead1(self):

          context = zmq.Context()
          socket = context.socket(zmq.REP)
          for port1 in self.ports:
                  socket.connect("tcp://*:"+str(port))
          #    while True:
                  #  Wait for next request from client
                  message = socket.recv()
                  print(f"Received request: {message}")
                  #  Send reply back to client
                  socket.send(b"World")
           #       break

  def zmqWrite(self,data,port):
      if port not in self.neighbors:
          print("node is out of range!")
          return

      context = zmq.Context()

      #  Socket to talk to server
      print("Connecting to hello world server…")
      socket = context.socket(zmq.REQ)
      socket.connect("tcp://localhost:"+str(port))
      #  Do 10 requests, waiting each time for a response
      #for request in range(10):
      print(f"Sending request 1 …")
      socket.send(b"Hello")
      print("Sent")
      #  Get the reply.
     # print(" Not Waiting for reply")
      #while True:
       #message = socket.recv()

     # print(f"Received reply {request} [ {message} ]")

  def zmqBroadCast(self, data,port):
      context = zmq.Context()

      #  Socket to talk to server
      print("Connecting to hello world server…")
      for neighbor in self.neighbors:
       if neighbor is not port:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:"+str(neighbor))
      #  Do 10 requests, waiting each time for a response
      # for request in range(10):
        print(f"Sending request broadcast …")
        socket.send(b"Hello")
        print("Sent Broadcast")