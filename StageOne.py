from StageOneStateMachine import StageOneStateMachine, StageOneState
from Task import Task, TaskType, InitMsg
from mission_planning.msg import InitMessage
import time
import os
import rospy

class MissionStageOne():
     
    def __init__(self):

        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
    
        # take initial time
        self.start = time.time()
        self.Task = []
        #State object to handle the states with initial state one
        self.StateOne = StageOneState(state='startMotor')
        #state machine instance to handle the main state machine
        self.StageOneState = StageOneStateMachine(self.StateOne)
        self.StageDone=False
        
        self.Hovertime = 10 #seconds
        self.hoverTimeReached = False
        self.OnWayBackHome = False
        self.readyToDefend = False

        
        self.EntryStartMotor = False 
        self.EntryhoverState = False
        self.EntryBackHome = False
        self.EntryDefendStart = False

        # Set initial heading for agents
        self.initialHeading = 0.0     # [deg]


    def StageOne(self, agentsList, foosList, TaskList):
    
       
        #----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # ----------------- TO - DO -------------------------------------------
        
        #----------------------------------------------------------------------
        # EXECUTION PART: In This Part The State Machine is Running
        #----------------------------------------------------------------------

        
        #Set current time for this loop run
        self.currentTime= time.time()
        #Step : Go in to the State Machine and Execute relevant features
        
        if self.StateOne.state == 'startMotor':

	   # To-Do as long as in current State

           if not (self.EntryStartMotor):

            # Wait until first agent data arrives
                while not agentsList:
                    time.sleep(0.5)
           # Send initialization message with home locations
                self.sendInitMessages(agentsList)

                print("S1:: TAKEOFF")
           # Create Task Objects handle the tasks for each agent
                for i in range(0, len(agentsList)):
                    deadline = 120
                    TaskList.append(Task(agentsList[i].agentId, 0,TaskType.TAKEOFF.value,[1, 1, 1],deadline))
		    # wait for qgent to get message
                    print "S1: Takeoff order send to agent: %d" % agentsList[i].agentId
                self.EntryStartMotor = True
                return

           ## ==Main Part ========
           print("S1: Agents taking off...")
           self.allAgentsReachedAllAltitude = self.allAgentsFinishedTask(agentsList)
           
           time.sleep(2)
           
	   # Execution of Transition Check and Exit of current State	
           if (self.allAgentsReachedAllAltitude):
               #execute statemachine transition with trigger
               self.StageOneState.reachedAlitude()
               #times runs now for next stage in hover mode
               self.start = time.time()
               

        elif self.StateOne.state == 'hover':

	   # To-Do as long as in current State

           #Entry
           if not (self.EntryhoverState):
           #Execute Payload Drop
           # Create Task Objects
               # -> Nothing to do
               self.EntryhoverState = True
               return
               
           ## ==Main Part ========
           self.current = time.time()          
           #time.sleep(5)
           print("S1: Agents hovering...")
          
           if ((self.current-self.start)>=self.Hovertime): # Hovertime Comapare
               self.hoverTimeReached = True
           else:
               self.hoverTimeReached = False
               
           
           #Exit of current State
           if (self.hoverTimeReached):
               # Execution of Transition
                self.StageOneState.hoverTimeReached()

        elif self.StateOne.state == 'goToAOI':
	   # To-Do as long as in current State
           #Entry
           if not (self.EntryBackHome):
           #Execute Payload Drop
           # Send Task
               f = open(self.getRelativeFilePath('MissionPlan/Stage_1_Return.txt'))
               line = f.readlines(0)
               deadline = 120
               print("S1: Setting waypoints")
               for i in range(0, len(agentsList)):
                   waypoint = line[i].split(";")
                   del waypoint[-1] # delete last element with new line command
                   waypoint = [int(x) for x in waypoint]
                   TaskList.append(Task(agentsList[i].agentId, 0, TaskType.WAYPOINT.value,waypoint,deadline))
                   print "S1: Waypoint: {0} set for agent: {1}".format(waypoint, agentsList[i].agentId)
               f.close()
               self.EntryBackHome = True
               return
           ## ==Main Part ========
           print("S1: Agents going to waypoint...")
           self.allAgentsBackInAOI =self.allAgentsFinishedTask(agentsList)
           #time.sleep(20)
           
           #Exit of current State
           if (self.allAgentsBackInAOI):
                #execute statemachine transition with trigger
                self.StageOneState.BackInAOI()

        elif self.StateOne.state == 'hoverInAOI':
	   # To-Do as long as in current State
           #Entry
           if not (self.EntryDefendStart):
           #Execute Payload Drop
           # Create Task Objects
               for i in range(0, len(agentsList)):
                   #TaskList.append(Task(agentsList.friendlyId[i],TaskType.WAIT.value,[1, 1, 1],hoverTime))
                   print "S1: Agent {0} in hovering mode".format(agentsList[i].agentId)
               self.EntryDefendStart = True
           ## ==Main Part ========
           print("S1: Agents hovering...")
           hoverTime = 5
           self.readyToDefend = self.allAgentsFinishedTask(agentsList)
           #time.sleep(hoverTime)
           
           #Exit of current State
           if (self.readyToDefend):
                #execute statemachine transition with trigger
                return self.readyToDefend

            #----------------------------------------------------------------------
            # WRITING PART: In This Part the Messages AND Parameters Are Read
            #----------------------------------------------------------------------        
            
            # Here the variables have to be send to external processes and agents
            
            # ----------------- TO - DO -------------------------------------------
                    
    
            #----------------------------------------------------------------------
            # WAITING PART: Wait for 1 sec before goig to next execution 
            #----------------------------------------------------------------------
            #time.sleep(1)
                
    def allAgentsFinishedTask(self,agentsList):
    #Loop over all friends to see if all fullfiled task
        for i in range(0, len(agentsList)):
            if (agentsList[i].taskStatus is True) and (agentsList[i].agentWorkingStatus is True):
                return False
        return True

    def getRelativeFilePath(self, relativePath):

        scriptDir = os.path.dirname(__file__)
        absFilePath = os.path.join(scriptDir, relativePath)
        return absFilePath

    def sendInitMessages(self, agentsList):

        # Init of ROS Publisher for Initialization Message
        pubInit = rospy.Publisher('InitInformation', InitMessage, queue_size=10)
        homeLocationList = []

        # Read home waypoints from file (home set to Stage 3 landing waypoints)
        f = open(self.getRelativeFilePath("MissionPlan/Stage_3_Attack.txt"))
        line = f.readlines(0)
        rate = rospy.Rate(5)

        # Create list of InitMsg objects
        for i in range(0, len(agentsList)):
            homeWaypoint = line[i].split(";")
            del homeWaypoint[-1]  # delete last element with new line command
            homeWaypoint = [int(x) for x in homeWaypoint]
            homeLocationList.append(InitMsg(agentsList[i].agentId, homeWaypoint))
        f.close()

        print("S1: Setting home location")

        # Publish initialization messages to topic
        if not len(homeLocationList) == 0:
            for i in range(0, len(homeLocationList)):
                msg = InitMessage()
                msg.agentId = homeLocationList[i].agentIdx
                msg.homeLocation = homeLocationList[i].homeLocation
                msg.nominalHeading = self.initialHeading
                rate.sleep()
                pubInit.publish(msg)
                print "S1: Home location for agent: {0} set to: {1}".format(msg.agentId, msg.homeLocation)
                del msg

        # Wait - give system time to process messages
        time.sleep(2)
