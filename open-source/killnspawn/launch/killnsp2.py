#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty

reset = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
resetta_tutto = reset()
