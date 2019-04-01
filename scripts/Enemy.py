class Enemy():
    """
    ===========================================================
    Enemy Class which represents a target object
    ===========================================================
    """  
    # Defined States in the Mission State Machine
    def __init__(self, agentId, agentPos, agentVel, confidence):
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
              - Confidence (float64)
        :return: None
        ===========================================================
        """  
        # Timeframe for interpolation of target motion        
        self.timeframe=10
        
        # object information
        self.agentId = agentId
        self.agentPos = agentPos
        self.agentVel = agentVel
        self.agentFuturePositon = self.get_futurePosition()
        self.confidence = confidence
        self.attackStatus = False


    # Getter Functions
    def get_futurePosition(self):
        """
        ===========================================================
        Function which does a dead reckoning of the agents position
        in order to send a agent to a possible future position of
        the agent
        ===========================================================
        """  
        return ((self.agentPos[0]+self.agentVel[0]*self.timeframe), (self.agentPos[1]+self.agentVel[1]*self.timeframe), (self.agentPos[2]+self.agentVel[2]*self.timeframe))
    
    
