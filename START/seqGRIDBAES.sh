#!/bin/sh

sleep 3h
killall roscore
sleep 10s
killall -9 gzserver gzclient
sleep 20s

cd parameters
. ./sim_param.txt
echo $number_of_joints
echo $radius
echo $lenght
echo $mass
echo $friction
echo $max_effort

echo Done.

cd ..
cd script
python config_files_yaml_generator.py $number_of_joints

number_of_elements=$(cat numelements_temp.yaml)
echo $number_of_elements
controllerargs=$(cat controllerargs_temp.yaml)
echo $controllerargs
roslaunch snake_description easy_spawn.launch number_of_elements:="$number_of_elements" controller_args:="$controllerargs" diameter_m:="$radius" lenght_m:="$lenght" mass_m:="$mass" friction_m:="$friction" max_ef:="$max_effort"
