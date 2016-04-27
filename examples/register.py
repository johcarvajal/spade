#!/usr/bin/env python
# encoding: utf-8
#####################################
#  REGISTER EXAMPLE                 #
#####################################
'''
This file shows a simple agent which just registers
a service in the DF. Then it searches for the same service
in order to check it is properly registered.
You need to be running a SPADE platform on the same host
'''

import os
import sys

sys.path.append('..'+os.sep+'trunk')
sys.path.append('..')

import spade
from time import sleep


class RegisterAgent(spade.Agent.Agent):
    class BehaviourDef(spade.Behaviour.Behaviour):
        def _process(self):
            sleep(1)

        def onStart(self):
            try:
                sd = spade.DF.ServiceDescription()
                sd.setName("test")
                sd.setType("testservice")
                dad = spade.DF.DfAgentDescription()
                dad.addService(sd)
                sd = spade.DF.ServiceDescription()
                sd.setName("MYSERVICE")
                sd.setType("MYTYPE")
                dad.addService(sd)
                dad.setAID(self.myAgent.getAID())
                res = self.myAgent.registerService(dad)
                print "Service Registered:",str(res)
                
                # Now the search
                dad = spade.DF.DfAgentDescription()
                ds = spade.DF.ServiceDescription()
                ds.setType("testservice")
                dad.addService(ds)
                search = self.myAgent.searchService(dad)
                print "Search Results:"
                for s in search:
                    print " * ",s.asRDFXML()
                
            except Exception,e:
                print "EXCEPTION ONSTART",str(e)

    def _setup(self):
        db = self.BehaviourDef()
        self.addBehaviour(db, spade.Behaviour.MessageTemplate(spade.Behaviour.ACLTemplate()))

if __name__ == "__main__":
    host = os.getenv("HOSTNAME")
    if host == None:
        host = "127.0.0.1"

    print "Using HOST:",host
    ag = RegisterAgent("register@"+host, "secret")
    ag.setDebugToScreen()
    ag.start()

    while True:
        try:
            sleep(0.5)
        except:
            ag.stop()
            break

