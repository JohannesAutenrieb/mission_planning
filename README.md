# TeamACranfieldUAVSwarm

#### Discription
This Software Project was created as part of a UAV Swarm Project in which a Cranfield Student Team Participated in the BAE Systems UAV Swarm Challenge.
The software in this contains the Mission Control and Task Allocation which was used for the orchestration of the UAV Swarm. The sytems is embedded in a ROS Framwork which is able
to communicate with other Subsytems such as the Agents Autopilot and the Situational Awarness Systems. The Software is able to process the receiving data from Situational Awarness (current Agent and Enemies Inforamtion) and using a mathmatical appraoch to choose suitable countermeasures.

#### Task Allocation Appraoch

The dynamic task allocation approach is to decompose complex multui-task missions in to single-task steos. This simplfies the assignment problem from a complex optimization to a problem which can be solved in optimal manner with linear programming appraoches. For solving this combinatorial optimization problem following algorithms are utilized:
* Kuhn–Munkres Algorithm
* Jonker-Volgenant Algorithm
* Stable-Marriage Algorithm

The default Algorithm is the Kuhn–Munkres Algorithm since it is ensured that it delivers the optimal solution. The Jonker-Volgenant Algorithm is currently under testing, since it has the potential to solve the problem with an equal accuarcy by having a lower computational complexity.


<p align=center>
<img src="https://github.com/JohannesAutenrieb/TeamACranfieldUAVSwarm/blob/master/img/GUI_MISSION_OVERVIEW.png" alt="MISSION_GUI" height=300px>
</p>



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



License
-------

Released under the 2-clause GPL GNU license, see `LICENSE`.

Copyright (C) 2019, Johannes Autenrieb and Natalia Strawa
