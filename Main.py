#!/usr/bin/env python2.7

from MissionStateMachine import MissionStateMachine, MissionState
from StageOne import MissionStageOne
from StageThree import MissionStageThree
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from Task import Task, TaskType
from TaskAllocation import TaskAllocation
from Agent import Agent
from Enemy import Enemy
import datetime
import time
import rospy
from mission_planning.msg import TaskMessage,TargetInformation, SwarmInfo

class MissionExecution():
    
    def __init__(self):
        
        # ----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        # ----------------------------------------------------------------------

        print(":::: MISSION INITIALIZATION :::: ")

        # take initial time
        self.startTime = time.time()
        
        #Mission Stage Times in seconds (currently not real time)
        self.TotalMissionTime = 500
        self.StageThreeTime = 120
        self.MaximumStageTwoTime = self.TotalMissionTime - self.StageThreeTime
        
        #State object to handle the states with initial state one
        self.obj = MissionState(state='stageOne')
        
        #state machine instance to handle the main state machine
        self.mission = MissionStateMachine(self.obj)   
        self.stageOneState= MissionStageOne()
        self.stageThreeState= MissionStageThree()
        self.taskAllocation = TaskAllocation()
        
        #Set up of initial state status (inital state one)
        self.StageOneCompleted = False
        self.StageThreeCompleted = False
        self.MissionDone = False

        # Define the input data containers for friends:
        # self.currentFriendsInformation = FriendStatus()
        # self.currentEnemyInformation = EnemyStatus()
        self.agentsList = []
        self.fooList = []
        self.taskList = []

        # Define the input data containers for foos:
        self.fooId = []
        self.fooPos = []
        self.fooTimestamp = [] 
        
        # Init of ROS Talker
        self.pub = rospy.Publisher('TaskActions', TaskMessage, queue_size=10)

    def callbackFriend(self, msg):
        #operation on recieved data
        #print(data.data)

        # Extract foos information from message
        dataFoo = msg.enemies

        # Search for enemies from the current list that are not in the updated list and remove them
        idxToDelete = []
        for i in range(0, len(self.fooList)):
            if not any(self.fooList[i].agentId == foo.agentId for foo in dataFoo):
                idxToDelete.append(i)
        for i in range(0, len(idxToDelete)):
            del self.fooList[i]

        # Iter over list of messages
        for i in range(0, len(dataFoo)):
            # If enemy is not on the list, append new enemy object
            if not any(foo.agentId == dataFoo[i].agentId for foo in self.fooList):
                self.fooList.append(Enemy(dataFoo[i].agentId, dataFoo[i].agentPosition, dataFoo[i].confidence))
            # Else update enemy attributes
            else:
                # Find index of agent with given Id in the friendsList
                idx = None
                for e in self.fooList:
                    if e.agentId == dataFoo[i].agentId:
                        idx = self.fooList.index(e)
                        break
                setattr(self.fooList[idx], 'agentId', dataFoo[i].agentId)
                setattr(self.fooList[idx], 'agentPos', dataFoo[i].agentPosition)
                setattr(self.fooList[idx], 'confidence', dataFoo[i].confidence)

        # Extract friends information from message
        dataFriend = msg.friendlies

        # Iter over list of messages
        for i in range(0, len(dataFriend)):
            # If agent is not on the list, append new agent object
            if not any(agent.agentId == dataFriend[i].agentId for agent in self.agentsList):
                self.agentsList.append(Agent(dataFriend[i].agentId, dataFriend[i].agentPosition, dataFriend[i].agentHeading, dataFriend[i].agentTaskId, dataFriend[i].agentTaskStatus, dataFriend[i].agentBattery, dataFriend[i].agentPayload))
            # Else update agent attributes
            else:
                # Find index of agent with given Id in the friendsList
                idx = None
                for a in self.agentsList:
                    if a.agentId == dataFriend[i].agentId:
                        idx = self.agentsList.index(a)
                        break
                # Change attack status of enemies
                self.changeEnemyAttackStatus(dataFriend[i], self.agentsList[idx])

                setattr(self.agentsList[idx], 'agentWorkingStatus', dataFriend[i].agentWorkingStatus)
                setattr(self.agentsList[idx], 'agentPosi', dataFriend[i].agentPosition)
                setattr(self.agentsList[idx], 'agentHeading', dataFriend[i].agentHeading)
                setattr(self.agentsList[idx], 'taskID', dataFriend[i].agentTaskId)
                setattr(self.agentsList[idx], 'taskStatus', dataFriend[i].agentTaskStatus)
                setattr(self.agentsList[idx], 'agentBattery', dataFriend[i].agentBattery)
                setattr(self.agentsList[idx], 'agentPayload', dataFriend[i].agentPayload)

    def changeEnemyAttackStatus(self, friendMsg, friendPrevious):
        if (friendMsg.agentTaskId == 0) and (friendPrevious.taskID == TaskType.ATTACK.value):
            # Find the foo that was attacked by this agent
            for foo in self.fooList:
                if foo.attackingAgent == friendPrevious.agentId:
                    # Change foo attack status
                    print "T: Foo %d attack status changed to False" % foo.agentId
                    setattr(foo, 'attackStatus', False)
                    setattr(foo, 'attackingAgent', 0)
                    break

    def missionState(self):

            # ----------------------------------------------------------------------
            # READING PART: In This Part the Messages AND Parameters Are Read
            # ---------------------------------------------------------------------- 
            # Here the parameters have to be read
            # ----------------- TO - DO -------------------------------------------
            # ----------------------------------------------------------------------
            # EXECUTION PART: In This Part The State Machine is Running
            # ----------------------------------------------------------------------
            #Dont do something unless you receive information from SA
            #if len(self.currentFriendsInformation.friendlyId)<=0:
                #return

    
            # Set current time for this loop run
            self.currentTime = time.time()
            # Step : Go in to the State Machine and Execute relevant features
    
            if self.obj.state == 'stageOne':
    
    	   # To-Do as long as in current State
               #Execute Stage One State Machine and return Boolean if executed
               self.StageOneCompleted = self.stageOneState.StageOne(self.agentsList, self.fooList, self.taskList)
               #print ("Status:", StageOne())
    	   # Execution of Transition Check and Exit of current State	
               if (self.StageOneCompleted):
                   #execute statemachine transition with trigger
                   print ("It's time to defend our assests Jedi! #MaytheForceBeWithYou")
                   self.mission.triggerOne()
                   
            elif self.obj.state == 'stageTwo':
    
    	   # To-Do as long as in current State
               self.taskAllocation.TaskAllocation(self.agentsList, self.fooList, self.taskList)
               
               # Execution of Transition Check and Exit of current State
               if (((self.currentTime-self.startTime)>=self.MaximumStageTwoTime)):
                    #execute statemachine transition with trigger
                    for agent in self.agentsList:
                        self.taskList.append(Task(agent.agentId, 0, TaskType.ABORTMISSION.value, [1,1,1], 0))
                    self.mission.triggerTwo()
                    
            elif self.obj.state == 'stageThree':
    	   # To-Do as long as in current State
               self.StageThreeCompleted = self.stageThreeState.StageThree(self.agentsList, self.fooList, self.taskList)
               
               # Execution of Transition Check and Exit of current State
               if (self.StageThreeCompleted):
                    print(":::: SYSTEM SHUTDOWN :::: ")
                    self.MissionDone = True
                    # Let's go and drink a beer
                    return self.MissionDone
                    
            #----------------------------------------------------------------------
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            # ----------------------------------------------------------------------
    
            # Here the variables have to be send to external processes and agents
            #
            #--- Handle Task before
            #self.TaskList    
            #self.pub.publish(self.TaskList)

            if not len(self.taskList) == 0:
                print("T: Sending tasks to agents")
                for i in range(0, len( self.taskList)):
                    msg = TaskMessage()
                    msg.agentId = self.taskList[i].agentIdx
                    msg.targetId = self.taskList[i].targetId
                    msg.taskId = self.taskList[i].taskType
                    msg.taskLocation = self.taskList[i].wayPointLocation
                    msg.taskDeadline = self.taskList[i].taskDeadline
                    msg.timestamp = time.time()
                    self.pub.publish(msg)
                    #clear message object
                    del msg
                # Wait for 1 sec before goig to next execution
                print "MS::Length of TaskList: %d" % len(self.taskList)
                #clear taesk lsit for next time step
                del self.taskList[:]


if __name__ == "__main__":

    print(":::: NODE INITIALIZATION :::: ")

    # Setup of Mission Statemachine
    missionExecution = MissionExecution()
    # Init of ROS Listener Node
    rospy.init_node('TaskAllocation', anonymous=True)  
    # Init Listener for friend and foos
    rospy.Subscriber("SwarmInformation", SwarmInfo, missionExecution.callbackFriend)

    # spin() simply keeps python from exiting until this node is stopped
    rate = rospy.Rate(1)

    print("::::: MISSION START ::::: ")
    while not rospy.is_shutdown() and not missionExecution.MissionDone:
        missionExecution.missionState()
        rate.sleep()
        
    




