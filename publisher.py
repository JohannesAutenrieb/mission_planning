#!/usr/bin/env python2.7
import rospy
from mission_planning.msg import AgentInfo, EnemyInfo, SwarmInfo


def talker():
    pub = rospy.Publisher('SwarmInformation', SwarmInfo, queue_size=10)
    rospy.init_node("Halko", anonymous=True)
    rate = rospy.Rate(10) # 10hz


    swarm = SwarmInfo()

    agentList = []
    enemyList = []

    for i in range(0, 6):
        agent = AgentInfo()

        agent.agentId = i + 1
        agent.agentWorkingStatus = True
        agent.agentPosition = [3 * i + 1, 3 * i + 2, 3 * i + 3]
        agent.agentHeading = 0
        agent.agentTaskId = i + 1
        agent.agentTaskStatus = False
        agent.agentBattery = 0.5
        agent.agentPayload = True

        agentList.append(agent)

    for i in range(0, 2):
        enemy = EnemyInfo()
        enemy.agentId = i + 1
        enemy.agentPosition = [8 * i + 1, 8 * i + 2, 8 * i + 3]
        enemy.confidence = 0.75

        enemyList.append(enemy)

    swarm.friendlies = agentList
    swarm.enemies = enemyList

    while not rospy.is_shutdown():

        pub.publish(swarm)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
