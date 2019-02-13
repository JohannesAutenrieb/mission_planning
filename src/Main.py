from MissionStateMachine import MissionStateMachine, MissionState
from StageOne import MissionStageOne
from StageThree import MissionStageThree
from EnemyStatus import EnemyStatus
from FriendStatus import FriendStatus
from Task import Task
import datetime
from PyQt5 import QtCore
import sys
import rospy
from std_msgs.msg import String

class MissionExecution():
    
    def __init__(self):
        
        # ----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        # ----------------------------------------------------------------------
    
        # take initial time
        self.startTime = datetime.datetime.now().timestamp()
        
        #Mission Stage Times in seconds (currently not real time)
        self.TotalMissionTime = 150
        self.StageThreeTime = 120
        self.MaximumStageTwoTime = self.TotalMissionTime - self.StageThreeTime
        
        #State object to handle the states with initial state one
        self.obj = MissionState(state='stageOne')
        
        #state machine instance to handle the main state machine
        self.mission = MissionStateMachine(self.obj)   
        self.stageOneState= MissionStageOne()
        self.stageThreeState= MissionStageThree()
        
        #Set up of initial state status (inital state one)
        self.StageOneCompleted =False
        self.StageThreeCompleted =False
        self.MissionDone = False
        
        
        
        # Define the input data containers for friends:
        self.currentFriendsInformation = FriendStatus()
        self.currentEnemyInformation= EnemyStatus()
        self.TaskList = []

        # Define the input data containers for foos:
        self.fooId = []
        self.fooPos = []
        self.fooTimestamp = []   
        
        
        # Init of ROS Listener Node
        rospy.init_node('TaskAllocation', anonymous=True)
        rospy.Subscriber("DataBase", String, self.callback)
        
        # Init of ROS Talker
        self.pub = rospy.Publisher('SytstemArch', String, queue_size=10)



#        self. rospy.Subscriber("chatter", String, callback)

    def callback(self,data):
        #operation on recieved data
        # data.Value 
#        print(data.data)
        
        #REceived Friend Information
        setattr(self.currentFriendsInformation, 'friendlyId', data.friendlyId) 
        setattr(self.currentFriendsInformation, 'friendlyStatus', data.friendlyStatus)
        setattr(self.currentFriendsInformation, 'friendlyPos', data.friendlyPos)
        setattr(self.currentFriendsInformation, 'friendlyBatt', data.friendlyBatt)
        setattr(self.currentFriendsInformation, 'friendlyTimestamp', data.friendlyTimestamp)

#        self.friendlyId = data.friendlyId
#        self.friendlyStatus = data.friendlyStatus
#        self.friendlyPos = data.friendlyPos
#        self.friendlyBatt = data.friendlyBatt
#        self.friendlyTimestamp = data.friendlyTimestamp
        
        #Received Foo information
        
        setattr(self.currentEnemyInformation, 'fooId', data.fooId) 
        setattr(self.currentEnemyInformation, 'fooPos', data.fooPos)
        setattr(self.currentEnemyInformation, 'fooTimestamp', data.fooTimestamp)
        
#        self.fooId = data.fooId
#        self.fooPos = data.fooPos
#        self.fooTimestamp = data.fooTimestamp


    def missionState(self):

            # ----------------------------------------------------------------------
            # READING PART: In This Part the Messages AND Parameters Are Read
            # ----------------------------------------------------------------------
    
            # Here the parameters have to be read
    
            # ----------------- TO - DO -------------------------------------------
    
            # ----------------------------------------------------------------------
            # EXECUTION PART: In This Part The State Machine is Running
            # ----------------------------------------------------------------------
    
            # Set current time for this loop run
            self.currentTime = datetime.datetime.now().timestamp()
            # Step : Go in to the State Machine and Execute relevant features
    
            if self.obj.state == 'stageOne':
    
    	   # To-Do as long as in current State
               print ("1 - Stage One Entered")
               #Execute Stage One State Machine and return Boolean if executed
               self.StageOneCompleted = self.stageOneState.StageOne(self.currentFriendsInformation, self.currentEnemyInformation, self.TaskList)
               #print ("Status:", StageOne())
    	   # Execution of Transition Check and Exit of current State	
               if (self.StageOneCompleted):
                   #execute statemachine transition with trigger
                   print ("Switch Bitch")
                   self.mission.triggerOne()
                   
            elif self.obj.state == 'stageTwo':
    
    	   # To-Do as long as in current State
               print ("2 - Got a true expression value")
               
               # Execution of Transition Check and Exit of current State
               if (((self.currentTime-self.startTime)>=self.MaximumStageTwoTime)):
                    #execute statemachine transition with trigger
                     self.mission.triggerTwo()
                    
            elif self.obj.state == 'stageThree':
    	   # To-Do as long as in current State
               print ("3 - Stage Three entered")
               
               self.StageOneCompleted = self.stageThreeState.StageThree(self.currentFriendsInformation, self.currentEnemyInformation, self.TaskList)
               
               # Execution of Transition Check and Exit of current State
               if (self.StageThreeCompleted):
                    print ("We are done with the Mission")
                    MissionDone = True
                    # Let's go and drink a beer
                    return MissionDone
                    
            #----------------------------------------------------------------------
    
    
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            # ----------------------------------------------------------------------
    
            # Here the variables have to be send to external processes and agents
            #
            #--- Handle Task before
           
            self.pub.publish("Tasks")
    
            # Wait for 1 sec before goig to next execution    

if __name__ == "__main__":
    print("Its Me bitch")
    
    # Setup of Mission Statemachine
    missionExecutaion = MissionExecution()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    # Setup of timer thread
    app = QtCore.QCoreApplication([])   
    timer = QtCore.QTimer()
    time = QtCore.QTime()
    timer.timeout.connect(missionExecutaion.missionState)
    timer.start(100)
    sys.exit(app.exec_())




