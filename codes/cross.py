import os,sys
import traci

sys.path.append(os.path.join('d:', os.sep, 'sumo','sumo-1.1.0','tools'))
sumoBinary = "D:/sumo/sumo-1.1.0/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "cross.sumocfg"]
traci.start(sumoCmd) 
step = 0
while step < 1000:
   traci.simulationStep()
   if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
       traci.trafficlight.setRedYellowGreenState("0", "GrGr")
   step += 1

traci.close()