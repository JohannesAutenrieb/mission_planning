# Mission Planning & Task Allocation - Team A (Cranfield University)

### Discription
This Software Project was created as part of a UAV Swarm Project in which a Cranfield Student Team participated in the BAE Systems UAV Swarm Challenge. The software contains the Mission Control and Task Allocation system which was utilised for the orchestration of the UAV Swarm. The sytems is embedded in a ROS Framwork which is able to communicate with other Subsytems such as the Agents Autopilot and the Situational Awarness Systems (these software parts are not part of this repository). The Software is able to process the receiving data from Situational Awarness (current Agent and Enemies Inforamtion) and using a combinatorial optimization appraoch to choose suitable countermeasures against incoming threads.

#### Task Allocation Appraoch

The dynamic task allocation approach is to decompose complex multi-task missions in to single-tasks. This simplfies the assignment problem from a complex optimization to a problem which can be solved in optimal manner with linear programming appraoches. For solving this optimization problem following algorithms are implemented:
* Kuhn–Munkres Algorithm
* Jonker-Volgenant Algorithm
* Stable-Marriage Algorithm

The default Algorithm for System is the Kuhn–Munkres Algorithm since it is ensured that it delivers the optimal solution in a polynomial time. The Jonker-Volgenant Algorithm is implemented as an alternative, since it has the potential to solve the problem with an sufficient accuarcy by having a lower computational complexity as the Kuhn–Munkres Algorithm. Nevertheless, is that algorithm currently under testing, it will be implemented in future releases. The stable marriage algorithm is not under use anymore, since both the Jonker-Volgenant and the  Jonker-Volgenant Algorithm delivering better results in terms of a cost optimal solution.

#### Mission Concept

The full mission was seperated in to 3 stages:
* Stage 1: Agent Setup
* Stage 2: Asset Protection (Dynamic Task Allocation)
* Stage 3: Landing 

The distinct stages are implemented as a state machines which is using defined trigger parameter to transit from one stage to another. Inside of stage 1 and stage 3 sub-statemachines are implemented which are ensuring the correct agent workflows in those stages. Stage 2 is fully dynamic and is only using a dynamic task allocation approach as explained prior.

<p align=center>
<img src="https://github.com/JohannesAutenrieb/TeamACranfieldUAVSwarm/blob/master/img/Statemachine_main.png" alt="Statemachine_main" height=500px>
</p>

#### Task Manger
In order to create a fully autonomous mission system a task manager system has been implemented. The task manager is a independent software system which is able to recognise task assignments and to monitor their progress. For that is the process computing a reward for each waypoint or attack task progress of the agents. When it is recognised that the reward is not increasing over a defined time window the assigned task is getting aborted. The same is the case for a task execution which exceeds a certain time window. The time window for each assignened task is individualy defined based on task type, distance and flying speed.

<p align=center>
<img src="https://github.com/JohannesAutenrieb/TeamACranfieldUAVSwarm/blob/master/img/System_Overview.png" alt="System_Overview" height=500px>
</p>


#### Graphical User Interface

The GUI was created to simplify the mission overview for the user during the competition. The GUI-System is fully integrated in to the ROS Network System and is listining to the exchanged messages. Received information are displayed for the user in a Mission Window which is based on the PyQT framework.

<p align=center>
<img src="https://github.com/JohannesAutenrieb/TeamACranfieldUAVSwarm/blob/master/img/GUI_MISSION_OVERVIEW.png" alt="MISSION_GUI" height=500px>
</p>



## Dependencies

The software system us using external libraries which needs to be installed.

Install Rospy for Pyton 3.6:

	sudo pip3 install -U rospkg
	sudo pip3 install roslibpy
	sudo apt-get install python3-yaml
	sudo pip3 install rospkg catkin_pkg

Install PyQt, PyUic4 and PyRcc4:

	sudo apt-get install pyqt4-dev-tools qt4-designer


**The software was tested under Linux Ubuntu Versions 16.04.6 LTS and 18.04.2 LTS*-** 

### Usage

This Software system is using ROS for that reason it needs to be integrated in a Robot Operating System Framework. If not allready existing, a working ROS Workspace needs to be created. If that is the case, please go first to your workspace.

	# Go to your ROS Workspace Directory
	$ cd ~/your_ros_workspace

Next Step is to clone this github repository and use it as a new package:

	$  git clone https://github.com/JohannesAutenrieb/mission_planning.git ./src/mission_planning

The system is build with:
	
	#Building all ROS packages
	$  catkin_make

To have a fucntional Task Allocation sytem the system needs inital agent information to start. When the sytem is not embedded in the completele ROS environment, the publisher.py can be used to fake the swarm:

	# fakes a swarm environment with 5 agents and 2 moving targets
	$  rosrun mission_planning publisher.py

The task allocation software is started with:
	
	$  rosrun mission_planning Main.py

The task manager software is started with:

	$  rosrun mission_planning TaskManager.py

When it is wanted to display the mission via the gui, the gui can started with:

	$  rosrun mission_planning GUI.py


License
-------

Released under the 2-clause GPL GNU license, see `LICENSE`.

Copyright (C) 2019, Johannes Autenrieb and Natalia Strawa
