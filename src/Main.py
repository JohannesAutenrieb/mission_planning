from MissionStateMachine import MissionStateMachine, MissionState
import time

def main():

    #----------------------------------------------------------------------
    # Init: Create relevant Objects and global Variables
    #----------------------------------------------------------------------

    # take initial time
    start = time.time()
    #State object to handle the states with initial state one
    obj = MissionState(state='stageOne')
    #state machine instance to handle the main state machine
    mission = MissionStateMachine(obj)
    
    
    #Set up of initial state status (inital state one)
    stageOneStatus =True
    stageTwoStatus =False
    stageThreeStatus =False
    
    #Mission Stage Times in seconds (currently not real time)
    stageOneDuration= 5
    stageTwoDuration= 5
    stageThreeDuration= 5
    
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
        
        if obj.state == 'stageOne':

	   # To-Do as long as in current State
           print ("1 - Got a true expression value")
           
	   # Execution of Transition Check and Exit of current State	
           if (((currentTime-start)>=stageOneDuration) and (stageOneStatus ==True)):
               #execute statemachine transition with trigger
               mission.triggerOne()
               stageOneStatus =False
               stageTwoStatus = True
               #Set time new to restart the countdown
               start = time.time()
               
        elif obj.state == 'stageTwo':

	   # To-Do as long as in current State
           print ("2 - Got a true expression value")
           
           # Execution of Transition Check and Exit of current State
           if (((currentTime-start)>=stageTwoDuration) and (stageTwoStatus ==True)):
                #execute statemachine transition with trigger
                mission.triggerTwo()
                stageTwoStatus = False
                stageThreeStatus = True
                #Set time new to restart the countdown
                start = time.time()
                
        elif obj.state == 'stageThree':
	   # To-Do as long as in current State
           print ("3 - Got a true expression value")
           
           # Execution of Transition Check and Exit of current State
           if (((currentTime-start)>=stageThreeDuration) and (stageThreeStatus ==True)):
                print ("We are done with the Mission")
                print (stageThreeStatus)
                #execute statemachine transition with trigger
                mission.triggerThree()
                stageThreeStatus = False
                stageOneStatus = True
                #Set time new to restart the countdown
                start = time.time()

        #----------------------------------------------------------------------
        # WRITING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the variables have to be send to external processes and agents
        
        # ----------------- TO - DO -------------------------------------------
                
        # Wait for 1 sec before goig to next execution     
        time.sleep(1)
                
main()



