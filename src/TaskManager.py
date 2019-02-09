from Agent import Agent
import math

class TaskManager():
    
    def __init__(self,numberOfAgents):
        #To-DO
        
        # ROS PArt in which all information of the swarm should been recieved and stored
        
        #listen Initial ROS message
        
        listOfAgents = []
        listOfTasks = []
        
#        for count in range(0, numberOfAgents):
#            x = Agent()
#            listOfAgents.append(x)
#            print(count)      
      
    def updateAgentData(self):
        # Step 1: listen to ROS
        # TO-DO
        print('On enter yellow')
        # Step 2: update list of agents
        # TO-DO

    def taskProgress(self):
        
        print('Task Progress started')
        # Loop over all agents and check progess
#        for AgentListidX in range(0, len(listOfAgents)):
#            for TaskListidX in range(0, len(listOfTasks)):
#               currentReward = computeExecutionReward(listOfAgents[].agentPos, listOfTasks[].wayPointLocation)
#               currentRewardSlope = currentReward/timestep
#               if currentRewardSlope<Threshold
#                     assign task new and trigger systemCheckprocedure or land\restart
#                     print(count)
#               else:
#                  listOfTasks[].setLastReward(currentReward) 
#               
        
    def sendEmergencyMessage(self):
        print('On enter yellow')

    def computeExecutionReward(self, agentPos, TaskWaypoint):
        print('On enter yellow')
        reward = math.sqrt((agentPos[0]-TaskWaypoint[0])**2 + (agentPos[1]-TaskWaypoint[1])**2 + (agentPos[2]-TaskWaypoint[2])**2)
        return reward

    def sendAbortMessage(self):
        print('On enter yellow')
        # send message through ROS
        