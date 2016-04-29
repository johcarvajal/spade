##################################
#   Sensor Plot                  #
##################################
'''
This is an example to show how agent can communicate to send information to each other
'''
# noinspection PyUnresolvedReferences
import spade
import time
import sys
import matplotlib.pyplot as pl
import numpy as np

sys.path.append('../..')

host = "127.0.0.1"
A=2
period = 6
dt = 0.1
rnd = np.random.RandomState(0)

class Sender(spade.Agent.Agent):
    class Periodic(spade.Behaviour.Behaviour):
        def onStart(self):
            print "Starting behaviour . . ."
            self.counter = 0
            self.sensor = 0
            self.y = np.array([self.sensor])
            self.x = np.array([self.counter])

        def _process(self):
            print "Counter:", self.counter
            print(self.x)
            print(self.y)
            self.counter += dt
            self.sensor = A*np.sin(self.counter)
            if self.counter > period:
                pl.figure(figsize=(16, 6))
                self.signal = pl.scatter(self.x, self.y, marker='o', color='b', linestyle='-',label='Sensor Data')
                pl.legend(loc='upper right')
                pl.xlim(xmin=0, xmax=self.counter)
                pl.xlabel('time[s]')
                pl.ylabel('Position [m]')
                pl.ylim(ymin=-(A+0.1), ymax=(A+0.1))
                pl.show()
                self.counter = 0
                self.sensor = 0
                self.x = np.array([self.counter])
                self.y = np.array([self.sensor])
                print("Starting over")
            else:
                time.sleep(dt)
                self.x = np.append(self.x, self.counter)
                self.y = np.append(self.y, self.sensor)

    def _setup(self):
        print "Sensor Agent Starting . . ."
        b = self.Periodic()
        self.addBehaviour(b, None)

if __name__ == "__main__":
    a = Sender("sensor@"+host, "secret")
    a.start()

