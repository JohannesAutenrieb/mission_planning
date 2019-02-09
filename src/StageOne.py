from StageOneStateMachine import StageOneStateMachine, StageOneState
import time

class MissionStageOne():
    
    
    def __init__(self):

        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
    
        # take initial time
        self.start = time.time()
        #State object to handle the states with initial state one
        self.StateOne = StageOneState(state='startMotor')
        #state machine instance to handle the main state machine
        self.StageOneState = StageOneStateMachine(self.StateOne)
        self.StageDone=False
        

    def StageOne(self):
    

        
        
       
        #----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the parameters have to be read

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
           self.allAgentsReachedAllAltitude=True
           time.sleep(2)
           
	   # Execution of Transition Check and Exit of current State	
           if (self.allAgentsReachedAllAltitude):
               
               print("All agents reached all Altitude")
               #execute statemachine transition with trigger
               self.StageOneState.reachedAlitude()

               
        elif self.StateOne.state == 'hover':

	   # To-Do as long as in current State
           print ("S1 - Initial Hover")
           self.hoverTimeReached = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.hoverTimeReached):

                print ("Hover time Reached")                
               #execute statemachine transition with trigger
                self.StageOneState.hoverTimeReached()


                
        elif self.StateOne.state == 'changeColor':
	   # To-Do as long as in current State
           print ("S1 - Change Color")
           self.colorIsChanged = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.colorIsChanged):
                print ("changed Color for all Agents")
                #execute statemachine transition with trigger
                self.StageOneState.colorIsChanged()



        elif self.StateOne.state == 'goToEnemiesArea':
	   # To-Do as long as in current State
           print ("S1 - Go to Enemies Area")
           self.ReachedEnemiesArea = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.ReachedEnemiesArea):
                print ("All agents reached Enemie Area")
                #execute statemachine transition with trigger
                self.StageOneState.ReachedEnemiesArea()



        elif self.StateOne.state == 'hoverLowAttitude':
	   # To-Do as long as in current State
           print ("S1 - Hover in low Altitude")
           self.HoverAltInEnemiesAreaReached =True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.HoverAltInEnemiesAreaReached):
                print ("Hover Altitude in Enemies are reached")
                #execute statemachine transition with trigger
                self.StageOneState.HoverAltInEnemiesAreaReached()



        elif self.StateOne.state == 'dropPayload':
	   # To-Do as long as in current State
           print ("S1 - Drop Payload")
           self.PayloadDroped = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.PayloadDroped):
                print ("Drop Payload")
                #execute statemachine transition with trigger
                self.StageOneState.PayloadDroped()

                
        elif self.StateOne.state == 'goToAOI':
	   # To-Do as long as in current State
           print ("S1 - Go to AOI")
           self.allAgentsBackInAOI = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
           if (self.allAgentsBackInAOI):
                print ("All agents back in AOI")
                #execute statemachine transition with trigger
                self.StageOneState.BackInAOI()


        elif self.StateOne.state == 'hoverInAOI':
	   # To-Do as long as in current State
           print ("S1 - Hover in AOI")
           self.readyToDefend = True
           time.sleep(2)
           # Execution of Transition Check and Exit of current State
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
                



