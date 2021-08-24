#!/usr/bin/env python

import os
import sys
import optparse

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

    def generate_routefile():
        random.seed(42)  # make tests reproducible
        N = 3600  # number of time steps
        # demand per second from different directions
        pH = 1. / 7
        pV = 1. / 11
        pAR = 1. / 30
        pAL = 1. / 25
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
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="left_%i" depart="%i" />' % (
                        vehNr, ch2, i), file=routes)
				
                elif ch1==2:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="top_%i" depart="%i" />' % (
                        vehNr, ch2, i), file=routes)
				
                elif ch1==3:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="down_%i" depart="%i" />' % (
                        vehNr, ch2, i), file=routes)
				
                elif ch1==4:
                    print('    <vehicle id="vehicle_%i" type="SUMO_DEFAULT_TYPE" route="right_%i" depart="%i" />' % (
                        vehNr, ch2, i), file=routes)
                vehNr += 1
                lastVeh = i
            print("</routes>", file=routes)

    def get_options():
        optParser = optparse.OptionParser()
        optParser.add_option("--nogui", action="store_true",
                             default=False, help="run the commandline version of sumo")
        options, args = optParser.parse_args()
        return options
	
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
        print(det_11-det_12,det_21-det_22,det_31-det_32,det_41-det_42)

    def controlTrafficLight(t1,t2,t3,t4):
	
        return 0
		
# contains TraCI control loop
def run():
    step = 0
    while step < 10000:
        traci.simulationStep()
        print(step)
        SumoIntersection.getTrafficState()
        step += 1
    traci.close()
    sys.stdout.flush()

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
    SumoIntersection.generate_routefile()
    traci.start([sumoBinary, "-c", "cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()