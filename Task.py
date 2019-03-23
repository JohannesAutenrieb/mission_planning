import time
from enum import Enum

class TaskType(Enum):
    TAKEOFF = 1
    WAYPOINT = 2
    PRELEASE = 3
    LAND = 4
    ABORTMISSION = 5
    RECOVERY= 6
    SYSTEMCHECK = 7
    ATTACK = 8          #!!Clarify with GNC about Requeired behaviour (go to Waypoint and wait)!!

class Task():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentIdx,targetId, taskType,wayPointLocation,taskDeadline):
        
        self.timestamp = time.time()
        self.agentIdx = agentIdx
        self.targetId = targetId
        self.taskType = taskType
        self.wayPointLocation = wayPointLocation
        self.taskDeadline = taskDeadline

class InitMsg():

    # Initialization message with home location
    def __init__(self, agentIdx, homeLocation):

        self.agentIdx = agentIdx
        self.homeLocation = homeLocation