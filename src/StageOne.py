from StageOneStateMachine import StageOneStateMachine, StageOneState
import time

def StageOne():

    #----------------------------------------------------------------------
    # Init: Create relevant Objects and global Variables
    #----------------------------------------------------------------------

    # take initial time
    start = time.time()
    #State object to handle the states with initial state one
    StateOne = StageOneState(state='startMotor')
    #state machine instance to handle the main state machine
    StageOne = StageOneStateMachine(StateOne)
    StageDone=False
    
    
    
    while (True):
        #----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the parameters have to be read

	# ----------------- TO - DO -------------------------------------------
        
        #----------------------------------------------------------------------
        # EXECUTION PART: In This Part The State Machine is Running
        #----------------------------------------------------------------------
        
        #Set current time for this loop run
        currentTime= time.time()
        #Step : Go in to the State Machine and Execute relevant features
        
        if StateOne.state == 'startMotor':

	   # To-Do as long as in current State
           print ("S1 - Start Motor")
           allAgentsReachedAllAltitude=True
           
	   # Execution of Transition Check and Exit of current State	
           if (allAgentsReachedAllAltitude):
               
               print("All agents reached all Altitude")
               #execute statemachine transition with trigger
               StageOne.reachedAlitude()
               #Set time new to restart the countdown
               start = time.time()
               
        elif StateOne.state == 'hover':

	   # To-Do as long as in current State
           print ("S1 - Initial Hover")
           hoverTimeReached = True
           
           # Execution of Transition Check and Exit of current State
           if (hoverTimeReached):

                print ("Hover time Reached")                
               #execute statemachine transition with trigger
                StageOne.hoverTimeReached()

                #Set time new to restart the countdown
                start = time.time()
                
        elif StateOne.state == 'changeColor':
	   # To-Do as long as in current State
           print ("S1 - Change Color")
           colorIsChanged = True
           
           # Execution of Transition Check and Exit of current State
           if (colorIsChanged):
                print ("changed Color for all Agents")
                #execute statemachine transition with trigger
                StageOne.colorIsChanged()

                #Set time new to restart the countdown
                start = time.time()

        elif StateOne.state == 'goToEnemiesArea':
	   # To-Do as long as in current State
           print ("S1 - Go to Enemies Area")
           ReachedEnemiesArea = True
           
           # Execution of Transition Check and Exit of current State
           if (ReachedEnemiesArea):
                print ("All agents reached Enemie Area")
                #execute statemachine transition with trigger
                StageOne.ReachedEnemiesArea()

                #Set time new to restart the countdown
                start = time.time()

        elif StateOne.state == 'hoverLowAttitude':
	   # To-Do as long as in current State
           print ("S1 - Hover in low Altitude")
           HoverAltInEnemiesAreaReached =True
           
           # Execution of Transition Check and Exit of current State
           if (HoverAltInEnemiesAreaReached):
                print ("Hover Altitude in Enemies are reached")
                #execute statemachine transition with trigger
                StageOne.HoverAltInEnemiesAreaReached()

                #Set time new to restart the countdown
                start = time.time()

        elif StateOne.state == 'dropPayload':
	   # To-Do as long as in current State
           print ("S1 - Drop Payload")
           PayloadDroped = True
           
           # Execution of Transition Check and Exit of current State
           if (PayloadDroped):
                print ("Drop Payload")
                #execute statemachine transition with trigger
                StageOne.PayloadDroped()

                #Set time new to restart the countdown
                start = time.time()
                
        elif StateOne.state == 'goToAOI':
	   # To-Do as long as in current State
           print ("S1 - Go to AOI")
           allAgentsBackInAOI = True
           
           # Execution of Transition Check and Exit of current State
           if (allAgentsBackInAOI):
                print ("All agents back in AOI")
                #execute statemachine transition with trigger
                StageOne.BackInAOI()

                #Set time new to restart the countdown
                start = time.time()

        elif StateOne.state == 'hoverInAOI':
	   # To-Do as long as in current State
           print ("S1 - Hover in AOI")
           readyToDefend = True
           
           # Execution of Transition Check and Exit of current State
           if (readyToDefend):
                print ("Ready to defend MotherSuckaaaaaa :", readyToDefend)
                #execute statemachine transition with trigger

                #Set time new to restart the countdown
                start = time.time()
                return readyToDefend

        #----------------------------------------------------------------------
        # WRITING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the variables have to be send to external processes and agents
        
        # ----------------- TO - DO -------------------------------------------
                

        #----------------------------------------------------------------------
        # WAITING PART: Wait for 1 sec before goig to next execution 
        #----------------------------------------------------------------------
        #time.sleep(1)
                



