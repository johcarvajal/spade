import spade
import time
from spade.bdi import *
from spade.DF import Service
from spade.Agent import BDIAgent


def s1_method(Value):
    return {"O1": 1}


def s2_method(Myoutput1):
    return {"O2": 2}

def goalCompletedCB(Goal):
    agent.goalCompleted = True


agent = BDIAgent("bdi@127.0.0.1", "secret")

s1 = Service(name="s1", owner=agent.getAID(), inputs=["Value"], outputs=["O1"], P=["Var(Value,0,Int)"],
             Q=["Var(O1,1,Int)"])
s2 = Service(name="s2", owner=agent.getAID(), inputs=["O1"], outputs=["O2"], P=["Var(O1,1,Int)"],
             Q=["Var(O2,2,Int)"])

agent.registerService(s1, s1_method)
agent.registerService(s2, s2_method)

agent.goalCompleted = False

agent.saveFact("Value", 0)

agent.setGoalCompletedCB(goalCompletedCB)

agent.addGoal(Goal("Var(O1,1,Int)"))

agent.start()

counter = 0
while not agent.goalCompleted and counter < 20:
    time.sleep(1)
    print(counter)
    counter += 1

if agent.goalCompleted:
    print("Goal completed")

agent.askBelieve("Var(O1,1,Int)")
agent.getFact("O1")
agent.stop()

print("End")
sys.exit(0)
