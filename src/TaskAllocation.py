
class Task Allocation():
    
    def TaskAssignment(PositionsOfFriends, EnemiesInOurArea, PayloadStatusOfFriends, BatteryStatusOfFriends):
    
        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
        
        #Disctance between Friend and Foos
        shortestDistance=None
        D=None
        closestFriendIdx = None
        friendsIdx = None
        
        #definition of empty lists for return the chosed agents and waypoints
        agentsWithTask = []
        AttackWaypoint = []
        
        #----------------------------------------------------------------------
        # Functionality: Indicating the ideal friend agent for attacking by going 
        # through the list of enemies and matching the next friend agent
        #----------------------------------------------------------------------
        
        for targetIdx in range(0,len(EnemiesInOurArea)):            
         
            #loop over all target drones
            for friendsIdx in range(0,len(PositionsOfFriends)): 
                #x-position of all target drones
                D = compute_distance(EnemiesInOurArea[targetIdx], PositionsOfFriends[friendsIdx])
                
                #for first loop run
                if friendsIdx:
                    closestFriendIdx =friendsIdx
                    shortestDistance = D
                    print("first instance:", closestFriendIdx)
                #update if closer friend agent is found
                else:
                    if shortestDistance >= D:
                        closestFriendIdx =friendsIdx
                        shortestDistance = D
            #Add chosed friend to index list and add target position as waypoint            
            agentsWithTask.append(closestFriendIdx)
            AttackWaypoint.append(EnemiesInOurArea[targetIdx])
    
        return agentsWithTask,AttackWaypoint
    #=================================================
    #
    # More Paramter for cost to follow
    #
    #=================================================
                        
    
    def searchForTargetUAVInOurArea(PositionsOfEnememies):
    
        #Search for Targets in our area (only x component is relevant)
    
        AreaThreshold = 4;                   # threshold in LAt or long (define)
        NumberOfDetectedTargets =len(PositionsOfEnememies)
        
        #definition of empty lists for return the chosed agents and waypoints
        EnemiesInOurArea = []
    #    PositionsofEnememies = 0
    #    PositionsofEnememies=[None] * 20
    
        #loop over all target drones
    
        for targetIdx in range(0,NumberOfDetectedTargets): 
        # x-position of all target drones
            #xTarget = XPositionsofEnememies
            D = PositionsOfEnememies[targetIdx][0] - AreaThreshold
        
            if D<0:
                # add the enemies 
                #TargetFound = True
                EnemiesInOurArea.append(PositionsOfEnememies[targetIdx])
    
        return EnemiesInOurArea
    
    def TaskAllocation():
    
        #----------------------------------------------------------------------
        # Init: Create relevant Objects and global Variables
        #----------------------------------------------------------------------
        #Step 1: Requesting and reading all needed trigger parameters
        
        #Friends related
        PositionsOfFriends = []       #should be given as parameter for Cost calculation
        PayloadStatusOfFriends = []   #should be given as parameter for Cost calculation
        BatteryStatusOfFriends = []   #should be given as parameter for Cost calculation
        
        #Empty List for Agents 
        agentsWithTask = []
        TaskWaypoint = []
    
        #Enemy realated
        PositionsOfEnememies = []     #should be given as parameter from searchForTargetUAV()
        EnemiesInOurArea = searchForTargetUAVInOurArea(PositionsOfEnememies)
        numberOfEnemiesInOurArea = len(EnemiesInOurArea)    #searchForTargetUAVInOurArea
    
               
        #%Step 2: Evaluate Triggers in Mission Tree and find appropriate reaction
    
        if (numberOfEnemiesInOurArea>0):
            
            agentsWithTask,AttackWaypoint = TaskAssignment(PositionsOfFriends, EnemiesInOurArea, PayloadStatusOfFriends, BatteryStatusOfFriends)
    
        #Step 3: Send Task back to agents
        
        # ===== Part with ROS
    
           
    
        #Step 4: Set Tags and go oPout
        
        # ==== Update Flags and Timestamps in Database to update 
        
        def compute_distance(self, availableFriends, unhandledEnemies):
        # Initialize distance list

                agentDistance.append(sqrt((self.friendlyPos[0] - self.fooPos[0])**2 +\
                                                       (self.friendlyPos[1] - self.fooPos[1])**2 +\
                                                       (self.friendlyPos[2] - self.fooPos[2])**2))
        return distance





