import networkx as nx
import random
import hashlib
import NetworkDesignV1_3 as network

if(network.CheckConsensus("message")):
    print("Consensus has been reached!", flush=True)
else:
    print("didn't passed", flush=True)

print("End of program")










