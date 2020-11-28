# robotics_project_dvrk_psm

This robotics project about the PSM arm of the dVRK interfaces with the API of the dVRK tool in ROS and implements a small interface to obtain information from the robot and to impart movements to the robot, by means of forward and inverse kinematics. The latter both in an approximate form (with KDL) and in a closed form (geometric approach).


## How to use this script?

To run the script, first download and install the dVRK tool from [here](https://github.com/jhu-dvrk/sawIntuitiveResearchKit/wiki/CatkinBuild) and then from [here](https://github.com/jhu-dvrk/sawIntuitiveResearchKit/wiki/Kinematics-Simulation)

Later, clone this repo.
Then, start dvrk with this command:

```
roslaunch dvrk_robot dvrk_arm_rviz.launch arm:=PSM1 config:=/home/luca/catkin_ws/src/cisst-saw/sawIntuitiveResearchKit/share/console-PSM1_KIN_SIMULATED.json
```

Then, in another terminal, run the script using python


## But does this script really work?

Yes, you can see it in action in this youtube video:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/V8fZ8WUCJoM/0.jpg)](https://www.youtube.com/watch?v=V8fZ8WUCJoM)
