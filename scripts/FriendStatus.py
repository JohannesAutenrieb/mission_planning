#!/usr/bin/env python3

class FriendStatus():
    
    friendlyId =[]
    
    def __init__(self):
        #Define the input data containers for foos:
        self.friendlyId = [1,2,3,4,5,6,7,8]
        self.friendlyWorkingStatus =[True,True,True,True,True,True,True,True]
        self.friendlyTaskStatus = [False, False, False, False, False, False, False, False]
        self.friendlyTaskId = [1,2,3,4,5,6,7,8]
        self.friendlyPos = [[5,6,7],[8,9,10],[11,12,13],[1,2,3],[5,6,7],[8,9,10],[11,12,13],[14,15,16]]
        self.friendlyHeading = [1,1,1,1,1,1,1,1]
        self.friendlyBatt = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        self.friendlyPayload = [True,True,True,True,True,True,True,True]
        #self.friendlyW = 0
        #self.friendlyTimestamp = 0
        
    def get_fooId(self):
        return self.fooId 
    def get_fooPos(self):
        return self.fooPos 
    def get_fooTimestamp(self):
        return self.fooTimestamp 
    
    ## Clarify if erase or append() to list
    # setattr(x, 'attr_name', s)    
    ## Maybe not usefull under python
    def set_fooId(self, fooId):
        self.fooId = fooId
    def set_agentIdx(self, agentIdx):
        self.fooPos = agentIdx
    def set_fooTimestamp(self, fooTimestamp):
        self.fooTimestamp = fooTimestamp
        