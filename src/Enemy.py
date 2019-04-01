class Enemy():

    # Defined States in the Mission State Machine
    def __init__(self, agentId, agentPos, agentVel, confidence):
        
        self.timeframe=10
        
        self.agentId = agentId
        self.agentPos = agentPos
        self.agentVel = agentVel
        self.agentFuturePositon = self.get_futurePosition()
        self.confidence = confidence
        self.attackStatus = False


    # Getter Functions
    def get_futurePosition(self):
        return ((self.agentPos[0]+self.agentVel[0]*self.timeframe), (self.agentPos[1]+self.agentVel[1]*self.timeframe), (self.agentPos[2]+self.agentVel[2]*self.timeframe))
    
    
    def get_agentId(self):
        return self.agentId

    def get_agentPos(self):
        return self.agentPos

    def get_confidence(self):
        return self.confidence

    def get_attackStatus(self):
        return self.attackStatus

    # setter Functions
    def set_agentId(self, agentId):
        self.agentId = agentId

    def set_agentPos(self, agentPos):
        self.agentPos = agentPos

    def set_confidence(self, confidence):
        self.confidence = confidence

    def set_attackStatus(self, attackStatus):
        self.attackStatus = attackStatus

