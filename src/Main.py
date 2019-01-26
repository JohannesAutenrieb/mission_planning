from MissionStateMachine import MissionStateMachine, MissionState
import time

def main():

    #----------------------------------------------------------------------
    # Init: Create relevant Objects and global Variables
    #----------------------------------------------------------------------
    start = time.time()
    #State object to handle the states
    obj = MissionState(state='stageOne')
    #state machine instance to handle the main state machine
    mission = MissionStateMachine(obj)
    
    
    #Set up of initial state status
    stageOneStatus =True
    stageTwoStatus =False
    stageThreeStatus =False
    
    #Mission Stage Times 
    stageOneDuration= 5
    stageTwoDuration= 5
    stageThreeDuration= 5
    
    while (True):
        #----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        #----------------------------------------------------------------------        
        
        # Here the parameters have to be read
        
        #----------------------------------------------------------------------
        # EXECUTION PART: In This Part The State Machine is Running
        #----------------------------------------------------------------------
        
        #Set current time for this loop run
        currentTime= time.time()
        #Step : Go in to the State Machine and Execute relevant features
        
        if obj.state == 'stageOne':
           print ("1 - Got a true expression value")
           
           if (((currentTime-start)>=stageOneDuration) and (stageOneStatus ==True)):
               #execute statemachine transition with trigger
               mission.triggerOne()
               stageOneStatus =False
               stageTwoStatus = True
               #Set time new to restart the countdown
               start = time.time()
               
        elif obj.state == 'stageTwo':
           print ("2 - Got a true expression value")
           
           
           if (((currentTime-start)>=stageTwoDuration) and (stageTwoStatus ==True)):
                #execute statemachine transition with trigger
                mission.triggerTwo()
                stageTwoStatus = False
                stageThreeStatus = True
                #Set time new to restart the countdown
                start = time.time()
                
        elif obj.state == 'stageThree':
           print ("3 - Got a true expression value")
           
           
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
        
        
                
        # Wait for 1 sec before goig to next execution     
        time.sleep(1)
                
main()



