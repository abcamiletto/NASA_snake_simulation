#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from control_sn.msg import param

x = 0
y = 0
i = 0
a_p = 0
ot_p = 0
ox_p = 0
a_y = 0
ot_y = 0
ox_y = 0

def Callback1(data):
    global x, y
    x = data.x
    y = data.y

def Callback2(data):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y
    a_p = data.A_p
    ot_p = data.Ot_p
    ox_p = data.Ox_p
    a_y = data.A_y
    ot_y = data.Ot_y
    ox_y = data.Ox_y

rospy.init_node('writer_csv')

while not rospy.is_shutdown():
    pos = rospy.Subscriber ('/my_odom', Pose2D, Callback1)
    par = rospy.Subscriber ('/param', param, Callback2)
    i+=1
    csvRow = ['Tentativo' + str(i)]
    csvfile = "data.csv"
    with open(csvfile, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(csvRow)
        wr.writerow(['Amplitude Pitch', a_p])
        wr.writerow(['Spatial frequency Pitch', ox_p])
        wr.writerow(['Temporal frequency Pitch', ot_p])
        wr.writerow(['Amplitude Yaw', a_y])
        wr.writerow(['Spatial frequency Yaw', ox_y])
        wr.writerow(['Temporal frequency Yaw', ot_y])
        wr.writerow(['x', x])
        wr.writerow(['y', y])
    rospy.sleep(5)
