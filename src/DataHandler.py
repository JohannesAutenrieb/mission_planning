# ---------------------------------------------
# DATA HANDLING FUNCTIONS
# ---------------------------------------------
import math

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

    def get_friendly_data(self, friendly_package):
        # Remove old data from lists
        self.friendlyId.clear()
        self.friendlyStatus.clear()
        self.friendlyPos.clear()
        self.friendlyBatt.clear()
        self.friendlyTimestamp.clear()
        # Add new data to list
        self.friendlyId.extend(friendly_package[0])
        self.friendlyStatus.extend(friendly_package[1])
        self.friendlyPos.extend(friendly_package[2])
        self.friendlyBatt.extend(friendly_package[3])
        self.friendlyTimestamp.extend(friendly_package[4])

    def get_foo_data(self, fooPackage):
        # Remove old data from lists
        self.fooId.clear()
        self.fooPos.clear()
        self.fooTimestamp.clear()
        # Add new data to list
        self.fooId.extend(fooPackage[0])
        self.fooPos.extend(fooPackage[1])
        self.fooTimestamp.extend(fooPackage[2])

    def compute_distance(self):
        # Remove old data
        self.distance.clear()
        for friend in range(len(self.friendlyId)):
            for foo in range(len(self.fooId)):
                self.distance[friend][foo] = math.sqrt((self.friendlyPos[3*friend] - self.fooPos[3*foo])**2 +\
                                                       (self.friendlyPos[3*friend+1] - self.fooPos[3*foo+1])**2 +\
                                                       (self.friendlyPos[3*friend+2] - self.fooPos[3*foo+2])**2)
