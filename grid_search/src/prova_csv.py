#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from control_sn.msg import param

x = 0
y = 0
i = 1
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
    csvRows = [['Tentativo' + str(i)], ['Amplitude Pitch', a_p], ['Spatial frequency Pitch', ox_p], ['Temporal frequency Pitch', ot_p], ['Amplitude Yaw', a_y], ['Spatial frequency Yaw', ox_y], ['Temporal frequency Yaw', ot_y], ['x', x], ['y', y]]
    csvfile = "data.csv"
    with open(csvfile, 'r') as readFile:
        read = csv.reader(readFile, dialect='excel')
        lines = list(read)
        lines[(i-1)*9+1] = csvRows[1], lines[(i-1)*9+2] = csvRows[2], lines[(i-1)*9+3] = csvRows[3], lines[(i-1)*9+4] = csvRows[4], lines[(i-1)*9+5] = csvRows[5], lines[(i-1)*9+6] = csvRows[6], lines[(i-1)*9+7] = csvRows[7], lines[(i-1)*9+8] = csvRows[8], lines[(i-1)*9+9] = csvRows[9],
    with open(csvfile, 'w') as writeFile:
        wr = csv.writer(writeFile, dialect='excel')
        wr.writerows = lines
    readFile.close()
    writeFile.close()
    rospy.sleep(0.2)
