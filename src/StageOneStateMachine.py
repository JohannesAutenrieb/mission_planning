from statemachine import StateMachine, State

class StageOneStateMachine(StateMachine):

    # Defined States in the Mission State Machine
    startMotor = State('startMotor', initial=True)
    hover = State('hover')
    changeColor = State('changeColor')
    goToEnemiesArea = State('goToEnemiesArea')
    hoverLowAttitude = State('hoverLowAttitude')
    dropPayload = State('dropPayload')
    goToAOI = State('goToAOI')
    hoverInAOI = State('hoverInAOI')

    # Defined Transitions
    reachedAlitude = startMotor.to(hover)
    hoverTimeReached = hover.to(changeColor)
    colorIsChanged = changeColor.to(goToEnemiesArea)
    ReachedEnemiesArea = goToEnemiesArea.to(hoverLowAttitude)
    HoverAltInEnemiesAreaReached = hoverLowAttitude.to(dropPayload)
    PayloadDroped = dropPayload.to(goToAOI)
    BackInAOI = goToAOI.to(hoverInAOI)
    
    # Executed when entering stages
    def on_enter_startMotor(self):
        print('On enter yellow')
    
    def on_enter_hover(self):
        print('On enter yellow')

    def on_enter_changeColor(self):
        print('On enter red')

    def on_enter_goToEnemiesArea(self):
        print('On enter red')

    def on_enter_hoverLowAttitude(self):
        print('On enter red')
        
    def on_enter_dropPayload(self):
        print('On enter red')

    def on_enter_goToAOI(self):
        print('On enter red')

    def on_enter_hoverInAOI(self):
        print('On enter red')

    # Executed when exiting stages        
    def on_exit_startMotor(self):
        print('In green')

    def on_exit_hover(self):
        print('On enter yellow')
        
    def on_exit_changeColor(self):
        print('On enter red')
        
    def on_exit_goToEnemiesArea(self):
        print('On enter red')
        
    def on_exit_hoverLowAttitude(self):
        print('On enter red')
        
    def on_exit_dropPayload(self):
        print('On enter red')

    def on_exit_goToAOI(self):
        print('On enter red')

    def on_exit_hoverInAOI(self):
        print('On enter red')

# Class to manage the states better 
class StageOneState(object):
    def __init__(self, state):
        self.state = state
