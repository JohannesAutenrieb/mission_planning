#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:10:26 2019


"""

class Agent():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentId,agentStatus,agentPos,agentBattery):
        
        self.agentId = agentId
        self.agentStatus = agentStatus
        self.agentPos = agentPos
        self.agentBattery = agentBattery

    def get_timestamp(self):
        print('Test Output timestamp :', self.timestamp)

    def get_agentIdx(self):
        print('Test Output agentIdx :', self.agentIdx)

    def get_taskType(self):
        print('Test Output taskType :', self.taskType)

    def get_wayPointLocation(self):
        print('Test Output wayPointLocation :', self.wayPointLocation)

    def get_taskDeadline(self):
        print('Test Output taskDeadline :', self.taskDeadline)