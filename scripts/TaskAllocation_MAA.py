import math
from operator import itemgetter
from Task import Task, TaskType
from munkres import Munkres, print_matrix

class TaskAllocation_MAA():
    def __init__(self):
        
        # ----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        # ----------------------------------------------------------------------

        self.m = Munkres()
    
    def TaskAssignment(self, agentsList, fooList):

        #TaskAssignment(agentsList.friendlyPos, agentsList.friendlyPayload, agentsList.friendlyBatt, freeEnemiesInOurArea, targetConfidence, attackStatus,agentsWithTask,AttackWaypoint, estimatedDeadline)
        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------     
        #Disctance between Friend and Foos

        lowestCost = int()
        closestFriendIdx = int()
        friendsIdx = None
        # Estimation of Deadline
        averageSpeed = 1 # (m/s)
        minimumSpeed = 0.5*averageSpeed # (m/s)
        deadline = 0
        #Maximum possible distance of battlefield to normlize the computed distance
        maximumDistance = 0
        
        # local list variablse
        agentsWithTask = list()
        attackWaypoint = list()
        estimatedDeadline = list()
        attackedTargets = list()

        #CostFunction Weights
        weightDistance = 0.3147
        weightPayload = 0.0290
        weightBaterystatus = 0.9488
        weightBias = -0.0025

        # Max distance for distance normalization in cost function
        max_x = 50          # [m]
        max_y = 100         # [m]
        max_z = 120         # [m]
        maxDistance = math.sqrt(max_x**2 + max_y**2 + max_z**2)

        # Set the battery level treshold
        batteryTreshold = 0.3    # [%]

        # Task allocation algorithm containers
        costMatrix = list()               # List of cost function values
        costEnemy = list()                # List of cost function values
        deadlineList = list()        # List of cost function values
        deadLineMatrix = list()        # List of cost function values
        foosPreferences = dict()          # Dictionary: key - foo index | value - friend index
        friendsPreferences = dict()       # Dictionary: key - friend index | value - foo index
        deadlineDict = dict()             # Dictionary: key - (friend index,  foo index) | value - deadline


        #----------------------------------------------------------------------
        # Functionality: Indicating the ideal friend agent for attacking by going 
        # through the list of enemies and matching the next friend agent
        #----------------------------------------------------------------------
        print("S2: Allocating tasks... ")
        # loop over all target drones
        for enemy in fooList:
            if (enemy.confidence > 0.7) and (enemy.attackStatus is False):

                # Loop over all agents
                for friend in agentsList:
                    # Check if battery status is not too low abd if agent is not allready in task
                    if (friend.agentBattery > batteryTreshold) and (friend.taskStatus is False) and (friend.agentWorkingStatus is True):

                        #x-position of all target drones
                        distance = self.compute_distance(enemy.agentFuturePositon, friend.agentPos)
                        distanceNormalized = distance/maxDistance
                        currentCost = weightBias + weightDistance*distanceNormalized + weightPayload*friend.agentPayload + weightBaterystatus/friend.agentBattery
                        deadline = (distance / minimumSpeed)+20
                        
                        costEnemy.append(currentCost)
                        deadlineList.append(deadline)

                # Append cost values value to the matrix
                costMatrix.append(costEnemy)
                deadLineMatrix.append(deadlineList)
                print(deadLineMatrix)
                costEnemy=[]
                deadlineList=[]
#                # Append deadline value to the list [foo, friend, deadline]
#                deadlineDict[(enemy.agentId, friend.agentId)] = deadline
        
        #Evaluate the Cost Matrix of the current run
        # Switch columns to rows
        costMatrix = map(list,map(None,*costMatrix))
        
        # Computing of Munkres Algorithm on current Cost Matrix
        indexes = self.m.compute(costMatrix)

        # Add chose friend to index list and add target position as waypoint
        # closestFriendIdx = int(closestFriendIdx)
        print("S2:: Task assignment ::")
        for row, column in indexes:
            friendIdx = row
            enemyIdx = column
            
            friendId = row +1
            enemyId = column + 1
            
            agentsWithTask.append(friendId)
            attackedTargets.append(enemyId)
            # AttackPosition is always ten meter before detected position
            attackWaypoint.append(fooList[enemyIdx].agentFuturePositon)
            estimatedDeadline.append(deadLineMatrix[enemyIdx][friendIdx])
            # Change enemy's attack status to True
            setattr(fooList[enemyIdx], 'attackStatus', True)
            setattr(fooList[enemyIdx], 'attackingAgent', friendId)
            print("Agent: ", friendId, "attacks foo: ", enemyId)

        print('-------------------------------------')
        print("S2: Attack status:")
        print("Agents with task: ", agentsWithTask)
        print("Attacked targets: ", attackedTargets)
        print("Waypoints: ", attackWaypoint)
        print("Deadlines: ", estimatedDeadline)
        print('-------------------------------------')

        del costMatrix[:]
        foosPreferences.clear()
        friendsPreferences.clear()
        deadlineDict.clear()

        return agentsWithTask, attackedTargets, attackWaypoint, estimatedDeadline
    #=================================================
    #
    # More Paramter for cost to follow
    #
    #=================================================
    

    def compute_distance(self,unhandledEnemies, availableFriends):
        # Initialize distance list
    
        distance = math.sqrt((availableFriends[0]-unhandledEnemies[0])**2 + (availableFriends[1]-unhandledEnemies[1])**2 + (availableFriends[2]-unhandledEnemies[2])**2)
        return distance

                        
    #Not n
    def searchForTargetUAVInOurArea(self, fooList):
    
        #Search for Targets in our area (only x component is relevant)
    
        AreaThreshold = 4    # threshold in LAt or long (define)
        y_axis = 0
        NumberOfDetectedTargets =len(fooList.fooPos)
        
        #definition of empty lists for return the chosed agents and waypoints
        EnemiesInOurArea = []
        targetConfidence = []
        attackStatus = []

        #loop over all target drones   
        for targetIdx in range(0,NumberOfDetectedTargets): 
            # x-position of all target drones
            #Comparing the scalar values in order to decide if in area
            D = fooList.fooPos[targetIdx][y_axis] - AreaThreshold
            # If enemy over threshold assign as possible target to attack
            if D<0:
                # add the enemies 
                EnemiesInOurArea.append(fooList.fooPos[targetIdx])
                targetConfidence.append(fooList.targetConfidence[targetIdx])
                attackStatus.append(fooList.attackStatus[targetIdx])

        return EnemiesInOurArea,targetConfidence,attackStatus

    def MatchMaker(self, sortedFoosPrefs, foosPreferences, friendsPreferences):

        # Foos that are still umatched
        foosFree = sortedFoosPrefs[:]
        # Matched pairs foo - friend
        matches = {}
        foosPrefer = foosPreferences
        friendsPrefer = friendsPreferences
        # Do as long as there are unmatched foos
        while foosFree:
            # Pick the first foo from the list and remove it from the list
            foo = foosFree.pop(0)
            # Extract the list of foos preferences
            foosList = foosPrefer[foo]
            # Pick the first friend from the list and remove it from the list
            friend = foosList.pop(0)
            # Check if this friend is already matched with any target
            assigned = matches.get(friend)
            # If not assigned, assign current foo
            if not assigned:
                # Agent's free
                matches[friend] = foo
            # Else friend is already assigned to other foo
            else:
                # Extract list of friend preferences
                friendsList = friendsPrefer[friend]
                # Check if current foo is higher in friend's preference list than its current assignment
                if friendsList.index(assigned) > friendsList.index(foo):
                    # New foo is better match
                    matches[friend] = foo
                    # If rejected foo has still some agents on the list
                    if foosPrefer[assigned]:
                        # Add it again to unassigned foos list
                        foosFree.append(assigned)
                else:
                    # Previously assigned foo was better match
                    # If there are any other friends on foos list
                    if foosList:
                        # Search again, mark foo as free
                        foosFree.append(foo)
        return matches

    
    def TaskAllocation(self, agentsList, fooList, taskList):
        
        # ----------------------------------------------------------------------
        agentsWithTask = list()
        attackedTargets = list()
        AttackWaypoint = list()
        estimatedDeadline = list()

        print("\nT: SITUATION ANALYSIS")
        print("T: Friends in our area:")
        for agent in agentsList: print "%d" % agent.agentId,
        print ("\nT: Foos in our area:")
        for foo in fooList: print "%d" % foo.agentId,
        print("\nT: Confidence of Foos:")
        for foo in fooList: print "%3.2f" % foo.confidence,
        print("\nT: Attack Status:")
        for foo in fooList: print "%d" % foo.attackStatus,
        print("\n")
    
        # ----------------------------------------------------------------------
        # Step 2: Evaluate Triggers in Mission Tree and find appropriate reaction
        if any(foo.attackStatus is False for foo in fooList):
            agentsWithTask, attackedTargets, AttackWaypoint, estimatedDeadline = self.TaskAssignment(agentsList, fooList)
    
        # Step 3: Send Task back to agents
        # ===== Part with ROS
        for i in range(0, len(agentsWithTask)):
            print("Agents with Task:", agentsWithTask)
            taskList.append(Task(agentsWithTask[i], attackedTargets[i], TaskType.ATTACK.value, AttackWaypoint[i], estimatedDeadline[i]))
        return



        





