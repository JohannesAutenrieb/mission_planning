#!/usr/bin/env python2.7
import rospy
import math
from TaskStatusInfo import TaskStatusInfo
from Task import Task, TaskType
from Agent import Agent
import time
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from mission_planning.msg import TaskMessage, AgentInfo, SwarmInfo


class TaskManager():
    
    def __init__(self):
        # ROS Part in which all information of the swarm should been recieved and stored
        
        # Instance to store all relevant data regarding the current tasks
        # Task list for storing the tasks which needs to be sended
        self.taskList = []
        # Init of ROS Publisher for Task Messages
        self.pub = rospy.Publisher('TaskActions', TaskMessage, queue_size=1)
             
        #instance to store all relevant data regarding the current tasks
        self.currentFriendsInformation = FriendStatus()
        self.currentEnemyInformation = EnemyStatus()
        self.taskStatusList = []
        self.taskList = []
        self.agentsList = []
        self.fooList = []
#==========================================================================================================
#                                  Database Part  
#==========================================================================================================
        
   # Callback for adding new tasks to current Database
    def callbackTaskMessages(self, data):

        if (data.taskId == TaskType.ABORTMISSION.value):
            for task in self.taskStatusList:
                if data.agentId == task.agentId:
                    setattr(task, 'taskType', data.taskId)
        
        # If Agent is not already in task database
        if not any(data.agentId == task.agentId for task in self.taskStatusList):

            # Get agent index in the database
            friendIdx = None
            for i in range(0, len(self.agentsList)):
                if self.agentsList[i].agentId == data.agentId:
                    friendIdx = i
                    break

            # Receive and Process Task Information
            self.taskStatusList.append(TaskStatusInfo(data.taskId, data.agentId, data.targetId,
                                                      self.agentsList[friendIdx].agentPos, self.agentsList[friendIdx].agentPos,
                                                      data.taskLocation, data.taskDeadline, data.timestamp))

    def callbackSystemStatusAgent(self, data):
        #operation on Friend Information 
        print("System Status")
        for task in self.taskStatusList:
            if data.agentId == task.agentId:
                setattr(task, 'systemWorkingStatus', data.systemWorkingStatus)
                break


    def callbackFriend(self, data):

        # Extract friends information from message
        dataFriend = data.friendlies

        # Iter over list of messages
        for i in range(0, len(dataFriend)):
            # If agent is not on the list, append new agent object
            if not any(agent.agentId == dataFriend[i].agentId for agent in self.agentsList):
                self.agentsList.append(
                    Agent(dataFriend[i].agentId, dataFriend[i].agentPosition,
                          dataFriend[i].agentHeading, dataFriend[i].agentTaskId, dataFriend[i].agentTaskStatus,
                          dataFriend[i].agentBattery, dataFriend[i].agentPayload))
            # Else update agent attributes
            else:
                # Find index of agent with given Id in the friendsList
                idx = None
                for a in self.agentsList:
                    if a.agentId == dataFriend[i].agentId:
                        idx = self.agentsList.index(a)
                        break
                # Receive and Store Friend Information
                setattr(self.agentsList[idx], 'agentWorkingStatus', dataFriend[i].agentWorkingStatus)
                setattr(self.agentsList[idx], 'agentPos', dataFriend[i].agentPosition)
                setattr(self.agentsList[idx], 'agentHeading', dataFriend[i].agentHeading)
                setattr(self.agentsList[idx], 'taskID', dataFriend[i].agentTaskId)
                setattr(self.agentsList[idx], 'taskStatus', dataFriend[i].agentTaskStatus)
                setattr(self.agentsList[idx], 'agentBattery', dataFriend[i].agentBattery)
                setattr(self.agentsList[idx], 'agentPayload', dataFriend[i].agentPayload)

        # Erase element with: list.pop(ListIdx)
        for agent in self.agentsList:
            for task in self.taskStatusList:
                if agent.agentId == task.agentId:
                    if (agent.taskStatus is True) and (task.agentTaskStatus is False):
                        setattr(task, 'agentTaskStatus', True)
                        break
                    elif (agent.taskStatus is False) and (task.agentTaskStatus is True):
                        #self.taskList.remove(task)
                        self.taskStatusList.pop(self.taskStatusList.index(task))
                        break
                    else:
                        break
        
        # Update current position
        for i in range(0, len(dataFriend)):
            for task in self.taskStatusList:
                if dataFriend[i].agentId == task.agentId:
                    setattr(task, 'currentPosition', dataFriend[i].agentPosition)
                    break
#==========================================================================================================
#==========================================================================================================

    def computeExecutionReward(self, agentPos, TaskWaypoint, initialPostion):
        # reward = d-a/d min: -x to max: 1 (-x when agent is increasing the distance between its position and given waypoint)
        d = math.sqrt((TaskWaypoint[0]-initialPostion[0])**2 + (TaskWaypoint[1]-initialPostion[1])**2 + (TaskWaypoint[2]-initialPostion[2])**2)
        a = math.sqrt((TaskWaypoint[0]-agentPos[0])**2 + (TaskWaypoint[1]-agentPos[1])**2 + (TaskWaypoint[2]-agentPos[2])**2)
        reward = (d-a)/d
        return reward

    def sendAbortMessage(self,AgentListidX, tasklist):
        # send message through ROS
        tasklist.append(Task(AgentListidX, 0, TaskType.ABORTMISSION.value,[1, 1, 1],0))
        
    def sendSystemRequestMessage(self, AgentListidX, tasklist):
        # send message through ROS
        tasklist.append(Task(AgentListidX,0, TaskType.SYSTEMCHECK,[1, 1, 1],0))

    def taskProgress(self):

        # current time taking
        currentTime = time.time()
      
        # Loop over all tasks and check progess
        for task in self.taskStatusList:
            
           #Taking relevant time information
           timeOfAssignment = task.timestampOfTask
           taskDeadline = task.taskDeadline

           if (task.taskType == 2) or (task.taskType == 8):
               # compute rewards
               currentReward = self.computeExecutionReward(task.currentPosition, task.wayPoint, task.initialPosition)
               if (0.9*task.lastReward > currentReward):
                   #Assign System Check task to trigger system Checkprocedure or land\restart
                   # SystemStatus True means it is officaly ok while False means it is not okay
                   self.sendAbortMessage(task.agentId, self.taskList)
                   # set current task as last ## need to be adjusted for the index
                   setattr(task, 'lastReward', currentReward)
               print "T: [REWARD]Abort of Task ID: %d" % task.taskType
               print "T: [REWARD]Abort mission msg send to agent: %d" % task.agentId

           if ((currentTime-timeOfAssignment) > taskDeadline):
               #Assign System Check task to trigger system Checkprocedure or land\restart
               # SystemStatus True means it is officaly ok while False means it is not okay
               self.sendAbortMessage(task.agentId, self.taskList)
	       print "T: [TIMEOUT]Abort of Task ID: %d" % task.taskType
               print "T: [TIMEOUT]Abort mission msg send to agent: %d" % task.agentId
#               setattr(task, 'lastReward', currentReward)
   
               # Abort Mission if the system is not working 
           if not task.systemWorkingStatus:
               self.sendAbortMessage(task.agentId, self.taskList)
               print("T: [SYSTEMFAIL]Abort mission msg send to agent: ", task.agentId)

	# print out for updqte
	print("\nT: Rewards are updated for all tasks")
        
        # Message to the Agents due to problems
        if not len(self.taskList) == 0:

            print("\nT: Sending tasks to agents")
            for i in range(0, len(self.taskList)):
                print "MISSION VALUE = %d" % self.taskList[i].taskType
                msg = TaskMessage()
                msg.agentId = self.taskList[i].agentIdx
                msg.taskId = self.taskList[i].taskType
                msg.taskLocation = self.taskList[i].wayPointLocation
                msg.timestamp = time.time()
                print "T: Agent: {0} assigned to task: {1}".format(msg.agentId, msg.taskId)
                print "T: Waypoint: {0} sent at: {1}".format(msg.taskLocation, msg.timestamp)
                self.pub.publish(msg)
                #clear message object
                del msg
            #clear task lsit for next time step
            del self.taskList[:]

   
if __name__ == "__main__":
    print("T:: TASK MANAGER INITIALIZED ::")
    
    # Setup of Mission Statemachine
    taskSupervision = TaskManager()
    
    # Init of ROS Listener Node
    rospy.init_node('TaskManagement', anonymous=True)
    
    # Init Listener for friend and foos
    rospy.Subscriber("SwarmInformation", SwarmInfo, taskSupervision.callbackFriend)

    # Init Listener to Task Topic
    rospy.Subscriber('TaskActions', TaskMessage, taskSupervision.callbackTaskMessages)
    
    # Task Manger is executing all 30 seconds 0.0333333
    rate = rospy.Rate(0.04)
    
    while not rospy.is_shutdown():
        taskSupervision.taskProgress()
        rate.sleep()     
