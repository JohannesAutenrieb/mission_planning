# TeamACranfieldUAVSwarm

<p align=center>
<img src="https://github.com/JohannesAutenrieb/TeamACranfieldUAVSwarm/blob/master/img/GUI_MISSION_OVERVIEW.png" alt="MISSION_GUI" height=800px>
</p>


This Project is utilized for single tasks task allocation scenarios wiht multiple drones.

The project is used for a student group project of students from cranfield university.

#### Dependencies

Install Rospy for Pyton 3.6:

	sudo pip3 install -U rospkg
	sudo pip3 install roslibpy
	sudo apt-get install python3-yaml
	sudo pip3 install rospkg catkin_pkg

Install PyQt, PyUic4 and PyRcc4:

	sudo apt-get install pyqt4-dev-tools qt4-designer


Tested under Linux Ubuntu Versions 16.04.6 LTS and 18.04.2 LTS 

### Usage

This Software system was integrated in Robot Operating System Framework. Thefore a working ROS Enrivoment needs to be created. If that is the case, please go first to your workspace.

	# You should have created Workspace in which the package can be created
	$ cd ~/catkin_ws/src

Next Step is to create a new package in that worksapce:

	$ catkin_create_pkg mission_planning message_generation rospy

After this you need to ajust your CMakeLists.txt file and your package.xml in order to make the needed customized ROS packages known to the ROS framework. Please search for the part in which the messages are generated **add_message_files()**
and please substitute with the following code part:
'''
	
 add_message_files(
   FILES
   TaskMessage.msg
   AgentInfo.msg
   SwarmInformation.msg
   TargetInformation.msg
   TaskStatusMessage.msg
   RewardMessage.msg
   TaskStatusInformation.msg
   SystemStatusMessage.msg
   InitMessage.msg
   SwarmInfo.msg
   EnemyInfo.msg
)


'''



License
-------

Released under the 2-clause BSD license, see `LICENSE`.

Copyright (C) 2012-2017, Tomas Kazmar
