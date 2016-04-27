##################################
#   SEND AND RECEIVE             #
##################################
'''
This is the most simple example about how
to send a message between 2 agents
'''
# noinspection PyUnresolvedReferences
import os
import sys
import time
import unittest

sys.path.append('../..')

import spade

host = "127.0.0.1"


class Sender(spade.Agent.Agent):

    def _setup(self):
		self.addBehaviour(self.SendMsgBehav())
		print "Sender started!"
		
    class SendMsgBehav(spade.Behaviour.OneShotBehaviour):

        def _process(self):
            msg = spade.ACLMessage.ACLMessage()
            msg.setPerformative("inform")
            msg.addReceiver(spade.AID.aid("b@"+host,["xmpp://b@"+host]))
            msg.setContent("testSendMsg")

            self.myAgent.send(msg)
            
            print "a has sent a message:"
            print str(msg)
            
            
class Receiver(spade.Agent.Agent):
    
    class RecvMsgBehav(spade.Behaviour.OneShotBehaviour):

        def _process(self):
            msg = self._receive(block=True,timeout=10)
            print "b has received a message:"
            print str(msg)
    
    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RecvMsgBehav(),t)
	print "Receiver started!"
    
    
a = Sender("a@"+host,"secret")
b = Receiver("b@"+host,"secret")

b.start()
import time
time.sleep(1)
a.start()
alive = True
alive = True
counter = 0
while alive:
    time.sleep(1)
    counter = counter + 1
    print("Alive")
    print(counter)
    if counter == 15:
        alive = False
    else:
        alive = True
a.stop()
b.stop()
print("Agents finished their job")
sys.exit(0)
