import rospy
import math
from TaskStatusInfo import TaskStatusInfo
from Task import Task, TaskType
import datetime
from mission_planning.msg import TaskList, UpdateList

class TaskManager():
    
    def __init__(self):
        #To-Do   
        # ROS PArt in which all information of the swarm should been recieved and stored
        
        #instance to store all relevant data regarding the current tasks 
        self.taskStatusInfo = TaskStatusInfo()
        
        # Task
        self.TaskList = []
        self.UpdateList = []

        # Init of ROS Talker
        self.pub = rospy.Publisher('TaskSupervision', TaskList, queue_size=10)

    def callback(self,data):
        # operation on recieved data
        # print(data.data)
        
        #Received Friend Information
        setattr(self.taskStatusInfo, 'taskType', data.taskType) 
        setattr(self.taskStatusInfo, 'agentId', data.agentId)
        setattr(self.taskStatusInfo, 'initialPostion', data.initialPostion)
        setattr(self.taskStatusInfo, 'currentPostion', data.currentPostion)
        setattr(self.taskStatusInfo, 'wayPoint', data.wayPoint)
        setattr(self.taskStatusInfo, 'lastReward', data.lastReward)
        setattr(self.taskStatusInfo, 'timeStempOfTask', data.timeStempOfTask)
        setattr(self.taskStatusInfo, 'targetId', data.targetId)        

    def taskProgress(self):
        
        # current time taking
        currentTime = datetime.datetime.now().timestamp()

        
        # Loop over all agents and check progess
        for AgentListidX in range(0, len(self.taskStatusInfo.agentId)):
            # taking relevant time information
           timeOfAssignment = self.taskStatusInfo.timestampOfTask[AgentListidX]
           maxEstimatedTime = self.taskStatusInfo.maxEstimatedTime[AgentListidX]

           currentReward = self.computeExecutionReward(self.taskStatusInfo.currentPostion[AgentListidX], self.taskStatusInfo.wayPointLocation[AgentListidX],self.taskStatusInfo.initialPostion[AgentListidX])
           
           if self.taskStatusInfo.lastReward[AgentListidX]>=currentReward or (currentTime-timeOfAssignment)>maxEstimatedTime:
               #assign task new and trigger systemCheckprocedure or land\restart
               if self.taskStatusInfo.systemStatus[AgentListidX] == True :
                  self.sendSystemRequestMessage(AgentListidX)
           else:
               #set current task as last ## need to be adjusted for the index
               setattr(self.taskStatusInfo, 'lastReward [%d]' % AgentListidX, currentReward)  
        
        # Message to the Agents due to problems
        if not len(self.taskList)==0:
            for  i in range(0, len( self.taskList)):
                msg = TaskList()
                print ("Task Message:")
                print(self.taskList[i].agentIdx)
                print(self.taskList[i].taskType.value)
                print("Posi type:", type(self.taskList[i].wayPointLocation[0]))
                print(self.taskList[0].wayPointLocation)
                msg.agentIdx =  self.taskList[i].agentIdx
                msg.TaskType = self.taskList[i].taskType.value
                msg.position = self.taskList[i].wayPointLocation
                msg.timestamp = datetime.datetime.now().timestamp()
               
                self.pub.publish(msg)
                #clear message object
                del msg
            #clear taesk lsit for next time step
            self.taskList.clear()
            
        #Message to System Architecture to update global Task Status
        if not len(self.UpdateList)==0:
            for  i in range(0, len( self.UpdateList)):
                msg = UpdateList()
                print ("Update Message:")
                print(self.UpdateList[i].agentIdx)
                print(self.UpdateList[i].taskType.value)
                print("Posi type:", type(self.UpdateList[i].wayPointLocation[0]))
                print(self.UpdateList[0].wayPointLocation)
                msg.agentIdx =  self.UpdateList[i].agentIdx
                msg.TaskType = self.UpdateList[i].taskType.value
                msg.position = self.UpdateList[i].wayPointLocation
                msg.timestamp = datetime.datetime.now().timestamp()
               
                self.pub.publish(msg)          
                #clear message object
                del msg
            #clear taesk lsit for next time step
            self.taskList.clear()
                     

    def computeExecutionReward(self, agentPos, TaskWaypoint, initialPostion):
        # reward = d-a/d min:0 and max: 1
        d = math.sqrt((agentPos[0]-initialPostion[0])**2 + (agentPos[1]-initialPostion[1])**2 + (agentPos[2]-initialPostion[2])**2)
        a = math.sqrt((agentPos[0]-TaskWaypoint[0])**2 + (agentPos[1]-TaskWaypoint[1])**2 + (agentPos[2]-TaskWaypoint[2])**2)
        reward = (d-a)/d
        return reward

    def sendAbortMessage(self,AgentListidX):
        # send message through ROS
        Task(self.taskStatusInfo.agentId[AgentListidX],TaskType.ABORTMISSION.value,[1, 1, 1],0)
        

    def sendSystemRequestMessage(self, AgentListidX):
        # send message through ROS
        Task(self.taskStatusInfo.agentId[AgentListidX],TaskType.SYSTEMCHECK.value,[1, 1, 1],0)
        
        

   
if __name__ == "__main__":
    print("The Main Programm")
    
    # Setup of Mission Statemachine
    taskSupervision = TaskManager()
    
    # Init of ROS Listener Node
    rospy.init_node('TaskManagement', anonymous=True)
    
    # spin() simply keeps python from exiting until this node is stopped
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        taskSupervision.taskProgress()
        rate.sleep()     