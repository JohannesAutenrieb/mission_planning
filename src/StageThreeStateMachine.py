from statemachine import StateMachine, State

class StageThreeStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    hoverAtCurrentPosition = State('hoverAtCurrentPosition', initial=True)
    goToWaypoint = State('goToWaypoint')
    landInAOI = State('landInAOI')
    waitOnGround = State('waitOnGround')
    TurnMotorsOff = State('TurnMotorsOff')


    # Defined Transitions
    hoverTimeReached = hoverAtCurrentPosition.to(goToWaypoint)
    reachedAOI = goToWaypoint.to(landInAOI)
    touchedGround = landInAOI.to(waitOnGround)
    timeToTurnOff = waitOnGround.to(TurnMotorsOff)

    
    # Executed when entering stages
    def on_enter_hoverAtCurrentPosition(self):
        print('On enter yellow')
    
    def on_enter_goToWaypoint(self):
        print('On enter yellow')

    def on_enter_landInAOI(self):
        print('On enter red')

    def on_enter_waitOnGround(self):
        print('On enter red')

    def on_enter_TurnMotorsOff(self):
        print('On enter red')
        

    # Executed when exiting stages        
    def on_exit_hoverAtCurrentPosition(self):
        print('In green')

    def on_exit_goToWaypoint(self):
        print('On enter yellow')
        
    def on_exit_landInAOI(self):
        print('On enter red')
        
    def on_exit_waitOnGround(self):
        print('On enter red')
        
    def on_exit_TurnMotorsOff(self):
        print('On enter red')
        

# Class to manage the states better 
class StageThreeState(object):
    def __init__(self, state):
        self.state = state
