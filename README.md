# EELS Simulation and Control
The ROS Melodic and Gazebo 9 setup working on Ubuntu 18.04 LTS, with optimum research algorithms and GUI interface for manual tries.



![Gif2](https://github.com/abcamiletto/eels_sim/blob/master/images_and_videos/ezgif-7-d21902ae1d3a.gif?raw=true)
## Installation

### ROS
To install ROS just follow the [main guide](http://wiki.ros.org/melodic/Installation/Ubuntu)

After that, you need to install ROS control package, just:

`sudo apt-get install ros-melodic-ros-control ros-melodic-ros-controllers`

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

![Gif1](https://github.com/abcamiletto/eels_sim/blob/master/images_and_videos/image_2019-12-19_17-21-17.png?raw=true)

### Search algorithms
The two main research algorithm are focused on finding the best gaits with sinusoidal motion of the different motors. In particular, all motors follow two different input whether they control the pitch or yaw degree of freedom.
Let's take a look at the inputs.

![Alt text](images_and_videos/yaw1.png?raw=true "Title")

![Alt text](images_and_videos/pitch.png?raw=true "Title")

Where n is the number of the joint they're in.

#### Grid Search
In this type of search we're doing a brute force research on pre-defined bounds. It prints a csv files in a Desktop folder "results" in which you can see all the results it achieved.

#### Baesian Optimization

As in other kinds of optimization, in Bayesian optimization we search the maximum of a function *f(**x**)* on some bounded set of parameters **x**. The logic at the base is to construct a probabilistic model for *f(**x**)* and then exploits the model to make decisions about where in **x** next to evaluate the function. To accomplish this task you need to choose an acquisition function used to construct the utility function chich choose the next point to evaluate. In our optimization we use the **Upper confidence bound (UCB)** and the trade-off between exploitation and exploration is controlled by the free parameter *k*.

The **Bayesian Optimization** is a most adequate and efficient for environments which sampling functions to be optimized is a very expensive work, that's due to the few evaluations needed. However the cost is to perform more computation to determine next point to try.

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
- **Grid Search Span** : the mash you want the grid search to look into. You can find it in *src/control_sn/launch/gaits_n.py*
- **Baesian Optimization** : 
    - DEFAULT VALUES:
        - the free parameter *k* (balance between exploration and exploitation); in our case it was fixed at the default value ie *k = 2.576*;
        - the utility function: the choice is between the *Probability of Improvement* ("poi"), the *Expected Improvement* ("ei") and the *Upper Confidence Bound* ("ucb"). By default the utility function is UCB;
    
    You can add them in */src/control_sn/launch/gaits_optimization.py* as arguments to the *maximize* function (at the bottom of the script). An example might be: 
    ```
    optimizer.maximize(
        init_points=n_pti_rand,
        n_iter=n_iteraz,
        acq='ei',
        kappa=2.576,
    )
    ```
    - "Efficiency" function: in order to modify the efficiency (the output of each simulation which is taken into account by the optimization algorithm) you should open the *gaits_optimization.py* in the repository *src/control_sn/launch* and modify the line 262. Currently our efficiency is:
    
    ![Alt text](images_and_videos/eff.png?raw=true "Title")
    
