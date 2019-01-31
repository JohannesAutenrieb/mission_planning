# ---------------------------------------------------------------------------------------
# DATA HANDLING FUNCTIONS
# ---------------------------------------------------------------------------------------
# TO DO:
# - establish GPS coords data format with GNC
# - establish GPS coords data format of competition area we will be provided with
#
# - define list of friendly drone status
# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------
# NOTES:
# - Data structure for GNC commands
#       - friendID
#       - commandType (TAKEOFF, LAND, WAYPOINT, PRELEASE, REPAINT, ABORTMISSION) ---> Path planning location to be decided after meeting with dr Shin)
#       - commandValue (float64):
#           * TAKEOFF - height in m
#           * LAND - -1
#           * WAYPOINT - GPS corrrdinates [posX, posY, posZ]
#           * RELSEASE - -1
#           * REPAINT - -1
#           * ABORTMISSION - -1
#           * GOIDLE - 0
#       - timestamp
# ---------------------------------------------------------------------------------------
from math import sqrt

class DataHandler:

    def __init__(self):
        # Define the input data containers for friends:
        self.friendlyId = []
        self.friendlyStatus = []
        self.friendlyPos = []
        self.friendlyBatt = []
        self.friendlyTimestamp = []

        # Define the input data containers for foos:
        self.fooId = []
        self.fooPos = []
        self.fooTimestamp = []

    def get_friendly_data(self, friendlyPackage):
        # Remove old data from lists
        self.friendlyId.clear()
        self.friendlyStatus.clear()
        self.friendlyPos.clear()
        self.friendlyBatt.clear()
        self.friendlyTimestamp.clear()

        # Add new data to list
        self.friendlyId.extend(friendlyPackage[0])
        self.friendlyStatus.extend(friendlyPackage[1])
        self.friendlyPos.extend(friendlyPackage[2])
        self.friendlyBatt.extend(friendlyPackage[3])
        self.friendlyTimestamp.extend(friendlyPackage[4])

    def get_foo_data(self, fooPackage):
        # Remove old data from lists
        self.fooId.clear()
        self.fooPos.clear()
        self.fooTimestamp.clear()

        # Add new data to list
        self.fooId.extend(fooPackage[0])
        self.fooPos.extend(fooPackage[1])
        self.fooTimestamp.extend(fooPackage[2])

    # Compute distance between foos and enemies
    def compute_distance(self, availableFriends, unhandledEnemies):
        # Initialize distance list
        distance = []
        agentDistance = []

        # Compute new data
        for friend in availableFriends:

            # Find index for the friendly id
            friendlyIndex = self.friendlyId.index(friend)
            agentDistance.clear()

            for foo in unhandledEnemies:

                fooIndex = self.fooId.index(foo)
                # Euclidean norm p=2
                agentDistance.append(sqrt((self.friendlyPos[friendlyIndex][0] - self.fooPos[fooIndex][0])**2 +\
                                                       (self.friendlyPos[friendlyIndex][1] - self.fooPos[fooIndex][1])**2 +\
                                                       (self.friendlyPos[friendlyIndex][2] - self.fooPos[fooIndex][2])**2))
            distance.append(agentDistance)
        return distance

    def get_agents_availability(self):
        # Create empty list of agents with certain status
        agentsWithTask = []
        agentsWithoutTask = []
        agentsInEmergencyMode = []

        # Iterate over list of agents and check they status
        for friend in range(len(self.friendlyStatus)):
            if self.friendlyStatus[friend] == 'IDLE':
                agentsWithoutTask.append(self.friendlyId[friend])
            elif self.friendlyStatus[friend] == 'EMERGENCY':
                agentsInEmergencyMode.append(self.friendlyId[friend])
            else:
                agentsWithTask.append(self.friendlyId[friend])

        return agentsWithTask, agentsWithoutTask, agentsInEmergencyMode


    def create_task_message(self, publisher, message, Id, cmdType, cmdValue, time):
        # -----------------------------------------------------------------------------
        # Message structure
        # Id: Id of agent which is task receiver
        # cmdType: Task name
        # cmdValue: Task value
        # time: current mission time
        # -----------------------------------------------------------------------------

        # Assembly message
        message.agentId = Id
        message.commandType = cmdType
        message.commandValue = cmdValue
        message.timestamp = time

        # Publish message
        publisher.publish(message)



