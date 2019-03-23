#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from StageThreeStateMachine import StageThreeStateMachine, StageThreeState
from Task import Task,TaskType
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
        self.EntryStartMotor = False
        self.EntryHover = False 
        self.EntryGoToWaypoint = False
        self.EntryLandInAOI = False
        self.EntryWaitOnGround = False
        self.Entry = False
        self.Entry = False
        self.Entry = False

        self.StageDone = False
        
        

    def StageThree(self, agentsList, fooList, TaskList):

        
     
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
            
           if not (self.EntryHover):
           # Hover State
               time.sleep(5)
               self.EntryHover = True
               return

	   # To-Do as long as in current State
           print("S3: Agents hovering...")
           hoverTimeReached = True
           time.sleep(2)
	   # Execution of Transition Check and Exit of current State	
           if (hoverTimeReached):
               #execute statemachine transition with trigger
               self.mission.hoverTimeReached()
               #Set time new to restart the countdown
               
        elif self.obj.state == 'goToWaypoint':

	   # To-Do as long as in current State
           if not (self.EntryGoToWaypoint):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               deadline = 120
               f = open(self.getRelativeFilePath("MissionPlan/Stage_3_Attack.txt"))
               line = f.readlines(0)
               print("S3: Setting waypoints")
               for i in range(0, len(agentsList)):
                   waypoint = line[i].split(";")
                   del waypoint[-1] # delete last element with new line command 
                   waypoint = [int(x) for x in waypoint]              
                   TaskList.append(Task(agentsList[i].agentId, 0, TaskType.WAYPOINT.value,waypoint,deadline))
                   print "S3: Waypoint: {0} set for agent: {1}".format(waypoint, agentsList[i].agentId)
                   self.EntryGoToWaypoint = True
               f.close() 
               return

           print("S3: Agents going to waypoint...")
           reachedAOI = self.allAgentsFinishedTask(agentsList)
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (reachedAOI):
                #execute statemachine transition with trigger
                self.mission.reachedAOI()

                
        elif self.obj.state == 'landInAOI':
	   # To-Do as long as in current State
           if not (self.EntryLandInAOI):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               deadline = 180
               for i in range(0, len(agentsList)):
                   TaskList.append(Task(agentsList[i].agentId, 0, TaskType.LAND.value,[1, 1, 1],deadline))
                   print "S3: Land order send to agent: %d" % agentsList[i].agentId
               self.EntryLandInAOI = True
               return
           touchedGround = self.allAgentsFinishedTask(agentsList)
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (touchedGround):
                #execute statemachine transition with trigger
                self.mission.touchedGround()

        elif self.obj.state == 'waitOnGround':
	   # To-Do as long as in current State
           if not (self.EntryWaitOnGround):
           # Wait on Ground
               time.sleep(5)                
               self.EntryWaitOnGround = True
               return
           timeToTurnOff = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (timeToTurnOff):
                print("End of the mission")
                self.StageDone = True
                return self.StageDone

            #----------------------------------------------------------------------
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            #----------------------------------------------------------------------        
            
            # Here the variables have to be send to external processes and agents
            
            # ----------------- TO - DO -------------------------------------------
                    
    
            #----------------------------------------------------------------------
            # WAITING PART: Wait for 1 sec before goig to next execution 
            #----------------------------------------------------------------------

    def getRelativeFilePath(self, relativePath):

        scriptDir = os.path.dirname(__file__)
        absFilePath = os.path.join(scriptDir, relativePath)
        return absFilePath

    def allAgentsFinishedTask(self,agentsList):
    #Loop over all friends to see if all fullfiled task
        for i in range(0, len(agentsList)):
            if(agentsList[i].taskStatus is True) and (agentsList[i].agentWorkingStatus is True):
                return False
        return True
