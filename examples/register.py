#!/usr/bin/env python
# encoding: utf-8
import sys
import os
sys.path.append('..'+os.sep+'trunk')
sys.path.append('..')

from spade import *
from spade.ACLMessage import *
from string import *
from time import sleep
from xmpp import *

class RegisterAgent(Agent.Agent):
    class BehaviourDefecte(Behaviour.Behaviour):
        def _process(self):
            sleep(1)

        def onStart(self):
            try:
                sd = DF.ServiceDescription()
                sd.setName("test")
                sd.setType("testservice")
		print sd.asContentObject()
                dad = DF.DfAgentDescription()
                dad.addService(sd)
                dad.setAID(self.myAgent.getAID())
                res = self.myAgent.registerService(dad)
                print "Service Registered",str(res)
            except Exception,e:
                print "EXCEPTION ONSTART",str(e)

    def _setup(self):
        db = self.BehaviourDefecte()
        self.addBehaviour(db, Behaviour.MessageTemplate(Behaviour.ACLTemplate()))

if __name__ == "__main__":
    host = os.getenv("HOSTNAME")
    if host == None:
    	host = "127.0.0.1"

    print "HOST:",host
    ag = RegisterAgent("register@"+host, "secret")
    ag.start()

    while True:
        try:
            sleep(0.5)
        except:
            ag.stop()
            break

