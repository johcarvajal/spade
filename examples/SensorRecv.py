import spade


class MyAgent(spade.Agent.Agent):
    class RecvMsgBehav(spade.Behaviour.Behaviour):
        def onStart(self):
            print "Starting Estimation Agent. . ."
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
            msg = self._receive(block=True,timeout=10)
            print "Estimator has received a message:"
            print str(msg)

    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("sensor@127.0.0.1", ["xmpp://sensor@127.0.1"]))
        t = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.RecvMsgBehav(),t)
        print "Receiver started!"

if __name__ == "__main__":
    b = MyAgent("estimator@127.0.0.1", "secret")
    b.start()
