from statemachine import StateMachine, State

class MissionStateMachine(StateMachine):
    "A traffic light machine"
    stageOne = State('stageOne', initial=True)
    stageTwo = State('stageTwo')
    stageThree = State('stageThree')

    triggerOne = stageOne.to(stageTwo)
    triggerTwo = stageTwo.to(stageThree)
    triggerThree = stageThree.to(stageOne)
    
      
    def on_enter_stageOne(self):
        print('On enter yellow')
    
    def on_enter_stageTwo(self):
        print('On enter yellow')

    def on_enter_stageThree(self):
        print('On enter red')
        
    def on_exit_stageOne(self):
        print('In green')

    def on_exit_stageTwo(self):
        print('On enter yellow')
        
    def on_exit_stageThree(self):
        print('On enter red')

class MissionState(object):
    def __init__(self, state):
        self.state = state