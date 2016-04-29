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
import spade
import matplotlib.pyplot as pl
import numpy as np
from pykalman import KalmanFilter
import unittest
sys.path.append('../..')

# Host Address for the MAS platform
host = "127.0.0.1"
# Amplitude of the position signal
A=2
# Simulation Length (seconds)
period = 13
# Sampling period in seconds
dt = 0.01
# Seed initialization
rnd = np.random.RandomState(0)


class Sender(spade.Agent.Agent):

    def _setup(self):
        self.addBehaviour(self.SendMsgBehav(), None)
        print "Sensor started!"
        time.sleep(dt)

    class SendMsgBehav(spade.Behaviour.Behaviour):
        def onStart(self):
           # Initialize variables
            self.counter = 0
            self.sensor = 0
            self.y = np.array([self.sensor])
            self.x = np.array([self.counter])
            # First, form the AMS AID to inform start
            self.informAMSt = spade.AID.aid(name="ams.127.0.0.1", addresses=["xmpp://ams.127.0.0.1"])
            # Second, build the message
            self.msgt = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msgt.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msgt.setOntology("Estimation")  # Set the ontology of the message content
            self.msgt.setLanguage("OWL-S")  # Set the language of the message content
            self.msgt.addReceiver(self.informAMSt)  # Add the message receiver
            self.msgt.setContent("Start of Transmission")  # Set the message content
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msgt)

        def _process(self):
            self.counter += dt
            self.sensor = A*np.sin(self.counter)+0.1*A*rnd.randn()
            #print "Counter:", self.counter
            #print(self.sensor)
            self.msg = spade.ACLMessage.ACLMessage()
            self.msg.setPerformative("inform")
            self.msg.addReceiver(spade.AID.aid("estimator@"+host,["xmpp://estimator@"+host]))
            self.msg.setContent(str(self.sensor))
            self.myAgent.send(self.msg)
            print "Sensor has sent a message:"
            print(self.msg.content)
            self.x = np.append(self.x, self.counter)
            self.y = np.append(self.y, self.sensor)
            time.sleep(dt)

        def onEnd(self):
            print("Launching Figures for Sender")
            #
            #print(self.x)
            #print(self.y)
            # First, form the AMS AID to inform start
            self.informAMST = spade.AID.aid(name="ams.127.0.0.1", addresses=["xmpp://ams.127.0.0.1"])
            # Second, build the message
            self.msgT = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msgT.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msgT.setOntology("Estimation")  # Set the ontology of the message content
            self.msgT.setLanguage("OWL-S")  # Set the language of the message content
            self.msgT.addReceiver(self.informAMST)  # Add the message receiver
            self.msgT.setContent("End of Transmission")  # Set the message content
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msgT)


class Receiver(spade.Agent.Agent):

    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("sensor@"+host,["xmpp://sensor@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RecvMsgBehav(), t)
        print "Estimator started!"
        time.sleep(dt)

    class RecvMsgBehav(spade.Behaviour.Behaviour):
        def onStart(self):
           # Initialize variables
            self.counterr = 0
            self.datarcv = 0
            self.yr = np.array([self.datarcv])
            self.xr = np.array([self.counterr])
            # First, form the AMS AID to inform start
            self.informAMSr = spade.AID.aid(name="ams.127.0.0.1", addresses=["xmpp://ams.127.0.0.1"])
            # Second, build the message
            self.msgr = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msgr.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msgr.setOntology("Estimation")  # Set the ontology of the message content
            self.msgr.setLanguage("OWL-S")  # Set the language of the message content
            self.msgr.addReceiver(self.informAMSr)  # Add the message receiver
            self.msgr.setContent("Start of Reception")  # Set the message content
            print(self.msgr.content)
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msgr)

        def _process(self):
            self.counterr += dt
            self.msg2 = spade.ACLMessage.ACLMessage()
            self.msg = self._receive(block=True, timeout=2*dt)
            self.msg2 = self.msg
            print "Estimator has received a message:"
            self.msgs = self.msg2.content
            self.datarcv = float(self.msgs)
            print(self.datarcv)
            self.xr = np.append(self.xr, self.counterr)
            self.yr = np.append(self.yr, self.datarcv)

        def onEnd(self):
            print("Launching Figures for Estimator")
            #print(self.xr)
            #print(self.yr)
            kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]), transition_covariance=0.01 * np.eye(2))
            self.states_pred = kf.em(self.yr).smooth(self.yr)[0]
            self.signalr = pl.scatter(self.xr, self.yr, linestyle='-', marker='o', color='b',
                            label='Data Received from Sensor')
            self.position_line = pl.plot(self.xr,self.states_pred[:, 0], linestyle='-', marker='o', color='g',
                            label='Data Estimated from Sensor')
            self.position_error = pl.plot(self.xr, (self.yr-self.states_pred[:, 0]), linestyle='-', marker='o',
                            color='m', label='Relative Estimation Error')
            pl.legend(loc='upper right')
            pl.xlim(xmin=0, xmax=self.counterr)
            pl.xlabel('time[s]')
            pl.ylabel('Position [m]')
            pl.ylim(ymin=-(A+0.25), ymax=(A+0.25))
            pl.show()
            # First, form the AMS AID to inform start
            self.informAMSr = spade.AID.aid(name="ams.127.0.0.1", addresses=["xmpp://ams.127.0.0.1"])
            # Second, build the message
            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msg.setOntology("Estimation")  # Set the ontology of the message content
            self.msg.setLanguage("OWL-S")  # Set the language of the message content
            self.msg.addReceiver(self.informAMSr)  # Add the message receiver
            self.msg.setContent("End of Reception")  # Set the message content
            print(self.msg.content)
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msg)

# Initialize Agents
sensor = Sender("sensor@"+host,"secret")
estimator = Receiver("estimator@"+host,"secret")
# Start Agents
estimator.start()
time.sleep(dt)
sensor.start()
# Wait loop
alive = True
time_delay = 0
while alive:
    time.sleep(1)
    time_delay += 1
    if time_delay == period:
        alive = False
    else:
        alive = True
sensor.stop()
estimator.stop()
time.sleep(1)
print("End of operation")
sys.exit(0)


