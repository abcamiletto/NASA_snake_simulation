# EELS Simulation and Control
The ROS Melodic and Gazebo 9 setup working on Ubuntu 18.04 LTS, with optimum research algorithms and GUI interface for manual tries.

## Installation

### ROS
To install ROS just follow the tutorial: http://wiki.ros.org/melodic/Installation/Ubuntu

### Gazebo
It should have been installed with the previous steps, if that's not the case follow: http://gazebosim.org/tutorials?tut=install_ubuntu&cat=install

### Prepare files to store env variables
Add this line to your .bashrc. You can find it in your home repository as an hidden file.

`source /opt/ros/kinetic/setup.bash`

### Create a ROS workspace
Let's assume you want to create your workspace on home.

```
mkdir -p ~/eels_ws/src
```

Before continuing source your new setup.*sh file, or add the path to the bashrc as we did before.

`source devel/setup.bash`

### Downloading EELS Setup

Download it from github
```
cd ~/eels_ws/src
git clone https://github.com/abcamiletto/snake.git .
```
For running the Bayesian optimization you need to clone the following repository and install the python module:
```
cd ~/snake/src/snake/control_sn
git clone https://github.com/fmfn/BayesianOptimization.git
pip install bayesian-optimization
```
Now build all the ROS modules

```
cd -
catkin build
```

## Code 
