#!/bin/sh
cd parameters
. ./sim_param.txt
echo $number_of_joints
echo $radius
echo $lenght
echo $mass
echo $friction
echo $max_effort_pitch
echo $max_effort_yaw

echo Done.

cd ..
cd script
python config_files_yaml_generator.py $number_of_joints

number_of_elements=$(cat numelements_temp.yaml)
echo $number_of_elements
controllerargs=$(cat controllerargs_temp.yaml)
echo $controllerargs
roslaunch snake_description onlyGUI.launch number_of_elements:="$number_of_elements" controller_args:="$controllerargs" diameter_m:="$radius" lenght_m:="$lenght" mass_m:="$mass" friction_m:="$friction" max_ef:="$max_effort_pitch" max_ya:="$max_effort_yaw"
