#!/usr/bin/env python

import rospy, yaml, sys, roslib
from gazebo_msgs.srv import DeleteModel
import roslaunch
import subprocess

rospy.init_node('kns')
#3--------------------------------------------------------------------- killo e rispawno
print('---------------------------KILLO IL MODELLO-------------------------')
#killo model
rospy.wait_for_service("/gazebo/delete_model")
delete = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)
try:
    delete(model_name = "snake")
    # or simply delete("snake")
except rospy.ServiceException as exc:
    print("Service did not process request: " + str(exc))


#print('---------------------------KILLO I NODI--------------.....------')
#killo nodi inutili
try:
    bashCommand = 'rosnode kill /snake/controller_spawner /robot_state_publisher'
    output = subprocess.check_output(['bash','-c', bashCommand])
except:
    print('NOOOOOOOOOO2')
#print('---------------------------SPAWN-------------------------') #POTREI LANCIARE TUTTO DA UN FILE LAUNCH MA DEVO ESSERE SICURO LA PARTE PRIMA SIA FINITA, COME?
#-------SPAWN
#uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#roslaunch.configure_logging(uuid)
#launch = roslaunch.parent.ROSLaunchParent(uuid, 
#["/home/andrea/Desktop/simsnake/src/snake_description2/launch/no_gaz_start.launch"])
#launch.start()

#rospy.sleep(3.)

#--------- SPAWN CONTROLLORE ---- FUNZIONA SOLO DA LINEA DI COMANDO
#print('---------------------------CONTROLLORE-------------------------')
#uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#roslaunch.configure_logging(uuid)
#launch = roslaunch.parent.ROSLaunchParent(uuid, 
#["/home/andrea/Desktop/simsnake/src/control_sn/launch/snake_full_control.launch"])
#launch.start()




