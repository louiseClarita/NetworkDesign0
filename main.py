import networkx as nx
import random
import hashlib

class PBFTNode:
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.peers = self.get_peers()
        self.state = 'pre-prepare'
        self.current_view = 0
        self.current_seq_num = 0
        self.current_request = None
        self.prepare_msgs = {}
        self.commit_msgs = {}

    def get_peers(self):
        G = nx.fast_gnp_random_graph(self.num_nodes, 0.5)
        return list(G.adj[self.node_id])

    def pre_prepare(self, request):
        self.current_request = request
        msg = f'pre-prepare:{self.current_view}:{self.current_seq_num}:{self.current_request}'
        self.broadcast(msg)

    def prepare(self):
        msg = f'prepare:{self.current_view}:{self.current_seq_num}:{self.current_request}'
        self.broadcast(msg)

    def commit(self):
        msg = f'commit:{self.current_view}:{self.current_seq_num}:{self.current_request}'
        self.broadcast(msg)

    def handle_msg(self, msg):
        msg_type, view, seq_num, request = msg.split(':')
        #
        # if view > self.current_view:
        #     self.current_view = view
        #     self.current_seq_num = 0

        if seq_num < self.current_seq_num:
            return

        if msg_type == 'pre-prepare' and self.state == 'pre-prepare':
            self.state = 'prepare'
            self.current_seq_num = seq_num
            self.prepare_msgs[self.node_id] = msg
            self.prepare()
        elif msg_type == 'prepare' and self.state == 'prepare':
            self.prepare_msgs[self.node_id] = msg
            if len(self.prepare_msgs) > (self.num_nodes * 2) / 3:
                self.state = 'commit'
                self.commit_msgs[self.node_id] = msg
                self.commit()

                # elif msg_type == 'prepare' and self.state == 'prepare':
                # self.prepare_msgs[self.node_id] = msg
                # if len(self.prepare_msgs) > (self.num_nodes * 2) / 3:
                #     self.state = 'commit'
                #     self.commit_msgs[self.node_id] = msg
                #     self.commit()
        elif msg_type == 'commit' and self.state == 'commit':
            self.commit_msgs[self.node_id] = msg
            if len(self.commit_msgs) > (self.num_nodes * 2) / 3:
                self.state = 'done'
                print(f'Node {self.node_id} done with request: {self.current_request}')

    #
    # def broadcast(self, msg):
    #     for peer in self.peers:
    #         if random.random() < 0.9: # Simulate network delays/drops
    #             print(f'Node {self.node_id} sending to node {peer}: {msg}')
    #             # Create hash of message to simulate digital signature

    #             hash = hashlib

    #             hash = hashlib.sha256(msg.encode()).hexdigest()
    #             self.handle_msg(f'{msg}:{hash}')


    def broadcast(self, msg):
        for peer in self.peers:
            if random.random() < 0.9: # Simulate network delays/drops
                print(f'Node {self.node_id} sending to node {peer}: {msg}')
                # Create hash of message to simulate digital signature
                hash = hashlib.sha256(msg.encode()).hexdigest()
                self.handle_msg(f'{msg}:{hash}')


num_nodes = 5
nodes = [PBFTNode(i, num_nodes) for i in range(num_nodes)]
request = 'test request'
nodes[0].pre_prepare(request)

