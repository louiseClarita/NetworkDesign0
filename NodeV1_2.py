# echo-server.py
import hashlib
import json
import socket
import NetworkConfig
import time
import zmq
import threading
import random
##from IOTATransaction1 import dict_to_transaction, calculate_transaction_weight, to_dict, IOTATransactionEncoder
##from Tangle1 import Tangle

##import iota
#from iota import Transaction, TransactionTrytes, TransactionHash, ProposedTransaction, TryteString, Bundle


variable_mutex = threading.Lock()


class Node:
    # context = zmq.asyncio.Context()
    currentSendingNode = 0
    messageRCVD = 0
    broadcastCounter = 0
    # Generate a random seed.
    ##myseed = iota.crypto.types.Seed.random()
    # Get an address generator.
    ##address_generator = iota.crypto.addresses.AddressGenerator(myseed)
    ##addys = address_generator.get_addresses(1, count=2)
    ##api = iota.Iota("https://nodes.thetangle.org:443", myseed, local_pow=True)

    tangleCounter = 0

    def __init__(self, host, ports, neighbors, tangle):
        self.host = host
        self.ports = ports
        self.neighbors = neighbors
        # global tangle
        self.tangle = tangle
        global messageRCVD
        self.currentSendingNode
        self.inputNodesList = []
        self.sending_socket = None
        self.sending_socket2 = None

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

    def BroadCastData(self, data):
        for p in self.ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, p))
                s.sendall(data.encode())
                data2 = s.recv(1024).decode()
                print(f"Received {data2!r} from {p!r}")

    def sendData(self, data3, port):

        if port not in self.ports:
            print("node is out of range!")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, port))
            s.sendall(data3.encode())
            data4 = s.recv(1024).decode()

    def zmqRead(self):

        # print("Listening1")
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            # print("Listening2")
            socket.bind("tcp://*:" + str(self.ports))
            while True:

                message = socket.recv()

                self.messageRCVD = message.decode()
                socket.send_string("rcvd on " + str(self.ports))
                # print(f"Received request: {message.decode()}", flush=True)
                if (self.tangle.confirmMessage(self.messageRCVD)):
                    # print(f"message confirmed, adding to tangle, and broadcasting...", flush=True)

                    txs = json.loads(self.messageRCVD)
                    transaction = dict_to_transaction(txs)
                    if transaction_exists(transaction, self.tangle):
                        print("already existing in this dag")
                    else:

                        # tip_selection_algorithm = TipSelectionAlgorithm(self.tangle)
                        if transaction.validate():
                            txhash = transaction.get_transaction_hash()
                            transaction.calculate_weight(txhash)
                            if self.tangle.select_tips(5) is not None:
                                trunk_hash, branch_hash = self.tangle.select_tips(5)
                                transaction.setTrunk(trunk_hash)
                                transaction.setBranch(branch_hash)
                                # print(str(transaction.validate()),flush=True)

                                # print('Transaction is confirmed!')

                                trunk_tx_hash = transaction.trunk_transaction_hash
                                branch_tx_hash = transaction.branch_transaction_hash
                                # Compute the hash of the transaction
                                # transaction_hash = transaction.get_transaction_hash()

                                # print(f'Trunk transaction hash: {trunk_tx_hash}', flush=True)
                                # print(f'Branch transaction hash: {branch_tx_hash}', flush=True)
                                # self.tangle.add_transaction(transaction, weight,{1})
                                # Wait for the transaction to be confirmed by other nodes

                                # self.tangle.add_transaction(transaction_hash, calculate_transaction_weight(transaction),
                                #                               {trunk_hash, branch_hash})
                                self.tangle.add_transaction1(transaction)
                                self.tangleCounter = self.tangleCounter + 1
                                self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)


                            else:
                                transaction_hash = transaction.get_transaction_hash()
                                # self.tangle.add_transaction(transaction_hash, calculate_transaction_weight(transaction),
                                #                             {1})
                                self.tangle.add_transaction1(transaction)
                                self.tangleCounter = self.tangleCounter + 1
                                self.zmqBroadCast(to_dict(transaction), self.currentSendingNode)

                        else:
                            print('Transaction is not yet confirmed.', flush=True)


        #           return
        except zmq.ZMQError as e:
            print(" errors : " + str(e))
            exit(1)

    def zmqRead2(self):

        # print("Listening1")
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        # print("Listening2")
        socket.bind("tcp://*:" + str(self.ports))
        while True:

            #  Wait for next request from client
            print("Listening3............", flush=True)
            # time.sleep(3)
            # print("awake...........")
            message = socket.recv()
            # self.messageRCVD = message.decode()
            self.messageRCVD = message
            print(f"Received request: {message}", flush=True)
            if (self.tangle.confirmMessage(messageRCVD)):
                print(f"message confirmed, adding to tangle, and broadcasting", flush=True)
                self.tangle.add_transaction(messageRCVD, {1})

                self.zmqBroadCast(message.decode(), self.currentSendingNode)

            break

    def zmqRead1(self):

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        for port1 in self.ports:
            socket.connect("tcp://*:" + str(self.ports))
            #    while True:
            #  Wait for next request from client
            message = socket.recv()

            print(f"Received request: {message}")
            #  Send reply back to client
            socket.send(b"World")
        #       break

    def zmqWrite(self, data, port, sendingPort):
        if port not in self.neighbors:
            print("node is out of range!")
            return
        context = zmq.Context()
        self.broadcastCounter = 0
        try:
            #  Socket to talk to server
            # print(f"Connecting to hello world server from {sendingPort}")
            self.currentSendingNode = sendingPort
            self.sending_socket = context.socket(zmq.REQ)
            self.sending_socket.connect("tcp://127.0.0.1:" + str(port))
            # Convert dictionary to JSON string
            json_string = json.dumps(data, cls=IOTATransactionEncoder)
            # Set up poller

            self.sending_socket.send_string(json_string)
            print("Sent", flush=True)
            # while True:
            # response = socket.recv_string()
            # print(f"Received response: {response}")

            t8 = threading.Thread(target=self.zmqRCV, args=(port,))
            t8.daemon = True
            t8.start()

        #          return
        except zmq.ZMQError as e:
            print(" errors : " + str(e))
            exit(1)

    def zmqRCV(self, port):
        message = self.sending_socket.recv()
        print(message)

    def zmqBroadCast(self, data, currentSendingNode1):
        context = zmq.Context()
        if self.broadcastCounter != 0:
            print("this node already sent her own broadcast, It will not send another!")
            return
        else:
            self.broadcastCounter = self.broadcastCounter + 1
        i = 0

        try:
            for neighbor in self.neighbors:
                print("je suis là\n")
                print("neighbor :" + str(neighbor) + " in input nodes list :" + str(self.inputNodesList))
                if neighbor in self.inputNodesList:
                    print(
                        "\nThis is the sender we will not send it back1 and the neighbor i am attempting to reach out to is" + str(
                            neighbor), flush=True)
                elif neighbor not in self.inputNodesList:

                    if neighbor != currentSendingNode1:
                        self.sending_socket = context.socket(zmq.REQ)
                        self.sending_socket.connect("tcp://localhost:" + str(neighbor))
                        print(" I am " + str(self.ports) + "currentSendingNode : " + str(
                            self.currentSendingNode) + ",/n currentsendingNode1 : " + str(currentSendingNode1))
                        print("broadcast from" + str(self.ports) + " ->" + str(neighbor), flush=True)
                        # Convert the transaction to trytes
                        # tx_trytes = data.as_tryte_string()
                        # self.currentSendingNode = neighbor
                        # Convert the trytes to bytes
                        # tx_bytes = self.trytes_to_bytes(tx_trytes)
                        # socket.send(tx_bytes)
                        NeighboringNode = NetworkConfig.network.getNodeByPort(node=neighbor)
                        if NeighboringNode == -1:
                            print("node was not found")
                            exit(1)
                        NeighboringNode.currentSendingNode = self.ports
                        NeighboringNode.inputNodesList.append(self.ports)
                        json_string = json.dumps(data, cls=IOTATransactionEncoder)
                        self.sending_socket.send_string(json_string)

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
        #            return
        #            return
        except zmq.ZMQError as e:
            print(" errors : " + str(e))
            exit(1)

    def closeSocket(self, port):

        #      if not self.sending_socket.closed:
        #  time.sleep(60)
        # self.sending_socket.close()
        print("not closing this socket:)")

    def zmqWrite1(self, data, port, sendingPort):
        if port not in self.neighbors:
            print("node is out of range!")
            #            return
        variable_mutex.acquire()
        context = zmq.Context()
        try:
            #  Socket to talk to server
            # print(f"Connecting to hello world server from {sendingPort}")
            self.currentSendingNode = sendingPort
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://127.0.0.1:" + str(port))
            # Convert dictionary to JSON string
            json_string = json.dumps(data)
            socket.send_string(json_string)
            print("Sent", flush=True)
        except zmq.ZMQError as e:
            print(" errors : " + str(e))
        finally:
            # release the mutex to allow other threads to access the object variable
            variable_mutex.release()

    def zmqBroadCast1(self, data, currentSendingNode1):
        context = zmq.Context()

        #  Socket to talk to server
        # print("Connecting to hello world server…")
        i = 0
        # create a mutex to synchronize access to the object variable
        variable_mutex = threading.Lock()
        # acquire the mutex to access the object variable
        variable_mutex.acquire()
        try:
            for neighbor in self.neighbors:
                if neighbor is not currentSendingNode1:
                    socket = context.socket(zmq.REQ)
                    socket.connect("tcp://localhost:" + str(neighbor))
                    #  Do 10 requests, waiting each time for a response
                    # for request in range(10):
                    print("broadcast from" + str(self.ports) + " ->" + str(neighbor), flush=True)
                    self.currentSendingNode = neighbor
                    # Convert the transaction to trytes
                    # tx_trytes = data.as_tryte_string()

                    # Convert the trytes to bytes
                    # tx_bytes = self.trytes_to_bytes(tx_trytes)
                    # socket.send(tx_bytes)
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
        print(" Node : { port:" + str(self.ports) + " ,"
                                                    "Neighbors : " + str(self.neighbors) + " "
                                                                                           "CurrentData : " + str(
            self.messageRCVD) + ""
                                "Current Tangle Index : " + str(self.tangleCounter) + ""
                                                                                      "\n"


        # + "Tangle "+ self.tangle.to_string()+"  "

                                                                                      "}", flush=True)

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


def transaction_exists(transaction, dag: Tangle):
    for t in dag.transactions:
        if t.bundle_hash == transaction.bundle_hash:
            return True
    return False