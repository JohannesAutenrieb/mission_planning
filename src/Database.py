#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from TaskStatusInfo import TaskStatusInfo
from mission_planning.msg import TaskList, TaskStatusInformation
from Task import Task, TaskType
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from mission_planning.msg import TaskMessage, SwarmInformation,TargetInformation, RewardMessage, SystemStatusMessage,TaskStatusMessage
import rospy
import time

class DatabaseFake(): 

    def __init__(self):
        # ROS Part in which all information of the swarm should been recieved and stored
        
        #instance to store all relevant data regarding the current tasks 
        self.taskStatusInfo = TaskStatusInfo()        
        self.currentFriendsInformation = FriendStatus()
        self.currentEnemyInformation= EnemyStatus()
        self.taskList = []
        
        # Init of ROS Talker
        self.pub = rospy.Publisher('DatabaseInformation', TaskList, queue_size=10)

    def callbackTaskStatusInformation(self,data):
        # Operation on recieved data
        print("Task Status List")
        
        # Received Friend Information
        setattr(self.taskStatusInfo, 'agentId', data.agentId)
        setattr(self.taskStatusInfo, 'taskType', data.taskType) 
        setattr(self.taskStatusInfo, 'initialPostion', data.initialPostion)
        setattr(self.taskStatusInfo, 'currentPostion', data.currentPostion)
        setattr(self.taskStatusInfo, 'wayPoint', data.wayPoint)
        setattr(self.taskStatusInfo, 'lastReward', data.lastReward)
        setattr(self.taskStatusInfo, 'timeStempOfTask', data.timeStempOfTask)
        setattr(self.taskStatusInfo, 'targetId', data.targetId)

    def callbackTaskMessages(self,data):
        
        print("Task Message")
        
        if not (data.taskType[data.agentIdx] == TaskType.ABORTMISSION or data.taskType[data.agentIdx] == TaskType.SYSTEMCHECK.value):
            if (data.taskType[data.agentIdx] == TaskType.ABORTMISSION.value):
                setattr(self.taskStatusInfo, 'taskType[%d]' % data.agentIdx, data.TaskType)
        
        if data.agentIdx not in self.taskStatusInfo.agentId:
            # Receive and Process Task Information
            getattr(self.taskStatusInfo, 'agentId').append(data.agentIdx)
            getattr(self.taskStatusInfo, 'taskType').append(data.TaskType)
            getattr(self.taskStatusInfo, 'wayPoint').append(data.position)
            getattr(self.taskStatusInfo, 'taskDeadline').append(data.taskDeadline)
            getattr(self.taskStatusInfo, 'timeStempOfTask').append(data.timestamp)
            
            # Inital values for other variables 
            setattr(self.taskStatusInfo, 'initialPostion').append(self.currentFriendsInformation.friendlyPos[data.agentIdx])
            setattr(self.taskStatusInfo, 'currentPostion').append(self.currentFriendsInformation.friendlyPos[data.agentIdx])
            setattr(self.taskStatusInfo, 'agentTaskStatus').append(False) # why?
            setattr(self.taskStatusInfo, 'lastReward').append(0)
                
            # In Case of an Attack
            if data.taskType[data.agentIdx] == TaskType.ATTACK:
                setattr(self.taskStatusInfo, 'targetId').append(data.targetId)
            else:
                setattr(self.taskStatusInfo, 'targetId').append(0)
                    
    def callbackTaskStatusAgent(self,data):
        #operation on recieved data   
        print("Task Status Agent")
        #Received Friend Information
        if data.agentIdx in data.agentIdx:       
             setattr(self.taskStatusInfo, 'agentTaskStatus[%d]' % data.agentIdx, data.agentTaskStatus)

    def callbackSystemStatusAgent(self,data):
        #operation on Friend Information 
        print("System Status")
        if data.agentIdx in data.agentIdx:       
            setattr(self.taskStatusInfo, 'systemWorkingStatus[%d]' % data.agentIdx, data.systemWorkingStatus)

    def callbackNewReward(self,data):
        #operation on Friend Information 
        print("New Reward")
        if data.agentIdx in data.agentIdx:       
            setattr(self.taskStatusInfo, 'lastReward[%d]' % data.agentIdx, data.lastReward)

    def callbackFriend(self,data):
        #operation on recieved data   
        print("Friend")
        #Receive and Store Friend Information
        setattr(self.currentFriendsInformation, 'friendlyId', data.friendlyId) 
        setattr(self.currentFriendsInformation, 'friendlyStatus', data.friendlyStatus)
        setattr(self.currentFriendsInformation, 'friendlyPos', data.friendlyPos)
        setattr(self.currentFriendsInformation, 'friendlyBatt', data.friendlyBatt)
        setattr(self.currentFriendsInformation, 'friendlyTimestamp', data.friendlyTimestamp) 
        
        #Handle related data which uses that information        
        for AgentListidX in range(0, len(data.friendlyId)):   
            if AgentListidX in self.currentFriendsInformation.agentId:              
                setattr(self.taskStatusInfo, 'currentPostion[%d]' % data.agentIdx, data.friendlyId[AgentListidX])
                break


    def dataBaseHandler(self):     
        # Send the messages every 5 seconds 

        if not len( self.taskList)==0:
            for  i in range(0, len( self.taskList)):
                msg = TaskList()
                # print ("Task Database Message:")
                # print(self.taskList[i].agentIdx)
                # print(self.taskList[i].taskType.value)
                # print("Posi type:", type(self.taskList[i].wayPointLocation[0]))
                # print(self.taskList[0].wayPointLocation)
                
                msg.lastUpdate = time.time()
                msg.taskType = self.taskType
                msg.agentId =  self.agentId
                msg.systemWorkingStatus =  self.systemWorkingStatus 
                msg.initialPostion =  self.initialPostion
                msg.currentPostion =  self.currentPostion
                msg.wayPoint =   self.wayPoint
                msg.lastReward =  self.lastReward 
                msg.taskDeadline =  self.taskDeadline
                msg.timestampOfTask =  self.timestampOfTask
                msg.targetId =   self.targetId

               
                self.pub.publish(msg)
                #clear message object
                del msg

if __name__ == "__main__":
    print("Execution of the Task Status Information System")
    
    # Setup of Mission Statemachine
    databaseFake = DatabaseFake()
    
    # Init of ROS Listener Node
    rospy.init_node('TaskStatusDatabase', anonymous=True)

    # Init Listener for friend and foos
    rospy.Subscriber("TaskMessages", TaskMessage, databaseFake.callbackTaskMessages)
    rospy.Subscriber("TaskSupervision", TaskStatusMessage, databaseFake.callbackTaskStatusAgent)
    rospy.Subscriber("SystemStatusMessage", SystemStatusMessage, databaseFake.callbackSystemStatusAgent)
    rospy.Subscriber("AgentSwarmInformation", SwarmInformation, databaseFake.callbackFriend)
    rospy.Subscriber("SystemStatus", RewardMessage, databaseFake.callbackNewReward)
    
    # spin() simply keeps python from exiting until this node is stopped
    rate = rospy.Rate(0.1)
    
    while not rospy.is_shutdown():
        databaseFake.dataBaseHandler()
        rate.sleep()            