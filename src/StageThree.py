#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from StageThreeStateMachine import StageThreeStateMachine, StageThreeState
from Task import Task
import time


class MissionStageThree():

    def __init__(self):

    
        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
    
        #State object to handle the states with initial state one
        self.obj = StageThreeState(state='hoverAtCurrentPosition')
        #state machine instance to handle the main state machine
        self.mission = StageThreeStateMachine(self.obj)
        
        # Entry Trigger
        self.EntryHover = False 
        self.EntryGoToWaypoint = False
        self.EntryLandInAOI = False
        self.EntryWaitOnGround = False
        self.EntryTurnMotorsOff = False
        self.Entry = False
        self.Entry = False
        self.Entry = False
        
        

    def StageThree(self, currentFriendsInformation, currentEnemyInformation, TaskList):

        
     
        #----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the parameters have to be read

        # ----------------- TO - DO -------------------------------------------
        
        #----------------------------------------------------------------------
        # EXECUTION PART: In This Part The State Machine is Running
        #----------------------------------------------------------------------
        
        #Set current time for this loop run
        #Step : Go in to the State Machine and Execute relevant features
        
        if self.obj.state == 'hoverAtCurrentPosition':
            
           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   self.Task = Task(currentFriendsInformation.friendlyId[i],5,[None]*3)
                   TaskList.append(self.Task)
                   del self.Task
                   
               self.EntryStartMotor = True
               return

	   # To-Do as long as in current State
           print ("S3 - Hover at current Position")
           hoverTimeReached = True
           time.sleep(2)
	   # Execution of Transition Check and Exit of current State	
           if (hoverTimeReached):
               #execute statemachine transition with trigger
               self.mission.hoverTimeReached()
               #Set time new to restart the countdown
               
        elif self.obj.state == 'goToWaypoint':

	   # To-Do as long as in current State
           print ("S3 - Go to Waypoint")
           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   self.Task = Task(currentFriendsInformation.friendlyId[i],5,[None]*3)
                   TaskList.append(self.Task)
                   del self.Task
                   
               self.EntryStartMotor = True
               return
           
           reachedAOI = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (reachedAOI):
                #execute statemachine transition with trigger
                self.mission.reachedAOI()

                
        elif self.obj.state == 'landInAOI':
	   # To-Do as long as in current State
           print ("S3 - Land in AOI")
           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   self.Task = Task(currentFriendsInformation.friendlyId[i],5,[None]*3)
                   TaskList.append(self.Task)
                   del self.Task
                   
               self.EntryStartMotor = True
               return
           touchedGround = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (touchedGround):
                print ("We touched the ground in AOI")
                #execute statemachine transition with trigger
                self.mission.touchedGround()

        elif self.obj.state == 'waitOnGround':
	   # To-Do as long as in current State
           print ("S3 - Wait on Ground")
           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   self.Task = Task(currentFriendsInformation.friendlyId[i],5,[None]*3)
                   TaskList.append(self.Task)
                   del self.Task
                   
               self.EntryStartMotor = True
               return
           timeToTurnOff = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (timeToTurnOff):
                print ("Time to wait is over")
                #execute statemachine transition with trigger
                self.mission.timeToTurnOff()

        elif self.obj.state == 'TurnMotorsOff':
	   # To-Do as long as in current State
           print ("S3 - Turn motor off")
           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   self.Task = Task(currentFriendsInformation.friendlyId[i],5,[None]*3)
                   TaskList.append(self.Task)
                   del self.Task
                   
               self.EntryStartMotor = True
               return
           everthingShutDown = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (everthingShutDown):
                print ("Motor is turned off")
                #Set time new to restart the countdown
                return everthingShutDown
    
    
            #----------------------------------------------------------------------
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            #----------------------------------------------------------------------        
            
            # Here the variables have to be send to external processes and agents
            
            # ----------------- TO - DO -------------------------------------------
                    
    
            #----------------------------------------------------------------------
            # WAITING PART: Wait for 1 sec before goig to next execution 
            #----------------------------------------------------------------------


