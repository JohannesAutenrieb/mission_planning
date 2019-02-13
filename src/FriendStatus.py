#!/usr/bin/env python3

class FriendStatus():
    
    friendlyId =[]
    
    def __init__(self):
        #Define the input data containers for foos:
        self.friendlyId = []
        self.friendlyStatus = []
        self.Task = []
        self.friendlyPos = []
        self.friendlyBatt = []
        self.friendlyTimestamp = []
        
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
        