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

rospy.init_node('writer_csv')

csvfile = "data.csv"
with open(csvfile, "w") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerows([['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i']])
while not rospy.is_shutdown():
    pos = rospy.Subscriber ('/my_odom', Pose2D, Callback1)
    par = rospy.Subscriber ('/param', param, Callback2)

    i = 1

    csvRow0 = ['Tentativo' + str(i)]
    csvRow1 = ['Amplitude Pitch', a_p]
    csvRow2 = ['Spatial frequency Pitch', ox_p]
    csvRow3 = ['Temporal frequency Pitch', ot_p]
    csvRow4 = ['Amplitude Yaw', a_y]
    csvRow5 = ['Spatial frequency Yaw', ox_y]
    csvRow6 = ['Temporal frequency Yaw', ot_y]
    csvRow7 = ['x', x]
    csvRow8 = ['y', y]
    

    with open(csvfile, 'r') as readFile:
        read = csv.reader(readFile, dialect='excel')
        lines = list(read)
        lines[(i-1)*9] = csvRow0, lines[(i-1)*9+1] = csvRow1, lines[(i-1)*9+2] = csvRow2, lines[(i-1)*9+3] = csvRow3, lines[(i-1)*9+4] = csvRow4, lines[(i-1)*9+5] = csvRow5, lines[(i-1)*9+6] = csvRow6, lines[(i-1)*9+7] = csvRow7, lines[(i-1)*9+8] = csvRow8,
    with open(csvfile, 'w') as writeFile:
        wr = csv.writer(writeFile, dialect='excel')
        wr.writerows = lines
    i+=1
    readFile.close()
    writeFile.close()
    rospy.sleep(0.2)
    print (i)