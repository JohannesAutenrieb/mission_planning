import time

class Task():
    
    # Defined States in the Mission State Machine
    def __init__(self,agentIdx,taskType,wayPointLocation):
        
        self.timestamp = time.time()
        self.agentIdx = None
        self.taskType = None
        self.wayPointLocation = None
        self.taskDeadline = None
    
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
    

