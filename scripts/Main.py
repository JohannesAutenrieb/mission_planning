#!/usr/bin/env python2.7

from MissionStateMachine import MissionStateMachine, MissionState
from StageOne import MissionStageOne
from StageThree import MissionStageThree
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from Task import Task, TaskType
from TaskAllocation_MAA import TaskAllocation_MAA
from Agent import Agent
from Enemy import Enemy
import datetime
import time
import rospy
import os
from mission_planning.msg import TaskMessage,TargetInformation, SwarmInfo

class MissionExecution():
    
    def __init__(self):
        
        """
        ===========================================================
        Constructor to create initial relevant Objects and global 
        Variables
        ===========================================================
        :Parameters: None
        	:return: None
        ===========================================================
        """

        print(":::: MISSION INITIALIZATION :::: ")

        # take initial time
        self.startTime = time.time()
        
        #Mission Stage Times in seconds (currently not real time)
        self.TotalMissionTime = 200
        self.StageThreeTime = 120
        self.MaximumStageTwoTime = self.TotalMissionTime - self.StageThreeTime
        
        #State object to handle the states with initial state one
        self.obj = MissionState(state='stageOne')
        
        #state machine instance to handle the main state machine
        self.mission = MissionStateMachine(self.obj)   
        self.stageOneState= MissionStageOne()
        self.stageThreeState= MissionStageThree()
        self.taskAllocation = TaskAllocation_MAA()
        
        #Set up of initial state status (inital state one)
        self.StageOneCompleted =False
        self.StageThreeCompleted =False
        self.MissionDone = False

        # Defining the input data containers for friends:
        self.agentsList = []
        self.fooList = []
        self.taskList = []

        # Define the input data containers for foos:
        self.fooId = []
        self.fooPos = []
        self.fooTimestamp = [] 
        
        # Init of ROS Talker
        self.pub = rospy.Publisher('TaskAction', TaskMessage, queue_size=10)
        
        # INITIAL OPEN OF LOG FILE
        self.f = open(self.getRelativeFilePath("MissionPlan/SwarmInfoLog.txt"), 'a')

    def __del__(self):
       print(":::::::DECONSTRUCT MAIN SYTSTEM")
       # CLOSE LOG FILE AGAIN
       self.f.close()
       print(":::::::LOG FILE IS CLOSED")

    def callbackSwarmInfo(self, msg):
        """
        ==============================================================
        Callback Function on receiving Swarm Informaion Data
        ===========================================================
        :Parameters: SwarmInfo ROS Message
    	
        :return: None
        ===========================================================
        """

        # Extract friends information from message
        dataFriend = msg.friendlies
        # WRITE TO FILE

        self.f.write("Friend data %s:\n" % rospy.get_time())

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
                setattr(self.agentsList[idx], 'agentWorkingStatus', dataFriend[i].agentWorkingStatus)
                setattr(self.agentsList[idx], 'agentPosi', dataFriend[i].agentPosition)
                setattr(self.agentsList[idx], 'agentHeading', dataFriend[i].agentHeading)
                setattr(self.agentsList[idx], 'taskID', dataFriend[i].agentTaskId)
                setattr(self.agentsList[idx], 'taskStatus', dataFriend[i].agentTaskStatus)
                setattr(self.agentsList[idx], 'agentBattery', dataFriend[i].agentBattery)
                setattr(self.agentsList[idx], 'agentPayload', dataFriend[i].agentPayload)
                
                # LOGING FOR VERFICATION
                self.f.write("Agent ID: %d \n" % dataFriend[i].agentId)
                self.f.write("Position: %6.4f %6.4f %6.4f \n" % dataFriend[i].agentPosition)
                self.f.write("Heading: %6.4f \n" % dataFriend[i].agentHeading)
                self.f.write("Task ID: %d \n" % dataFriend[i].agentTaskId)
                self.f.write("Task status %d \n" % dataFriend[i].agentTaskStatus)
                self.f.write("Battery %3.2f \n" % dataFriend[i].agentBattery)
                self.f.write("Working status %d \n\n" % dataFriend[i].agentWorkingStatus)

        # Extract foos information from message
        dataFoo = msg.enemies
        self.f.write("Foo data %s:\n" % rospy.get_time())

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
                self.fooList.append(Enemy(dataFoo[i].agentId, dataFoo[i].agentPosition, dataFoo[i].agentVelocity, dataFoo[i].confidence))
            # Else update agent attributes
            else:
                # Find index of agent with given Id in the friendsList
                idx = None
                for e in self.fooList:
                    if e.agentId == dataFoo[i].agentId:
                        idx = self.fooList.index(e)
                        break
                setattr(self.fooList[idx], 'agentId', dataFoo[i].agentId)
                setattr(self.fooList[idx], 'agentPos', dataFoo[i].agentPosition)
                setattr(self.fooList[idx], 'agentVel', dataFoo[i].agentVelocity)
                setattr(self.fooList[idx], 'confidence', dataFoo[i].confidence)
                
                # LOGING FOR LATER VERIFICATION
                self.f.write("Agent ID: %d \n" % dataFoo[i].agentId)
                self.f.write("Position: %6.4f %6.4f %6.4f \n" % dataFoo[i].agentPosition)
                self.f.write("Velocity: %6.4f %6.4f %6.4f \n" % dataFoo[i].agentVelocity)
                self.f.write("Confidence: %3.2f \n" % dataFoo[i].confidence)
                
    def missionState(self):
        """
        	==============================================================
         High Level statemachine of the Task Allocation System. In This Function
         high Level Statemachine is executed and the ROS Messages for
         each assigned task of the agents is send. 
        	==============================================================
         :Parameters: None	
         :return: Missiondone (bool) -	 only when the Mission time is over
         ===========================================================
        """

    
        # Set current time for this loop run
        self.currentTime = time.time()
	    #================================================================
	    # MAIN STATE MACHINE PART
	    #================================================================

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
                
        #================================================================
        # TASK MESSAGES SENDING
        #================================================================
        # Here the defined tasks are send as ROS Messages

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
            #clear taesk lsit for next time step
            del self.taskList[:]
        # Wait for 1 sec before goig to next execution
        print "MS::Length of TaskList: %d" % len(self.taskList)


    def getRelativeFilePath(self, relativePath):

        scriptDir = os.path.dirname(__file__)
        absFilePath = os.path.join(scriptDir, relativePath)
        return absFilePath



if __name__ == "__main__":
    """
    ==============================================================
    Main Loop of Task Allocation Software Loop
    ==============================================================
    :Parameters: None
	
    :return: None
    ==============================================================
    """

    print(":::: NODE INITIALIZATION :::: ")

    # Setup of Mission Statemachine
    missionExecution = MissionExecution()
    # Init of ROS Listener Node
    rospy.init_node('TaskAllocation', anonymous=True)  
    # Init Listener for friend and foos
    rospy.Subscriber("SwarmInformation", SwarmInfo, missionExecution.callbackSwarmInfo)

    # spin() simply keeps python from exiting until this node is stopped
    rate = rospy.Rate(1)

    print("::::: MISSION START ::::: ")
    while not rospy.is_shutdown() and not missionExecution.MissionDone:
        missionExecution.missionState()
        rate.sleep()
        
    




