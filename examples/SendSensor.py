##################################
#   Sensor sender                #
##################################
'''
This agents send information to another agent specified by name
'''
# noinspection PyUnresolvedReferences

import spade
import spade
import time
import sys
import matplotlib.pyplot as pl
import numpy as np

sys.path.append('../..')

A=2
period = 6
dt = 0.1
rnd = np.random.RandomState(0)


class MyAgent(spade.Agent.Agent):
    class SendBehv(spade.Behaviour.Behaviour):
        def onStart(self):
            print "Creating Sensor Agent. . ."
            # Initialize variables
            self.counter = 0
            self.sensor = 0
            self.y = np.array([self.sensor])
            self.x = np.array([self.counter])
            # First, form the AMS AID to inform start
            informAMS = spade.AID.aid(name="ams.127.0.0.1", addresses=["xmpp://ams.127.0.0.1"])
            # Second, build the message
            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msg.setOntology("Estimation")  # Set the ontology of the message content
            self.msg.setLanguage("OWL-S")  # Set the language of the message content
            self.msg.addReceiver(informAMS)  # Add the message receiver
            self.msg.setContent("Start of Transmission")  # Set the message content
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msg)

        def _process(self):
            print "Counter:", self.counter
            # print(self.x)
            print(self.sensor)
            self.counter += dt
            self.sensor = A*np.sin(self.counter)
            # First, form the receiver AID
            receiver = spade.AID.aid(name="estimator@127.0.0.1", addresses=["xmpp://estimator@127.0.0.1"])
            # Second, build the message
            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msg.setOntology("Estimation")  # Set the ontology of the message content
            self.msg.setLanguage("OWL-S")  # Set the language of the message content
            self.msg.addReceiver(receiver)  # Add the message receiver
            self.msg.setContent(self.sensor)  # Set the sensor content
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msg)
            time.sleep(dt)


    def _setup(self):
        print "Starting Sensor Agent . . ."
        b = self.SendBehv()
        self.addBehaviour(b, None)


if __name__ == "__main__":
    a = MyAgent("sensor@127.0.0.1", "secret")
    a.start()
