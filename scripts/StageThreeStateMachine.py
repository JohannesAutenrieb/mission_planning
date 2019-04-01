from statemachine import StateMachine, State

class StageThreeStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    hoverAtCurrentPosition = State('hoverAtCurrentPosition', initial=True)
    goToWaypoint = State('goToWaypoint')
    landInAOI = State('landInAOI')
    waitOnGround = State('waitOnGround')


    # Defined Transitions
    hoverTimeReached = hoverAtCurrentPosition.to(goToWaypoint)
    reachedAOI = goToWaypoint.to(landInAOI)
    touchedGround = landInAOI.to(waitOnGround)

    
    # Executed when entering stages
    def on_enter_hoverAtCurrentPosition(self):
        print("S3:: Hover at current position ::")
    
    def on_enter_goToWaypoint(self):
        print("S3:: Go hostile AoI ::")

    def on_enter_landInAOI(self):
        print("S3:: Land in AoI ::")

    def on_enter_waitOnGround(self):
        print("S3:: Wait on the ground ::")


    # Executed when exiting stages        
    def on_exit_hoverAtCurrentPosition(self):
        print("S3: Hover timeout")

    def on_exit_goToWaypoint(self):
        print("S3: All agents at landing position")
        
    def on_exit_landInAOI(self):
        print("S3: All agents on the ground")
        
    def on_exit_waitOnGround(self):
        print("S3: Disarmed")


# Class to manage the states better 
class StageThreeState(object):
    def __init__(self, state):
        self.state = state
