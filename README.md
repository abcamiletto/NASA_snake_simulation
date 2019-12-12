# EELS Simulation and Control
The ROS Melodic and Gazebo 9 setup working on Ubuntu 18.04 LTS, with optimum research algorithms and GUI interface for manual tries.

## Installation

### ROS
To install ROS just follow the [main guide](http://wiki.ros.org/melodic/Installation/Ubuntu)

### Gazebo
It should have been installed with the previous steps, if that's not the case follow the [installation tutorial](http://gazebosim.org/tutorials?tut=install_ubuntu&cat=install)

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
cd ~/eels_ws/src/control_sn
git clone https://github.com/fmfn/BayesianOptimization.git
pip install bayesian-optimization
```
Now build all the ROS modules

```
cd -
catkin build
```

## Code 
The simulation is based on an existing snake Gazebo implementation, you can find it [here](http://answers.gazebosim.org/question/16715/how-can-i-represent-a-anake-robot-with-many-identical-segmens-in-sdf/). It's well explained and you can understand the basics of the setup.

### Search algorithms
The two main research algorithm are focused on finding the best gaits with sinusoidal motion of the different motors. In particular, all motors follow two different input whether they control the pitch or yaw degree of freedom.
Let's take a look at the inputs.

![Alt text](yaw1.png?raw=true "Title")
![Alt text](pitch.png?raw=true "Title")


#### Grid Search
aaaaaaaa
#### Baesian Optimization
aaaaaaaa
### Parametrisation
The main variables that can be changed in *src/START/parameters/sim_param.txt* are:

- **number of joints** : It's the number of shoulders. *default = 10* 
- **radius** : It's the radius of a single module, without the screws. *default = 0.0552*
- **lenght** : It's the distance from one shoulder to the following one. *default = 0.35*
- **mass** : It's mass of a single module. *default = 6.75*
- **friction** : It's the friction coefficient. *default = 1.0*
- **max effort pitch** : It's the maximum torque possible on the pitch degree of freedom. *default = 400*
- **max effort yaw** : It's the maximum torque possible on the yaw degree of freedom. *default = 400*

Other parameters you may want to change are:

- **PIDs** : the PIDs of the Yaw and Pitch degree of freedom. You can find them in *src/START/script/config_files_yaml_generator.py*. The default values are P = 3000 for the yaw and P = 11000 for the pitch, both with I and D equal to zero.
- **Grid Search Span**: the mash you want the grid search to look into. You can find it in *src/control_sn/launch/gaits_n.py*
