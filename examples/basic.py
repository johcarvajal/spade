#####################################
#  BASIC EXAMPLE                    #
#####################################
'''
This file shows a simple agent which just asks for the 
Platform Information (pi) to the AMS agent and prints it 
to the debug system.
It uses a OneShot Behaviour
You need to be running a SPADE platform on the same host
'''

import time
import os
import sys
import spade

sys.path.append('..' + os.sep + 'trunk')
sys.path.append('..')


class MyAgent(spade.Agent.Agent):
    class MyBehav(spade.Behaviour.OneShotBehaviour):
        def onStart(self):
            self.myAgent.DEBUG("Starting behaviour . . .")

        def _process(self):
            self.myAgent.DEBUG("Hello World from a OneShot")
            pi = self.myAgent.getPlatformInfo()
            self.myAgent.DEBUG(str(pi))

        def onEnd(self):
            self.myAgent.DEBUG("Ending behaviour . . .")

    def _setup(self):
        self.DEBUG("MyAgent starting . . .")
        b = self.MyBehav()
        self.addBehaviour(b, None)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        host = "127.0.0.1"
    else:
        host = sys.argv[1]
a = MyAgent("agent@" + host, "secret")
a.wui.start()
a.setDebugToScreen()
a.start()
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
print("End")
sys.exit(0)
