import time

class Task():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentIdx,taskType,wayPointLocation,taskDeadline):
        
        self.timestamp = time.time()
        self.agentIdx = agentIdx
        self.taskType = taskType
        self.wayPointLocation = wayPointLocation
        self.taskDeadline = taskDeadline
    
    def get_timestamp(self):
        return self.timestamp 

    def get_agentIdx(self):
        return self.agentIdx 

    def get_taskType(self):
        return self.taskType 

    def get_wayPointLocation(self):
        return self.wayPointLocation 

    def get_taskDeadline(self):
        return self.taskDeadline 
    

    def set_timestamp(self):
        self.timestamp = time.time()

    def set_agentIdx(self, agentIdx):
        self.agentIdx = agentIdx

    def set_taskType(self, taskType):
        self.taskType = taskType

    def set_wayPointLocation(self, wayPointLocation):
        self.wayPointLocation = wayPointLocation

    def set_taskDeadline(self, taskDeadline):
        self.taskDeadline = taskDeadline