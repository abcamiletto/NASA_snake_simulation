#!/bin/sh

echo How many joints?
read number_of_segments

echo Diameter?
read di

echo Lenght?
read le

python config_files_yaml_generator.py $number_of_segments

number_of_elements=$(cat numelements_temp.yaml)
echo $number_of_elements
controllerargs=$(cat controllerargs_temp.yaml)
echo $controllerargs
roslaunch snake_description easy_spawn.launch number_of_elements:="$number_of_elements" controller_args:="$controllerargs" diameter_m:="$di" lenght_m:="$le"
