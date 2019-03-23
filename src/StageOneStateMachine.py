from statemachine import StateMachine, State

class StageOneStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    startMotor = State('startMotor', initial=True)
    hover = State('hover')
    goToAOI = State('goToAOI')
    hoverInAOI = State('hoverInAOI')

    # Defined Transitions
    reachedAlitude = startMotor.to(hover)
    hoverTimeReached = hover.to(goToAOI)
    BackInAOI = goToAOI.to(hoverInAOI)
    
    # Executed when entering stages
    def on_enter_startMotor(self):
        print("S1:: Start motor ::")
    
    def on_enter_hover(self):
        print("S1:: Initial hover ::")

    def on_enter_goToAOI(self):
        print("S1:: Go to AoI ::")

    def on_enter_hoverInAOI(self):
        print("S1:: Hover in AoI ::")

    # Executed when exiting stages        
    def on_exit_startMotor(self):
        print("S1: All agents reached altitude")

    def on_exit_hover(self):
        print("S1: Initial hover timeout")

    def on_exit_goToAOI(self):
        print("S1: All agents in AoI")

    def on_exit_hoverInAOI(self):
        print("S1: We are ready to defend hour honor!")

# Class to manage the states better 
class StageOneState(object):
    def __init__(self, state):
        self.state = state
