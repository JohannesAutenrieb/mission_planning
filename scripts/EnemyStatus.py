class EnemyStatus():
    
    def __init__(self):
         # Define the input data containers for foos:
        self.fooId = [1,2,3,4]
        self.fooPos = [[14,15,19],[2,3,6],[25,22,23],[28,17,18]]
        self.targetConfidence = [(0.56), (0.5), (0.7), (0.8)]
        self.attackStatus = [True, False, True, False]
        self.fooTimestamp = []
        
    def get_fooId(self):
        return self.fooId 
    def get_fooPos(self):
        return self.fooPos 
    def get_fooTimestamp(self):
        return self.fooTimestamp 
    
    ## Clarify if erase or append() to list
    
    ## Maybe not usefull under python
    def set_fooId(self, fooId):
        self.fooId = fooId
    def set_agentIdx(self, agentIdx):
        self.fooPos = agentIdx
    def set_fooTimestamp(self, fooTimestamp):
        self.fooTimestamp = fooTimestamp
        