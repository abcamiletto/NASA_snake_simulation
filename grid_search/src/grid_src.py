#!/usr/bin/env python

import rospy
from control_sn.msg import param

rospy.init_node('grid')

pub_param = rospy.Publisher ('/param', param, queue_size = 10)


# GRID SEARCH DEFINITIVO
# for ox_y in range()
#     for a_p in range()
#         for a_y in range()
#             for v_med in range()
#
#             for k in range()

# GRID SEARCH DI PROVA
a_p = 0
for a_p in range(5):
    P = param()

    P.A_p = a_p
    P.Ot_p = ot_p
    P.Ox_p = ox_p
    P.A_y = a_y
    P.Ot_y = ot_y
    P.Ox_y = ox_y
    P.V_m = v_med
    P.Ph = ph
    P.K = k
    P.COUNTER = counter

    rospy.sleep(0.1)
    pub_param.publish(P)

    rospy.sleep(3.)
