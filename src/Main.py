from MissionStateMachine import MissionStateMachine, MissionState
from StageOne import StageOne
from StageThree import StageThree
import time


def main():
    # ----------------------------------------------------------------------
    # Init: Create relevant Objects and global Variables
    # ----------------------------------------------------------------------

    # take initial time
    startTime = time.time()

    # Mission Stage Times in seconds (currently not real time)
    TotalMissionTime = 125
    StageThreeTime = 120
    MaximumStageTwoTime = TotalMissionTime - StageThreeTime

    # State object to handle the states with initial state one
    obj = MissionState(state='stageOne')

    # state machine instance to handle the main state machine
    mission = MissionStateMachine(obj)

    # Set up of initial state status (inital state one)
    StageOneCompleted = False
    StageThreeCompleted = False

    while (True):
        # ----------------------------------------------------------------------
        # READING PART: In This Part the Messages AND Parameters Are Read
        # ----------------------------------------------------------------------

        # Here the parameters have to be read

        # ----------------- TO - DO -------------------------------------------

        # ----------------------------------------------------------------------
        # EXECUTION PART: In This Part The State Machine is Running
        # ----------------------------------------------------------------------

        # Set current time for this loop run
        currentTime = time.time()
        # Step : Go in to the State Machine and Execute relevant features

        if obj.state == 'stageOne':

            # To-Do as long as in current State
            print("1 - Stage One Entered")
            # Execute Stage One State Machine and return Boolean if executed
            StageOneCompleted = StageOne()
            # print ("Status:", StageOne())

            # Execution of Transition Check and Exit of current State
            if (StageOneCompleted):
                # execute statemachine transition with trigger
                print("Switch Bitch")
                mission.triggerOne()


        elif obj.state == 'stageTwo':

            # To-Do as long as in current State
            print("2 - Got a true expression value")

            # Execution of Transition Check and Exit of current State
            if (((currentTime - startTime) >= MaximumStageTwoTime)):
                # execute statemachine transition with trigger
                mission.triggerTwo()


        elif obj.state == 'stageThree':
            # To-Do as long as in current State
            print("3 - Got a true expression value")

            StageThreeCompleted = StageThree()

            # Execution of Transition Check and Exit of current State
            if (StageThreeCompleted):
                print("We are done with the Mission")
                # Let's go and drink a beer
                return

                # ----------------------------------------------------------------------
        # WRITING PART: In This Part the Messages AND Parameters Are Read
        # ----------------------------------------------------------------------

        # Here the variables have to be send to external processes and agents

        # ----------------- TO - DO -------------------------------------------

        # Wait for 1 sec before goig to next execution


time.sleep(1)


if __name__ == "__main__":
    main()




