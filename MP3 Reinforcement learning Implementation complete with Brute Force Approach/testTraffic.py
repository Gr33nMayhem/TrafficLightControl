import numpy as np
import pandas as pd
import time
import random

#low -> less than 5, medium -> less than 15, high-> greater than 15



def generateNewTrafficState(s1,s2,s3,s4):
	l1 = random.randint(0,20)
	l2 = random.randint(0,20)
	l3 = random.randint(0,20)
	l4 = random.randint(0,20)
	val = [0,0,0,0]
	if s1 == 0:
		val[0] = 3
	elif s1 == 1:
		val[0] = 10
	elif s1 == 2:
		val[0] = 20

	if s2 == 0:
		val[1] = 3
	elif s2 == 1:
		val[1] = 10
	elif s2 == 2:
		val[1] = 20

	if s3 == 0:
		val[2] = 3
	elif s3 == 1:
		val[2] = 10
	elif s3 == 2:
		val[2] = 20

	if s4 == 0:
		val[3] = 3
	elif s4 == 1:
		val[3] = 10
	elif s4 == 2:
		val[3] = 20

	val[0] = val[0] + l1
	val[1] = val[1] + l2
	val[2] = val[2] + l3
	val[3] = val[3] + l4

	if val[0] < 5:
		s1 = 0
	elif val[0] < 15:
		s1 = 1
	elif val[0] >14:
		s1 = 2

	if val[1] < 5:
		s2 = 0
	elif val[1] < 15:
		s2 = 1
	elif val[1] >14:
		s2 = 2

	if val[2] < 5:
		s3 = 0
	elif val[2] < 15:
		s3 = 1
	elif val[2] >14:
		s3 = 2

	if val[3] < 5:
		s4 = 0
	elif val[3] < 15:
		s4 = 1
	elif val[3] >14:
		s4 = 2

	return(s1,s2,s3,s4)

def actionSelection(EPSILON,i):
	if EPSILON < (random.randint(0,100)/100):
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

def determineTrafficState(S1,S2,S3,S4,t1,t2,t3,t4):
	#something here
	for i in range(len(df['state'])):
#		print(df['state'][i])
#		print([t1,S1,t2,S2,t3,S3,t4,S4])
		if df['state'][i] == [t1,S1,t2,S2,t3,S3,t4,S4]:
			return(i)
	print("Lafda hai kuch")

def reduceTraffic(s1,s2,s3,s4,t1,t2,t3,t4):

	val = [0,0,0,0]
	if s1 == 0:
		val[0] = 3
	elif s1 == 1:
		val[0] = 10
	elif s1 == 2:
		val[0] = 20

	if s2 == 0:
		val[1] = 3
	elif s2 == 1:
		val[1] = 10
	elif s2 == 2:
		val[1] = 20

	if s3 == 0:
		val[2] = 3
	elif s3 == 1:
		val[2] = 10
	elif s3 == 2:
		val[2] = 20

	if s4 == 0:
		val[3] = 3
	elif s4 == 1:
		val[3] = 10
	elif s4 == 2:
		val[3] = 20

	val[0] = val[0] - t1*10/2
	val[0] = val[0] - random.randint(-5,5)
	val[1] = val[1] - t2*10/2
	val[1] = val[1] - random.randint(-5,5)
	val[2] = val[2] - t3*10/2
	val[2] = val[2] - random.randint(-5,5)
	val[3] = val[3] - t4*10/2
	val[3] = val[3] - random.randint(-5,5)

	if val[0] < 5:
		s1 = 0
	elif val[0] < 15:
		s1 = 1
	elif val[0] >14:
		s1 = 2

	if val[1] < 5:
		s2 = 0
	elif val[1] < 15:
		s2 = 1
	elif val[1] >14:
		s2 = 2

	if val[2] < 5:
		s3 = 0
	elif val[2] < 15:
		s3 = 1
	elif val[2] >14:
		s3 = 2

	if val[3] < 5:
		s4 = 0
	elif val[3] < 15:
		s4 = 1
	elif val[3] >14:
		s4 = 2

	return(s1,s2,s3,s4)

def determineReward(s1,s2,s3,s4,S1,S2,S3,S4):
	old_score = S1*S1+S2*S2+S3*S3+S4*S4
	new_score = s1*s1+s2*s2+s3*s3+s4*s4
	print("New Reward to store: ")
	print(old_score - new_score)
	return(old_score - new_score)

def updateRewardValue(reward, currentState, action):
	print(currentState)
	print(action)
	print("Reward Updated at action", str(A[action]), "and state", str(df.at[currentState,'state']))
	df.at[currentState,str(A[action])]=(reward*GAMMA)

#traffic density is a permutaion of Low, Medium and High
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

#print(len(S))
#S_A_R = S
#NumberOfStates = len(S_A_R)
#LengthOfState = len(S_A_R[0])
#for i in range(len(S)):
#	S_A_R[i].append(A)
#	Rewards.append(R)
	
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

s1 = 0
s2 = 0
s3 = 0
s4 = 0

t1 = 1
t2 = 1
t3 = 1
t4 = 1

#print(len(df['state']))
epoch = 10000
for ep in range(epoch):
	S1,S2,S3,S4 = generateNewTrafficState(s1,s2,s3,s4)
	currentState = determineTrafficState(S1,S2,S3,S4,t1,t2,t3,t4)
	action = actionSelection(EPSILON,currentState)
	[t1,t2,t3,t4] = A[action]
	s1,s2,s3,s4 = reduceTraffic(S1,S2,S3,S4,t1,t2,t3,t4)
	reward = determineReward(s1,s2,s3,s4,S1,S2,S3,S4)
	df.at[currentState,str(A[action])]=(reward*GAMMA)
	updateRewardValue(reward, currentState, action)
	EPSILON = EPSILON + END_EPSILON/epoch
	#print(df)

print(df)























#-----------------------------------------------------------------Retrieve info at lanes-----------------------------------------------------------

#LANE 1
s1 = 1
#LANE 2
s2 = 2
#LANE 3
s3 = 1
#LANE 4
s4 = 0

#GREEN TIME 1
t1 = 1
#GREEN TIME 2
t2 = 1
#GREEN TIME 3
t3 = 1
#GREEN TIME 3
t4 = 1

#__________________________________________________________________________________________________________________________________________________

#------------------------------------------------------------------REWARD Determination and STATE changing-------------------------------------------------

#REWARD
currentScore = (8 - (s1 + s2 + s3 + s4 ))/8

#GET THE NEW STATES
#LANE 1
s_1 = 1
#LANE 2
s_2 = 2
#LANE 3
s_3 = 1
#LANE 4
s_4 = 0


#___________________________________________________________________________________________________________________________________________________

#-------------------------------------------------------------------CHOSE ACTION--------------------------------------------------------------------


#___________________________________________________________________________________________________________________________________________________

#-------------------------------------------------------------------UPDATE REWARD-------------------------------------------------------------------


#___________________________________________________________________________________________________________________________________________________














def chose_action(stae, q_table):
	#we chose an action
	state_action = q_table.iloc[state, :]
	EPSILON = generate_EPSILON(EPSILON)
	if (np.random.uniform() > EPSILON):
		action_name = np.random.choice(ACTIONS)
	else:
		action_name = state_actions.idmax()
	return action_name 