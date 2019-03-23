class Enemy():

    # Defined States in the Mission State Machine
    def __init__(self, agentId, agentPos, confidence):
        self.agentId = agentId
        self.agentPos = agentPos
        self.confidence = confidence
        self.attackStatus = False
        self.attackingAgent = 0


    # Getter Functions
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

