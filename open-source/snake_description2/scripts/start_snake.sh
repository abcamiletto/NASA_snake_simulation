#!/bin/sh

echo How many links?
read number_of_segments

python config_files_yaml_generator.py $number_of_segments

number_of_elements=$(cat numelements_temp.yaml)
echo $number_of_elements
controllerargs=$(cat controllerargs_temp.yaml)
echo $controllerargs
roslaunch snake_description2 init_snake_n.launch number_of_elements:="$number_of_elements" controller_args:="$controllerargs"
