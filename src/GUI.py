#!/usr/bin/env python
from PyQt4 import QtGui, QtCore # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
import rospy
import time
import output # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer
from mission_planning.msg import TaskMessage, AgentInfo, SwarmInfo

class ExampleApp(QtGui.QMainWindow, output.Ui_MissionOverview):
    def __init__(self, parent=None):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
                            
        self.taskText= str()
        self.taskList = []
        
        # Set total mission time in seconds
        self.startTime=time.time()
        self.missionTime=600
        self.endTime=self.startTime+self.missionTime
        #Static: Used for progress estimation
        self.totalMissionTime=1000

    def callbackFriend(self, msg):

        # Extract friends information from message
        dataFriend = msg.friendlies
    
        # Iter over list of messages
        for i in range(0, len(dataFriend)):
            # If agent is not on the list, append new agent object
            if(dataFriend[i].agentId==1):
                self.lineEdit_TID_A1.setText(str(dataFriend[i].agentTaskId))
                self.lineEdit_TS_A1.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_WS_A1.setText(str(dataFriend[i].agentWorkingStatus))
                self.lineEdit_Pos_A1.setText(str(dataFriend[i].agentPosition))
                #self.lineEdit_Vel_A1.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_Pay_A1.setText(str(dataFriend[i].agentPayload))
                self.lineEdit_Bat_A1.setText(str(dataFriend[i].agentBattery))
#    
            if(dataFriend[i].agentId==2):
                self.lineEdit_TID_A2.setText(str(dataFriend[i].agentTaskId))
                self.lineEdit_TS_A2.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_WS_A2.setText(str(dataFriend[i].agentWorkingStatus))
                self.lineEdit_Pos_A2.setText(str(dataFriend[i].agentPosition))
                #self.lineEdit_Vel_A1.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_Pay_A2.setText(str(dataFriend[i].agentPayload))
                self.lineEdit_Bat_A2.setText(str(dataFriend[i].agentBattery))
#    
            if(dataFriend[i].agentId==3):
                self.lineEdit_TID_A3.setText(str(dataFriend[i].agentTaskId))
                self.lineEdit_TS_A3.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_WS_A3.setText(str(dataFriend[i].agentWorkingStatus))
                self.lineEdit_Pos_A3.setText(str(dataFriend[i].agentPosition))
                #self.lineEdit_Vel_A1.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_Pay_A3.setText(str(dataFriend[i].agentPayload))
                self.lineEdit_Bat_A3.setText(str(dataFriend[i].agentBattery))
#    
            if(dataFriend[i].agentId==4):
                self.lineEdit_TID_A4.setText(str(dataFriend[i].agentTaskId))
                self.lineEdit_TS_A4.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_WS_A4.setText(str(dataFriend[i].agentWorkingStatus))
                self.lineEdit_Pos_A4.setText(str(dataFriend[i].agentPosition))
                #self.lineEdit_Vel_A1.setText(str(dataFriend[i].agentTaskStatus))
                self.lineEdit_Pay_A4.setText(str(dataFriend[i].agentPayload))
                self.lineEdit_Bat_A4.setText(str(dataFriend[i].agentBattery))
#    
    
        # Extract foos information from message
        dataFoo = msg.enemies
        self.testString=str()
        for i in range(0, len(dataFoo)):
            self.testEnemies="EnemyID: {}  Position: {}  Velocity: {}  Confidence: {} \n \n".format(msg.enemies[i].agentId,msg.enemies[i].agentPosition,msg.enemies[i].agentVelocity,msg.enemies[i].confidence)
            self.testString=self.testString+self.testEnemies
        self.label_enemies.setText(self.testString)
        del self.testString
        
        #Timer
        self. currentTime= time.time()
        self.delta = int(self.endTime - self.currentTime)
        mins, secs = divmod(self.delta, 60)
        self.timeformat = '{:02d}:{:02d}'.format(mins, secs)
        #print(str(self.timeformat))
        self.lineEdit_time.setText(str(self.timeformat))
        
        self.string= "{0:.0%}".format((self.endTime - self.currentTime)/self.missionTime)
        self.label_progress.setText(self.string)

   # Callback for adding new tasks to current Database
    def callbackTaskMessages(self, msg):
        
        self.taskText=msg   
        self.task="AgentID: {}   TaskID: {}   Waypoint: {} \n \n".format(msg.agentId,msg.taskId,msg.taskLocation)
        self.label_task_histo.setText(self.task)
        

    def updater(self):
        
        #update countdown timer
        mins, secs = divmod(self.missionTime, 60)
        self.timeformat = '{:02d}:{:02d}'.format(mins, secs)
        #print(str(self.timeformat))
        self.lineEdit_time.setText(str(self.timeformat))
        # Count one second down        
        self.missionTime -= 1
        

if __name__ == '__main__':
    # Setup System              
    app = QtGui.QApplication(sys.argv)  
    form = ExampleApp()

     # Init of ROS Listener Node
    rospy.init_node('MissionDisplayer', anonymous=True)
    
    # Init Listener for friend and foos
    rospy.Subscriber("SwarmInformation", SwarmInfo, form.callbackFriend)

    # Init Listener to Task Topic
    rospy.Subscriber('TaskAction', TaskMessage, form.callbackTaskMessages)  
    #Execute the GUI            
    form.show()                         
    app.exec_()                         
    # Timer for Time Measurement
    timer = QtCore.QTimer()
    timer.timeout.connect(form.updater)
    timer.setInterval(500)
    timer.start()