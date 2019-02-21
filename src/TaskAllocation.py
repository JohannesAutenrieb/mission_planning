import math
from Task import Task, TaskType

class TaskAllocation():
    
    def TaskAssignment(self,PositionsOfFriends, PayloadStatusOfFriends, BatteryStatusOfFriends, freeEnemiesInOurArea, targetConfidence, attackStatus,agentsWithTask,AttackWaypoint):
    
        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
        
        #Disctance between Friend and Foos
        lowestCost=None
        closestFriendIdx = 0
        friendsIdx = None
        
        #CostFunction Weights
        weightDistance= 0.4
        weightPayload= 0.3
        weightBaterystatus= 0.3
        
    
        
        #----------------------------------------------------------------------
        # Functionality: Indicating the ideal friend agent for attacking by going 
        # through the list of enemies and matching the next friend agent
        #----------------------------------------------------------------------
        
        for targetIdx in range(0,len(freeEnemiesInOurArea)):            
            
            #loop over all target drones
            if targetConfidence[targetIdx] > 0.7 and attackStatus[targetIdx]==True:
                for friendsIdx in range(0,len(PositionsOfFriends)): 
                    
                    #x-position of all target drones
                    distance = self.compute_distance(freeEnemiesInOurArea[targetIdx], PositionsOfFriends[friendsIdx])
                    currentCost = weightDistance*distance + weightPayload*PayloadStatusOfFriends[friendsIdx] + weightBaterystatus*BatteryStatusOfFriends[friendsIdx]
                    
                    #for first loop run
                    if friendsIdx==0:
                        closestFriendIdx =friendsIdx
                        lowestCost = currentCost
                        print("first instance:", closestFriendIdx)
                        
                    #update if closer friend agent is found
                    else:
                        if lowestCost >= currentCost:
                            closestFriendIdx =friendsIdx
                            lowestCost = currentCost
                        
            #Add chosed friend to index list and add target position as waypoint
            #closestFriendIdx = int(closestFriendIdx)
            agentsWithTask.append(closestFriendIdx)
            # AttackPosition os allways ten meter before detected position
            AttackWaypoint.append(freeEnemiesInOurArea[targetIdx])
    
        return agentsWithTask,AttackWaypoint
    #=================================================
    #
    # More Paramter for cost to follow
    #
    #=================================================
    
    
    
    def compute_distance(self,unhandledEnemies, availableFriends):
        # Initialize distance list
    
        distance = math.sqrt((availableFriends[0]-unhandledEnemies[0])**2 + (availableFriends[1]-unhandledEnemies[1])**2 + (availableFriends[2]-unhandledEnemies[2])**2)
        return distance

                        
    
    def searchForTargetUAVInOurArea(self, currentEnemyInformation):
    
        #Search for Targets in our area (only x component is relevant)
    
        AreaThreshold = 4    # threshold in LAt or long (define)
        y_axis = 0
        NumberOfDetectedTargets =len(currentEnemyInformation.fooPos)
        
        #definition of empty lists for return the chosed agents and waypoints
        EnemiesInOurArea = []
        targetConfidence = []
        attackStatus = []

        #loop over all target drones   
        for targetIdx in range(0,NumberOfDetectedTargets): 
            # x-position of all target drones
            #Comparing the scalar values in order to decide if in area
            D = currentEnemyInformation.fooPos[targetIdx][y_axis] - AreaThreshold
            # If enemy over threshold assign as possible target to attack
            if D<0:
                # add the enemies 
                EnemiesInOurArea.append(currentEnemyInformation.fooPos[targetIdx])
                targetConfidence.append(currentEnemyInformation.targetConfidence[targetIdx])
                attackStatus.append(currentEnemyInformation.attackStatus[targetIdx])

        return EnemiesInOurArea,targetConfidence,attackStatus
    
    def TaskAllocation(self, currentFriendsInformation, currentEnemyInformation, taskList):
        
        #----------------------------------------------------------------------
        agentsWithTask = []
        AttackWaypoint= []
        
        #Step 1: Analysis if enemies are in our area and how much of them
        freeEnemiesInOurArea, targetConfidence, attackStatus = self.searchForTargetUAVInOurArea(currentEnemyInformation)  
        numberOfEnemiesInOurArea = len(freeEnemiesInOurArea)    #searchForTargetUAVInOurArea
    
        #----------------------------------------------------------------------                      
        #Step 2: Evaluate Triggers in Mission Tree and find appropriate reaction
        if (numberOfEnemiesInOurArea>0):
            agentsWithTask,AttackWaypoint = self.TaskAssignment(currentFriendsInformation.friendlyPos, currentFriendsInformation.friendlyPayload, currentFriendsInformation.friendlyBatt, freeEnemiesInOurArea, targetConfidence, attackStatus,agentsWithTask,AttackWaypoint)
    
        #Step 3: Send Task back to agents        
        # ===== Part with ROS
        for i in range(0, len(agentsWithTask)):
            taskList.append(Task(agentsWithTask[i],TaskType.ATTACK.value,AttackWaypoint[i],0))                
        return 
    
        





