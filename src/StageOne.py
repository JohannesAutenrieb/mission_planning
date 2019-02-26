from StageOneStateMachine import StageOneStateMachine, StageOneState
from Task import Task, TaskType
import time

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
        self.colorIsChanged = False
        self.PayloadDroped = False
        self.OnWayBackHome = False
        self.readyToDefend = False
        
        
        #Send Color Task
        
        self.EntryStartMotor = False 
        self.EntryhoverState = False
        self.EntryColorChange = False
        self.EntryAttackState = False
        self.EntryHoverInAOI = False
        self.EntryPayloadDrop = False
        self.EntryBackHome = False
        self.EntryDefendStart = False
        

    def StageOne(self, currentFriendsInformation, currentEnemyInformation, TaskList):
    
       
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
           print ("S1 - Start Motor")

           if not (self.EntryStartMotor):
           # Execute Payload Drop
           # Create Task Objects handle the tasks for each agent
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   print(TaskType.TAKEOFF.value)
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.TAKEOFF.value,[1, 1, 1],0))
                   #TaskList.append(self.Task)
                   #del self.Task
                   
               self.EntryStartMotor = True
               return
               
               
           ## ==Main Part ========
           self.allAgentsReachedAllAltitude=self.allAgentsFinishedTask(currentFriendsInformation);
           
           time.sleep(2)
           
	   # Execution of Transition Check and Exit of current State	
           if (self.allAgentsReachedAllAltitude):
               
               print("All agents reached all Altitude")
               #execute statemachine transition with trigger
               self.StageOneState.reachedAlitude()
               #times runs now for next stage in hover mode
               self.start = time.time()
               

               
        elif self.StateOne.state == 'hover':

	   # To-Do as long as in current State
           print ("S1 - Initial Hover")
           
           #Entry
           if not (self.EntryhoverState):
           #Execute Payload Drop
           # Create Task Objects
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   print(TaskType.REPAINT.value)
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.REPAINT.value,[1, 1, 1],0))
                   #TaskList.append(self.Task)
                   #del self.Task
                   
               self.EntryhoverState = True
               return
               
           ## ==Main Part ========
           self.current = time.time()          
           time.sleep(2)
          
           if ((self.current-self.start)>=self.Hovertime): # Hovertime Comapare
               self.hoverTimeReached = True
           else:
               self.hoverTimeReached = False
               
           
           #Exit of current State
           if (self.hoverTimeReached):
                print ("Hover time Reached")                
               # Execution of Transition
                self.StageOneState.hoverTimeReached()
                

        ###
        ## Get rid of this step ----- USELESS
        ###
        elif self.StateOne.state == 'changeColor':
	   # To-Do as long as in current State
           print ("S1 - Change Color")
           #Entry
           if not (self.EntryColorChange):
               #Execute color change
               # Send Task
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.REPAINT.value,[1, 1, 1],0))
                   #TaskList.append(self.Task)
                   #del self.Task
               self.EntryColorChange = True  
               return
           print ("S1 - Change Color")
               
           ## ==Main Part ========    
           self.colorIsChanged = self.allAgentsFinishedTask(currentFriendsInformation)
           
           
           #Exit of current State
           if (self.colorIsChanged):
                print ("changed Color for all Agents")
                #execute statemachine transition with trigger
                self.StageOneState.colorIsChanged()



        elif self.StateOne.state == 'goToEnemiesArea':
	   # To-Do as long as in current State
           print ("S1 - Go to Enemies Area")
           #Entry
           if not (self.EntryAttackState):
           #Execute Payload Drop
           # Create Task Objects
               f = open("/home/johannes/git/gdp_planning/src/mission_planning/scripts/MissionPlan/Stage_1_Attack.txt")
               line = f.readlines(0)
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   print("index:", i)
                   waypoint = line[i].split(";")
                   del waypoint[-1] # delete last element with new line command 
                   waypoint = [int(x) for x in waypoint]
                   TaskList.append( Task(currentFriendsInformation.friendlyId[i],TaskType.WAYPOINT.value,waypoint,0))
                   #TaskList.append(self.Task)
                   #del self.Task
               self.EntryAttackState = True
               f.close()  
               return
           ## ==Main Part ========
           self.ReachedEnemiesArea=self.allAgentsFinishedTask(currentFriendsInformation);
           
           
           #Exit of current State
           if (self.ReachedEnemiesArea):
                print ("All agents reached Enemy Area")
                #execute statemachine transition with trigger
                self.StageOneState.ReachedEnemiesArea()



        elif self.StateOne.state == 'hoverLowAttitude':
	   # To-Do as long as in current State
           print ("S1 - Hover in low Altitude")
           #Entry
           if not (self.EntryHoverInAOI):
           #Execute Payload Drop
           # Create Task Objects
               hoverTime = 5
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.WAIT.value,[1, 1, 1],hoverTime))
                   #TaskList.append(self.Task)
                   #del self.Task
               self.EntryHoverInAOI = True
               return
           
           ## ==Main Part ========
           self.HoverAltInEnemiesAreaReached =self.allAgentsFinishedTask(currentFriendsInformation)
           time.sleep(2)
           
           #Exit of current State
           if (self.HoverAltInEnemiesAreaReached):
                print ("Hover Altitude in Enemies are reached")
                #execute statemachine transition with trigger
                self.StageOneState.HoverAltInEnemiesAreaReached()



        elif self.StateOne.state == 'dropPayload':
	   # To-Do as long as in current State
           print ("S1 - Drop Payload")
           #Entry
           if not (self.EntryPayloadDrop):
           #Execute Payload Drop
           # Create Task Objects
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.PRELEASE.value,[1, 1, 1],0))
                   #TaskList.append(self.Task)
                   #del self.Task
               self.EntryPayloadDrop = True
               return
            ## ==Main Part ======== 
           self.PayloadDroped = self.allAgentsFinishedTask(currentFriendsInformation)   
           time.sleep(2)
           
           #Exit of current State
           if (self.PayloadDroped):
                print ("Payload Droped #DropItLikeItsHot")
                #execute statemachine transition with trigger
                self.StageOneState.PayloadDroped()

                
        elif self.StateOne.state == 'goToAOI':
	   # To-Do as long as in current State
           #Entry
           if not (self.EntryBackHome):
           #Execute Payload Drop
           # Send Task
               f = open("/home/johannes/git/gdp_planning/src/mission_planning/scripts/MissionPlan/Stage_1_Return.txt")
               line = f.readlines(0)
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   waypoint = line[i].split(";")
                   del waypoint[-1] # delete last element with new line command
                   waypoint = [int(x) for x in waypoint]
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.WAYPOINT.value,waypoint,0))
                   #TaskList.append(self.Task)
                   #del self.Task
               f.close()
               self.EntryBackHome = True
               return
           ## ==Main Part ========
           self.allAgentsBackInAOI =self.allAgentsFinishedTask(currentFriendsInformation)
           time.sleep(2)
           
           #Exit of current State
           if (self.allAgentsBackInAOI):
                print ("All agents back in AOI")
                #execute statemachine transition with trigger
                self.StageOneState.BackInAOI()


        elif self.StateOne.state == 'hoverInAOI':
	   # To-Do as long as in current State
           print ("S1 - Hover in AOI")
           #Entry
           if not (self.EntryDefendStart):
           #Execute Payload Drop
           # Create Task Objects
               hoverTime = 5
               for i in range(0, len(currentFriendsInformation.friendlyId)):
                   
                   TaskList.append(Task(currentFriendsInformation.friendlyId[i],TaskType.WAIT.value,[1, 1, 1],hoverTime))
                   #TaskList.append(self.Task)
                   #del self.Task
               self.EntryDefendStart = True
           ## ==Main Part ========
           self.readyToDefend = self.allAgentsFinishedTask(currentFriendsInformation)
           time.sleep(2)
           
           #Exit of current State
           if (self.readyToDefend):
                print ("Ready to defend MotherSuckaaaaaa :", self.readyToDefend)
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
                
    def allAgentsFinishedTask(self,currentFriendsInformation):
    #Loop over all friends to see if all fullfiled task
        for i in range(0, len(currentFriendsInformation.friendlyStatus)):
            if(currentFriendsInformation.TaskStatus[i] == True):
                return False
        return True


