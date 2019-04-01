import time
from enum import Enum

class TaskType(Enum):
    """
    ===========================================================
    Enum Structure Class for different Task Types
    ===========================================================
    """  
    TAKEOFF = 1
    WAYPOINT = 2
    PRELEASE = 3
    LAND = 4
    ABORTMISSION = 5
    RECOVERY= 6
    SYSTEMCHECK = 7
    ATTACK = 8 

class Task():
    """
    ===========================================================
    Task Class which represents a task object
    ===========================================================
    """     
    # Defined States in the Mission State Machine
    def __init__(self,agentIdx,targetId, taskType,wayPointLocation,taskDeadline):
        """
        ===========================================================
        Constructor to create initial relevant Objects and global 
        Variables of Agent instance
        ===========================================================
        :Parameters: None
         The Agents object is represented by a set of parameters:
              - agentIdx (uint32)
              - targetId (uint32)
              - wayPointLocation ([3] List of float64)
              - taskDeadline (float64)
        :return: None
        ===========================================================
        """  
        
        self.timestamp = time.time()
        self.agentIdx = agentIdx
        self.targetId = targetId
        self.taskType = taskType
        self.wayPointLocation = wayPointLocation
        self.taskDeadline = taskDeadline

class InitMsg():
    """
    ===========================================================
    Init Message Class which represents a init message object
    ===========================================================
    """   
    # Initialization message with home location
    def __init__(self, agentIdx, homeLocation):
        """
        ===========================================================
        Constructor to create initial relevant Objects and global 
        Variables of Agent instance
        ===========================================================
        :Parameters: None
         The Agents object is represented by a set of parameters:
              - agentIdx (uint32)
              - targetId (uint32)
              - homeLocation ([3] List of float64)
        :return: None
        ===========================================================
        """  

        self.agentIdx = agentIdx
        self.homeLocation = homeLocation