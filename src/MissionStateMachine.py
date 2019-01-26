from statemachine import StateMachine, State

class MissionStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    stageOne = State('stageOne', initial=True)
    stageTwo = State('stageTwo')
    stageThree = State('stageThree')

    # Defined Transitions
    triggerOne = stageOne.to(stageTwo)
    triggerTwo = stageTwo.to(stageThree)
    triggerThree = stageThree.to(stageOne)
    
    # Executed when entering stages
    def on_enter_stageOne(self):
        print('On enter yellow')
    
    def on_enter_stageTwo(self):
        print('On enter yellow')

    def on_enter_stageThree(self):
        print('On enter red')

    # Executed when exiting stages        
    def on_exit_stageOne(self):
        print('In green')

    def on_exit_stageTwo(self):
        print('On enter yellow')
        
    def on_exit_stageThree(self):
        print('On enter red')

# Class to manage the states better 
class MissionState(object):
    def __init__(self, state):
        self.state = state
