
class Agent():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentId,agentStatus,agentPos, agentOrient,taskStatus,agentBattery, agentPayload):
        
        self.agentId = agentId
        self.agentStatus = agentStatus
        self.agentPos = agentPos
        self.agentOrient = agentOrient
        self.taskStatus  = taskStatus
        self.agentBattery = agentBattery
        self.agentPayload = agentPayload
        self.lastReward = 0

    # Getter Functions
    def get_agentId(self):
        return self.agentId 

    def get_agentStatus(self):
        return self.agentStatus 

    def get_agentPos(self):
        return self.agentPos 

    def get_agentOrient(self):
        return self.agentOrient

    def get_taskStatus(self):
        return self.taskStatus 

    def get_agentBattery(self):
        return self.agentBattery 

    def get_agentPayload(self):
        return self.agentPayload

    def get_lastReward(self):
        return self.curentReward 
    
    
    # setter Functions
    def set_agentId(self, agentId):
        self.agentId = agentId

    def set_agentStatus(self, agentStatus):
        self.agentStatus = agentStatus

    def set_agentPos(self, agentPos):
        self.agentPos = agentPos

    def set_agentOrient(self, agentOrient):
        self.agentOrient = agentOrient

    def set_taskStatus(self, taskStatus):
        self.taskStatus = taskStatus

    def set_agentBattery(self, agentBattery):
        self.agentBattery = agentBattery
        
    def set_agentPayload(self, agentPayload):
        self.agentPayload = agentPayload

    def set_lastReward(self, lastReward):
        self.lastReward = lastReward