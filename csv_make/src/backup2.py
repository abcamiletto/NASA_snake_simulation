#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from control_sn.msg import param
import time
import math
import os

x = 0
y = 0
a_p = 0
ot_p = 0
ox_p = 0
a_y = 0
ot_y = 0
ox_y = 0
f = 0.01

time.sleep(4.)

def Callback1(data):
    global x, y
    x = data.x - 0.7
    y = data.y

def Callback2(data):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, V_m, Ph, k, count
    a_p = data.A_p
    ot_p = data.Ot_p
    ox_p = data.Ox_p
    a_y = data.A_y
    ot_y = data.Ot_y
    ox_y = data.Ox_y
    V_m = data.V_m
    Ph = data.Ph
    k = data.K
    count = data.COUNTER

p_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
rospy.init_node('writer_csv')


with open(str(p_path)+"/results/test2.csv", "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerow(['Attempt', 'Amplitude Pitch', 'Spatial frequency Pitch', 'Spatial frequency Pitch', 'Amplitude Yaw', 'Spatial frequency Yaw', 'Temporal frequency Yaw', 'Mean value', 'Phase', 'Constant', 'x', 'y', 'Distanza Totale', 'Distanza Percorsa'])
    wr.writerow([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    writeFile.close()

act_count = 1
act_x = 0
act_y = 0
dist_per = 0
r = rospy.Rate(100)
while not rospy.is_shutdown():

    pos = rospy.Subscriber ('/my_odom', Pose2D, Callback1)
    par = rospy.Subscriber ('/param', param, Callback2)
    dist = math.sqrt(x**2+y**2)
    dist_rel = math.sqrt((x-act_x)**2+(y-act_y)**2)
    dist_per += dist_rel
    if not a_p:
        pass

    else:
        
        line_to_override = {act_count:['Tentativo ' + str(act_count), a_p, ox_p, ot_p, a_y, ox_y, ot_y, V_m, Ph, k, round(x,3), round(y,3), round(dist,3), round(dist_per,3)]}
        act_x = x
        act_y = y
        if act_count == count:
            empty = []
            with open(str(p_path)+"/results/test2.csv", 'r') as readFile:
                read = csv.reader(readFile, dialect='excel')
                empty.extend(read)
            with open(str(p_path)+"/results/test2.csv", 'w') as writeFile:
                wr = csv.writer(writeFile, dialect='excel')
                for line, row in enumerate(empty):
                    data = line_to_override.get(line, row)
                    wr.writerow(data)
                writeFile.close()
            pd = True

            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
            
        else:
            act_count = count
            dist_per = 0
            with open(str(p_path)+"/results/test2.csv", "a") as fp:
                wr = csv.writer(fp, dialect="excel")
                line_to_override = ['Tentativo ' + str(act_count), a_p, ox_p, ot_p, a_y, ox_y, ot_y, V_m, Ph, k, round(x,3), round(y,3), round(dist,3), round(dist_per,3)]
                wr.writerow(line_to_override)
                fp.close()
            pd = True

            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
