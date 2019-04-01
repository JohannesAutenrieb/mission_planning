#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from StageThreeStateMachine import StageThreeStateMachine, StageThreeState
from Task import Task,TaskType
import time


class MissionStageThree():

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
        """
        ===========================================================
        Stage Three Statemachine function which is executing the
        initial static mission steps
        ===========================================================
        :Parameters: 
            - AgentsList: 
              A list which contains a lits of Agents obejct.The Agents object
              represents a real entity and contains information about: 
                  AgentID
                  AgentPosition
                  AgentVelocity
                  TaskStatus
                  TaskID
                  SystemWorkingStatus
                  
        
                
            - FoosList:
              A list which contains a lits of target obejct.The foo object
              represents a real targets and contains information about: 
                  TargetID
                  TargetPosition
                  AgentVelocity
                  AttackkStatus
                  Confidence
              
            - TaskList:
              A list which contains a lits of task obejct.The task object
              object contains information of assigend tasks:
                  AgentID
                  TagetID
                  TaskID
                  TaskLocation/Waypoint
                  TaskDeadLine
                
        	:return: None
        ===========================================================
        """
        
        if self.obj.state == 'hoverAtCurrentPosition':
            
           # ======== Entry ========
           if not (self.EntryHover):
           # Hover State
               time.sleep(5)
               self.EntryHover = True
               return

        	   # ====Main Part ========
           print("S3: Agents hovering...")
           hoverTimeReached = True
           time.sleep(2)
           
           # ===== Exit ========		
           if (hoverTimeReached):
               #execute statemachine transition with trigger
               self.mission.hoverTimeReached()
               #Set time new to restart the countdown
               
        elif self.obj.state == 'goToWaypoint':

	       # ======== Entry ========
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
           
            # ====Main Part ========
           print("S3: Agents going to waypoint...")
           reachedAOI = self.allAgentsFinishedTask(agentsList)
           time.sleep(2)
           
           # ===== Exit ========
           if (reachedAOI):
                #execute statemachine transition with trigger
                self.mission.reachedAOI()

                
        elif self.obj.state == 'landInAOI':
            
	      # ======== Entry ========
           if not (self.EntryLandInAOI):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               deadline = 180
               for i in range(0, len(agentsList)):
                   TaskList.append(Task(agentsList[i].agentId, 0, TaskType.LAND.value,[1, 1, 1],deadline))
                   print "S3: Land order send to agent: %d" % agentsList[i].agentId
               self.EntryLandInAOI = True
               return
           
            # ====Main Part ========
           touchedGround = self.allAgentsFinishedTask(agentsList)
           time.sleep(2)
           
           # ===== Exit ========
           if (touchedGround):
                #execute statemachine transition with trigger
                self.mission.touchedGround()

        elif self.obj.state == 'waitOnGround':
            
	      # ======== Entry ========
           if not (self.EntryWaitOnGround):
           # Wait on Ground
               time.sleep(5)                
               self.EntryWaitOnGround = True
               return
           
           # ====Main Part ========
           # System Turnsoff automaticly when landed therefore the flag just
           # set True
           timeToTurnOff = True
           time.sleep(2)
           
           # ===== Exit ========
           if (timeToTurnOff):
                print("End of the mission")
                self.StageDone = True
                return self.StageDone


    def getRelativeFilePath(self, relativePath):
        """
        ==============================================================
        Function to setup correct abolute path for rading the .txt file 
        for predefined agent positions
        ===========================================================
        :Parameters:
            - relativePath: String which contains the relative path of
              file
    	
        :return: absFilePath - absolute file path for further use
        ===========================================================
        """       

        scriptDir = os.path.dirname(__file__)
        absFilePath = os.path.join(scriptDir, relativePath)
        return absFilePath

    def allAgentsFinishedTask(self,agentsList):
        """
        ==============================================================
        Function to recognize if all agents are free for new task in
        order to go further to next state of the statemachine
        ===========================================================
        :Parameters:
            - AgentsList: 
              A list which contains a lits of Agents obejct.The Agents object
              represents a real entity and contains information about: 
                  AgentID
                  AgentPosition
                  AgentVelocity
                  TaskStatus
                  TaskID
                  SystemWorkingStatus
    	
        :return: True if all finished - False if still agents in work
        ===========================================================
        """
        for i in range(0, len(agentsList)):
            if(agentsList[i].taskStatus is True) and (agentsList[i].agentWorkingStatus is True):
                return False
        return True
