#!/usr/bin/env python

import rospy

from controller_manager_msgs.srv import SwitchController, SwitchControllerRequest


prova = SwitchControllerRequest()
prova.start_controllers = ["joint_state_controller"]
prova.stop_controllers = ["joint_state_controller"]
prova.strictness = 1


aaa = rospy.ServiceProxy('/snake/controller_manager/switch_controller', SwitchController)
resp1 = aaa(prova)



