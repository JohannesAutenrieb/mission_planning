
class Agent():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentId, agentPos, agentHeading, taskID, taskStatus, agentBattery, agentPayload):
        """
        ===========================================================
        Constructor to create initial relevant Objects and global 
        Variables of Agent instance
        ===========================================================
        :Parameters: None
         The Agents object is represented by a set of parameters:
              - AgentID (uint32)
              - AgentPosition ([3] List of float64)
              - AgentVelocity ([3] List of float64)
              - AgentHeading (float64)
              - AgentBattery (float64)
              - AgentPayload (bool)
        :return: None
        ===========================================================
        """       
        self.agentId = agentId
        self.agentPos = agentPos
        self.agentHeading = agentHeading
        self.taskID = taskID
        self.taskStatus = taskStatus
        self.agentBattery = agentBattery
        self.agentPayload = agentPayload
        self.agentWorkingStatus = True
        self.lastReward = 0
