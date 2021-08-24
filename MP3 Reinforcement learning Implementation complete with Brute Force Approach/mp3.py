#!/usr/bin/env python
import os.path
from os import path
import os
import sys
import optparse
import numpy as np
import pandas as pd
import time
import random

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import random

veh11=veh12=veh21=veh22=veh31=veh32=veh41=veh42=''
det_11=det_12=det_21=det_22=det_31=det_32=det_41=det_42=0
ROAD_CAPACITY = 50

class SumoIntersection:
    def __init__(Self):
        # we need to import python modules from the $SUMO_HOME/tools directory
        try:
            sys.path.append(os.path.join(os.path.dirname(
                __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
            sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
                os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
            from sumolib import checkBinary  # noqa
        except ImportError:
            sys.exit(
                "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

	#generate random traffic for the each new episod and save it in the input_routes.rou.xml file
    def generate_routefile():
        random.seed(42)  # make tests reproducible
        N = 10000  # number of time steps
        # demand per second from different directions
        with open("input_routes.rou.xml", "w") as routes:
            print('''<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <vType id="SUMO_DEFAULT_TYPE" accel="0.8" decel="4.5" sigma="0" length="5" minGap="2" maxSpeed="70"/>
    
	<route id="left_1" edges="1si 4o"/>
	<route id="left_2" edges="1si 2o"/>
	<route id="left_3" edges="1si 3o"/>
	
	<route id="top_1" edges="4si 1o"/>
	<route id="top_2" edges="4si 2o"/>
	<route id="top_3" edges="4si 3o"/>
	
	<route id="down_1" edges="3si 1o"/>
	<route id="down_2" edges="3si 2o"/>
	<route id="down_3" edges="3si 4o"/>
	
	<route id="right_1" edges="2si 1o"/>
	<route id="right_2" edges="2si 3o"/>
	<route id="right_3" edges="2si 4o"/>
    ''', file=routes)
            lastVeh = 0
            vehNr = 0
            ch1=ch2=0
            for i in range(N):
                ch1=random.choice([1,2,3,4])
                ch2=random.choice([1,2,3])
				
                if ch1==1:
                    v=i*3
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="left_%i" depart="%i" />' % (
                        vehNr, ch2, v), file=routes)
				
                elif ch1==2:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="top_%i" depart="%i" />' % (
                        vehNr, ch2, v), file=routes)
				
                elif ch1==3:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="down_%i" depart="%i" />' % (
                        vehNr, ch2, v), file=routes)
				
                elif ch1==4:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="right_%i" depart="%i" />' % (
                        vehNr, ch2, v), file=routes)
                vehNr += 1
                lastVeh = i
            print("</routes>", file=routes)

    def get_options():
        optParser = optparse.OptionParser()
        optParser.add_option("--nogui", action="store_true",
                             default=False, help="run the commandline version of sumo")
        options, args = optParser.parse_args()
        return options

	#return the no of vehicle waiting in the lane as the list
    def getTrafficState():
        global veh11,veh12,veh21,veh22,veh31,veh32,veh41,veh42
        global det_11,det_12,det_21,det_22,det_31,det_32,det_41,det_42
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_11")
        for i in v:
            if i!=veh11:
                det_11+=1#v.size;
            veh11=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_12")
        for i in v:
            if i!=veh12:
                det_12+=1#v.size;
            veh12=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_21")
        for i in v:
            if i!=veh21:
                det_21+=1#v.size;
            veh21=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_22")
        for i in v:
            if i!=veh22:
                det_22+=1#v.size;
            veh22=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_31")
        for i in v:
            if i!=veh31:
                det_31+=1#v.size;
            veh31=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_32")
        for i in v:
            if i!=veh32:
                det_32+=1#v.size;
            veh32=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_41")
        for i in v:
            if i!=veh41:
                det_41+=1#v.size;
            veh41=i
		
        v=traci.inductionloop.getLastStepVehicleIDs("det_42")
        for i in v:
            if i!=veh42:
                det_42+=1#v.size;
            veh42=i
			
        #print(veh11,veh12,veh21,veh22,veh31,veh32,veh41,veh42)
        return(det_11-det_12,det_21-det_22,det_31-det_32,det_41-det_42)


	#give the time of the state of the traffic light in the list time ex.[12,13,14,15]
	#there are only four green state to change yellow state are set to 1 sec fixed
    def controlTrafficLight(time):
        #traci.trafficlight.setPhaseDuration("0", t1)
        v=traci.trafficlight.getCompleteRedYellowGreenDefinition("0")
        index=0
        #print(v)
        #print('*************************************************************************')
        for i in v:
            t=i.getPhases()
            for phase in t:
                if phase.duration>1:
                    phase.duration=time[index]
                    index+=1;
                    #print(phase.duration)
       #print(v[0])
        traci.trafficlight.setCompleteRedYellowGreenDefinition("0", v[0])
	

def determineReward(s1,s2,s3,s4,S1,S2,S3,S4,waitTime):
    old_score = S1*S1+S2*S2+S3*S3+S4*S4
    new_score = s1*s1+s2*s2+s3*s3+s4*s4
    #print(s1,s2,s3,s4,S1,S2,S3,S4)
    #print("New Reward to store: ")
    reward = old_score - new_score - (waitTime/30)
    return(old_score - new_score - (waitTime/30))

def updateRewardValue(reward, currentState, action, newState):
    #print("bla")
    #print(currentState)
    #print(action)
    #print("Reward Updated at action", str(A[action]), "and state", str(df.at[currentState,'state']))
    val=df.at[currentState,str(A[action])]
    #df.at[currentState,str(A[action])]=(reward*GAMMA)
    df.at[currentState,str(A[action])]=(val)+ALPHA*(reward+GAMMA*findMaxReward(newState)-val);
    print( "The value stored in table is: ",str((val)+ALPHA*(reward+GAMMA*findMaxReward(newState)-val)) )

def determineTrafficState(S1,S2,S3,S4,t1,t2,t3,t4):
    #something here
    for i in range(len(df['state'])):
#       print(df['state'][i])
#       print([t1,S1,t2,S2,t3,S3,t4,S4])
        if df['state'][i] == [t1,S1,t2,S2,t3,S3,t4,S4]:
            return(i)
    #print("Lafda hai kuch")

def actionSelection(EPSILON,i):
    r = (random.randint(0,100)/100)
    #print(r)
    if EPSILON < r:
        #print(r)
        #print(EPSILON)
        #Select a random action
        ind = random.randint(0,len(A)-1)
        return(ind)
    else:
        ind = findMaxReward(i)
        return(ind)
        #Select best possible action

def findMaxReward(i):
    maxRew = 0
    maxRewInd = 0
    for r in range(len(A)):
        #print(A[r])
        #print(i)
        if (df[str(A[r])][i] > maxRew):
            #maxRew = df[str(A[i])][r]
            maxRewInd = r
            print("Max Reward")
            print(maxRewInd)
    return(maxRewInd)

def state(val):
    s=0
    if val < 10:
        s = 0
    elif val < 25:
        s = 1
    else:
        s = 2
    return s

# contains TraCI control loop
def run():
    global EPSILON
    t1=random.randint(1,4)
    t2=random.randint(1,4)
    t3=random.randint(1,4)
    t4=random.randint(1,4)
    step = 0

    #find current traffic state:
    S1,S2,S3,S4 = SumoIntersection.getTrafficState()
    S1 = state(S1)
    S2 = state(S2)
    S3 = state(S3)
    S4 = state(S4)
    print(S1,S2,S3,S4,t1,t2,t3,t4)
    currentState = determineTrafficState(S1,S2,S3,S4,t1,t2,t3,t4)
    #action selection:
    action = actionSelection(EPSILON,currentState)
    [t1,t2,t3,t4] = A[action]
    count =0
    waitTime = 0
    while step < 100000:
        traci.simulationStep()
        #print(t1*10+t2*10+t3*10+t4*10)
        #print(step)
        s1,s2,s3,s4 = SumoIntersection.getTrafficState()
        #calculate net waiting time of all vehicles
        waitTime = waitTime + (s1+s2+s2+s4)
        #check for conjustion
        if step > 100 and ((max(s1,s2,s3,s4) > ROAD_CAPACITY) or (max(s1,s2,s3,s4) <= 1 )):
            print('road capacity violated')
            print( max(s1,s2,s3,s4) )
            return
        #print (max(s1,s2,s3,s4))
        s1 = state(s1)
        s2 = state(s2)
        s3 = state(s3)
        s4 = state(s4)
        if (t1*10+t2*10+t3*10+t4*10) <= count:
            oldAction = action
            #action selection:
            action = actionSelection(EPSILON,currentState)
            [t1,t2,t3,t4] = A[action]
            #determine reward:
            reward = determineReward(s1,s2,s3,s4,S1,S2,S3,S4,waitTime)
            #update reward:
            newState = determineTrafficState(S1,S2,S3,S4,t1,t2,t3,t4)
            updateRewardValue(reward, currentState, oldAction, newState)
            #update EPSILON:
            EPSILON = EPSILON + END_EPSILON/100000
            #Store current state of traffic at each lane value
            S1 = s1
            S2 = s2
            S3 = s3
            S4 = s4
            #determine the net state of the intersection
            currentState = newState
            #end counter
            count = 0
            waitTime = 0
            step += 1
        else:
            count += 1
            #print(count)


        #if step%10 == 0 :
        SumoIntersection.controlTrafficLight([t1*10,t2*10,t3*10,t4*10])
        #print(t1*10,t2*10,t3*10,t4*10)

N_STATES = 12
SUB_STATES = ['low', 'medium', 'high']
MAX_TIME = 4 #Maximum time will be 5 * 20 = 80
MIN_TIME = 1 #Maximum time will be 1 * 20 = 20
TIME = [MIN_TIME, MIN_TIME, MIN_TIME, MIN_TIME]
STATE = [TIME[0], SUB_STATES, TIME[1], SUB_STATES, TIME[2], SUB_STATES, TIME[3], SUB_STATES]
#The possibela ctions possible
SUB_ACTION = [1,1,1,1]
ACTION = [SUB_ACTION[0], SUB_ACTION[1], SUB_ACTION[2], SUB_ACTION[3]]
#print (ACTION)

START_EPSILON = 0.0
END_EPSILON = 0.95
EPSILON = 0.0

ALPHA = 0.1
GAMMA = 0.9
Rewards = []
S = []
A = []
R = []

S_A_R = []

for t1 in range(1,5):
    for s1 in range(3):
        for t2 in range(1,5):
            for s2 in range(3):
                for t3 in range(1,5):
                    for s3 in range(3):
                        for t4 in range(1,5):
                            for s4 in range(3):
                                STATE = [t1,s1,t2,s2,t3,s3,t4,s4]
                                S.append(STATE)

for a1 in range(1,5):
    for a2 in range(1,5):
        for a3 in range(1,5):
            for a4 in range(1,5):
                ACTION = [a1,a2,a3,a4]
                R.append(0.0)
                A.append(ACTION)
#if path.exists("test.csv"):
#    df = pd.read_csv("test.csv")
#else:
#print(len(S))
#S_A_R = S
#NumberOfStates = len(S_A_R)
#LengthOfState = len(S_A_R[0])
#for i in range(len(S)):
#   S_A_R[i].append(A)
#   Rewards.append(R)
    
#print(S_A_R)

raw_data = {'state': S}

df = pd.DataFrame(raw_data)

#print(df)

for i in range(len(A)):
    df[str(A[i])] = 0.0

#print(df)
#df.set_value(13,str(A[24]),6)
#print(df)

#print(findMaxReward(13))

currentState = 0
reward = 0.0

# main entry point
if __name__ == "__main__":
    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run

    options = SumoIntersection.get_options()

    if options.nogui:
    #if True:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    episodes=100
    SumoIntersection.generate_routefile()

    while True:
        veh11=veh12=veh21=veh22=veh31=veh32=veh41=veh42=''
        det_11=det_12=det_21=det_22=det_31=det_32=det_41=det_42=0
        traci.start([sumoBinary, "-c", "cross.sumocfg",
                                 "--start","--quit-on-end"])
        run()
        df.to_csv(r'test.csv')

        traci.close(False)
    sys.stdout.flush()