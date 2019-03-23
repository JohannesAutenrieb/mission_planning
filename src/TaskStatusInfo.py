#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

class TaskStatusInfo():
    
    def __init__(self, taskType, agentId, targetId, initialPosition, currentPosition, wayPoint, taskDeadline, timestamp):


        self.taskType = taskType
        self.agentId = agentId
        self.targetId = targetId
        self.agentTaskStatus = False
        self.systemWorkingStatus = True
        self.initialPosition = initialPosition
        self.currentPosition = currentPosition
        self.wayPoint = wayPoint
        self.lastReward = 0
        self.taskDeadline = taskDeadline
        self.timestampOfTask = timestamp

        