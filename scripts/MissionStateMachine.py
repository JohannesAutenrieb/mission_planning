from statemachine import StateMachine, State

class MissionStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    init = State('init', initial=True)
    stageOne = State('stageOne')
    stageTwo = State('stageTwo')
    stageThree = State('stageThree')

    # Defined Transitions
    initEnd = init.to(stageOne)
    triggerOne = stageOne.to(stageTwo)
    triggerTwo = stageTwo.to(stageThree)
    
    # Executed when entering stages
    def on_enter_stageOne(self):
        print(":::: STAGE ONE ENTERED :::: ")
    
    def on_enter_stageTwo(self):
        print(":::: STAGE TWO ENTERED :::: ")

    def on_enter_stageThree(self):
        print(":::: STAGE THREE ENTERED :::: ")

    # Executed when exiting stages        
    def on_exit_stageOne(self):
        print("S1:Transition to Stage 2")

    def on_exit_stageTwo(self):
        print("S2:Transition to Stage 3")
        
    def on_exit_stageThree(self):
        print(":::: SYSTEM SHUTDOWN :::: ")

# Class to manage the states better 
class MissionState(object):
    def __init__(self, state):
        self.state = state
