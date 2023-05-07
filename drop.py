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
          time.sleep(10)
          #t = threading.Thread(target=self.processMessages, args=(message, port,))
          #t.daemon = True
          #t.start()
      else:
        self.iotaAlgorithmProcess(message, sentby)
          #return
  except KeyError as e:
      print(" errors in process message on " + str(self.ports) + " : " + str(e))

  end_time = time.time()
  convergence_time = end_time - start_time
  print(" convergence time for "+ str(self.ports) + " for message " + str(message) + " is "+ str(convergence_time))




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