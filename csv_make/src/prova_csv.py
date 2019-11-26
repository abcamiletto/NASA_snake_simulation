#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from control_sn.msg import param

x = 0
y = 0
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
    V_m = data.V_m
    Ph
    k

rospy.init_node('writer_csv')
pos = rospy.Subscriber ('/my_odom', Pose2D, Callback1)
par = rospy.Subscriber ('/param', param, Callback2)

csvfile = "test1.csv"
with open(csvfile, "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerows([['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i']])
    writeFile.close()
while not rospy.is_shutdown():

    i = 1
    if not a_p:
        rospy.sleep(0.01)
    else:
        #csvRow0 = ['Tentativo' + str(i)]
        #csvRow1 = ['Amplitude Pitch', a_p]
        #csvRow2 = ['Spatial frequency Pitch', ox_p]
        #csvRow3 = ['Temporal frequency Pitch', ot_p]
        #csvRow4 = ['Amplitude Yaw',a_y]
        #csvRow5 = ['Spatial frequency Yaw', ox_y]
        #csvRow6 = ['Temporal frequency Yaw', ot_y]
        #csvRow7 = ['x', x]
        #csvRow8 = ['y', y]

        empty = []

        with open("test1.csv", 'r') as readFile:
            read = csv.reader(readFile, dialect='excel')
            empty.extend(read)
            line_to_override = {0:['Tentativo ' + str(i)], 1:['Amplitude Pitch', a_p], 2:['Spatial frequency Pitch', ox_p], 3:['Temporal frequency Pitch', ot_p], 4:['Amplitude Yaw',a_y], 5:['Spatial frequency Yaw', ox_y], 6:['Temporal frequency Yaw', ot_y], 7:['x', x], 8:['y', y]}
            readFile.close()
        with open("test1.csv", 'w') as writeFile:
            wr = csv.writer(writeFile, dialect='excel')
            for line, row in enumerate(empty):
                data = line_to_override.get(line,row)
                wr.writerow(data)
            writeFile.close()
        i+=1
    rospy.sleep(0.2)
rospy.spin()