#!/usr/bin/env python3.6

from MissionStateMachine import MissionStateMachine, MissionState
from StageOne import MissionStageOne
from StageThree import MissionStageThree
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from Task import Task, TaskType
from TaskAllocation import TaskAllocation
import datetime
#from PyQt5 import QtCore
#import sys
import rospy
from std_msgs.msg import String
from mission_planning.msg import TaskList

class MissionExecution():
    
    def __init__(self):
        
        # ----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        # ----------------------------------------------------------------------
    
        # take initial time
        self.startTime = datetime.datetime.now().timestamp()
        
        #Mission Stage Times in seconds (currently not real time)
        self.TotalMissionTime = 150
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
        self.StageOneCompleted =False
        self.StageThreeCompleted =False
        self.MissionDone = False
        
        
        
        # Define the input data containers for friends:
        self.currentFriendsInformation = FriendStatus()
        self.currentEnemyInformation= EnemyStatus()
        self.taskList = []

        # Define the input data containers for foos:
        self.fooId = []
        self.fooPos = []
        self.fooTimestamp = [] 
        
        # Init of ROS Talker
        self.pub = rospy.Publisher('SytstemArch', TaskList, queue_size=10)
        
    



#        self. rospy.Subscriber("chatter", String, callback)

    def callback(self,data):
        #operation on recieved data
#        print(data.data)
        
        #REceived Friend Information
        setattr(self.currentFriendsInformation, 'friendlyId', data.friendlyId) 
        setattr(self.currentFriendsInformation, 'friendlyStatus', data.friendlyStatus)
        setattr(self.currentFriendsInformation, 'friendlyPos', data.friendlyPos)
        setattr(self.currentFriendsInformation, 'friendlyBatt', data.friendlyBatt)
        setattr(self.currentFriendsInformation, 'friendlyTimestamp', data.friendlyTimestamp)


        #Received Foo information  
        setattr(self.currentEnemyInformation, 'fooId', data.fooId) 
        setattr(self.currentEnemyInformation, 'fooPos', data.fooPos)
        setattr(self.currentEnemyInformation, 'fooTimestamp', data.fooTimestamp)
        



    def missionState(self):

            # ----------------------------------------------------------------------
            # READING PART: In This Part the Messages AND Parameters Are Read
            # ----------------------------------------------------------------------
    
            # Here the parameters have to be read
    
            # ----------------- TO - DO -------------------------------------------
    
            # ----------------------------------------------------------------------
            # EXECUTION PART: In This Part The State Machine is Running
            # ----------------------------------------------------------------------
            print("length of TaskList", len(self.taskList))
    
            # Set current time for this loop run
            self.currentTime = datetime.datetime.now().timestamp()
            # Step : Go in to the State Machine and Execute relevant features
    
            if self.obj.state == 'stageOne':
    
    	   # To-Do as long as in current State
               print ("1 - Stage One Entered")
               #Execute Stage One State Machine and return Boolean if executed
               self.StageOneCompleted = self.stageOneState.StageOne(self.currentFriendsInformation, self.currentEnemyInformation, self.taskList)
               #print ("Status:", StageOne())
    	   # Execution of Transition Check and Exit of current State	
               if (self.StageOneCompleted):
                   #execute statemachine transition with trigger
                   print ("Switch Bitch")
                   self.mission.triggerOne()
                   
            elif self.obj.state == 'stageTwo':
    
    	   # To-Do as long as in current State
               print ("2 - Got a true expression value")
               self.taskAllocation.TaskAllocation(self.currentFriendsInformation, self.currentEnemyInformation, self.taskList)
               
               # Execution of Transition Check and Exit of current State
               if (((self.currentTime-self.startTime)>=self.MaximumStageTwoTime)):
                    #execute statemachine transition with trigger
                     self.mission.triggerTwo()
                    
            elif self.obj.state == 'stageThree':
    	   # To-Do as long as in current State
               print ("3 - Stage Three entered")
               
               self.StageOneCompleted = self.stageThreeState.StageThree(self.currentFriendsInformation, self.currentEnemyInformation, self.taskList)
               
               # Execution of Transition Check and Exit of current State
               if (self.StageThreeCompleted):
                    print ("We are done with the Mission")
                    MissionDone = True
                    # Let's go and drink a beer
                    return MissionDone
                    
            #----------------------------------------------------------------------
    
    
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            # ----------------------------------------------------------------------
    
            # Here the variables have to be send to external processes and agents
            #
            #--- Handle Task before
            #self.TaskList    
            #self.pub.publish(self.TaskList)
            
            if not len( self.taskList)==0:
                for  i in range(0, len( self.taskList)):
                    msg = TaskList()
                    print ("Task Message:")
                    print(self.taskList[i].agentIdx)
                    print(self.taskList[i].taskType.value)
                    print("Posi type:", type(self.taskList[i].wayPointLocation[0]))
                    print(self.taskList[0].wayPointLocation)
                    msg.agentIdx =  self.taskList[i].agentIdx
                    msg.TaskType = self.taskList[i].taskType.value
                    msg.position = self.taskList[i].wayPointLocation
                    msg.timestamp = datetime.datetime.now().timestamp()
                   
                    self.pub.publish(msg)
                    #clear message object
                    del msg
                #clear taesk lsit for next time step
                self.taskList.clear()
            # Wait for 1 sec before goig to next execution    

if __name__ == "__main__":
    print("Its Me bitch")
    
    # Setup of Mission Statemachine
    missionExecutaion = MissionExecution()
    
    # Init of ROS Listener Node
    rospy.init_node('TaskAllocation', anonymous=True)
    
    # spin() simply keeps python from exiting until this node is stopped
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        missionExecutaion.missionState()
        rate.sleep()
        
    




