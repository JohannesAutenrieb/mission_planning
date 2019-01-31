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
#       - commandType (TAKEOFF, LAND, WAYPOINT, PRELEASE) ---> Path planning location to be decided after meeting with dr Shin)
#       - commandValue (float64):
#           * TAKEOFF - height in m
#           * LAND - -1
#           * WAYPOINT - GPS corrrdinates [posX, posY, posZ]
#           * RELSEASE - -1
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
        # Other data:
        self.distance = []

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
    def compute_distance(self):
        # Remove old data
        self.distance.clear()

        # Compute new data
        for friend in range(len(self.friendlyId)):
            for foo in range(len(self.fooId)):
                # Euclidean norm p=2
                self.distance[friend][foo] = sqrt((self.friendlyPos[friend][0] - self.fooPos[foo][0])**2 +\
                                                       (self.friendlyPos[friend][1] - self.fooPos[foo][1])**2 +\
                                                       (self.friendlyPos[friend][2] - self.fooPos[foo][2])**2)

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
                agentsWithoutTask.append(self.friendlyId[friend])

        return agentsWithTask, agentsWithoutTask, agentsInEmergencyMode


    def create_task_message(self, publisher, message, Id, cmdType, cmdValue, time):
        # -----------------------------------------------------------------------------
        # Message structure
        # Id: Id of agents which is task receiver
        # cmdType: List of tasks
        # cmdValue: List of command values (index must coincide with cmdType index)
        # time: current mission time
        # -----------------------------------------------------------------------------

        # Assembly message
        message.agentId = Id
        message.commandType = cmdType
        message.commandValue = cmdValue
        message.timestamp = time

        # Publish message
        publisher.publish(message)



