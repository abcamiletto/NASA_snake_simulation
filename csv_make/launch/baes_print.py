#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState
from control_sn.msg import param, printresu
import math
import os

#STARTING THE NODE
rospy.init_node('writer_csv')
leng = rospy.get_param('~leng')

#DEFINING A DIRECTORY and file name
dir = os.path.dirname(os.path.expanduser("~/Desktop"))
filenm = "baes_search_results"
path = dir + "/Desktop/results/" + filenm + ".csv"

#GLOBAL PARAMATERS
x = 0.0
y = 0.0
z = 0.0
a_p = 0.0
ot_p = 0.0
ox_p = 0.0
a_y = 0.0
ot_y = 0.0
ox_y = 0.0
V_m = 0.0
Ph = 0.0
k = 0.0
count = 0
x_1 = 0.0
y_1 = 0.0
dist = 0.0
power = [0] * (leng*2)
info_to_print = [0] * 5
dist_per = 0.0
dist_z_per = 0.0
en_y = 0.0
en_p = 0.0
en_tot = 0
dist = 0
effic = 0
z_to_add = 0.0
z_med = 0.0


#CALLBACKS FUNCTIONS
def Callback1(data):
    global x_1, y_1, dist, dist_per, dist_z_per, z_med, en_tot, en_p, en_y, effic
    x_1 = data.x_1
    y_1 = data.y_1
    dist = data.dist
    dist_per = data.dist_per
    dist_z_per = data.dist_z_per
    z_med = data.z_med
    en_tot = data.en_tot
    en_p = data.en_p
    en_y = data.en_y
    effic = data.effic


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

#SUBSCRIBERS

rospy.Subscriber('/param', param, Callback2)
rospy.Subscriber('/print', printresu, Callback1)

#WRITING THE FIRST LINE
with open(path, "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerow(['Attempt', 'x', 'y', 'Total Distance', 'Traveled space','Height Variation Stability', 'Mean Height', 'Amplitude Pitch', 'Time frequency Pitch', 'Spatial frequency Pitch', 'Amplitude Yaw', 'Time frequency Yaw', 'Spatial frequency Yaw', 'Mean value', 'Phase', 'Constant', 'Total Energy', 'Pitch Energy', 'Yaw Energy', 'Efficency'])
    writeFile.close()

#PARAMETERS I NEED
act_count = 1


#WRITING THE CSV
r=rospy.Rate(100)
while not rospy.is_shutdown():

    #WAITING FOR THE START
    if not a_p:
        pd = True
        while pd:
            try:
                r.sleep()
                pd = False
            except:
                pass
        pass
    #SNAKE PARAMETERS ARE IN
    else:
        if count == act_count :
            a_p_1 = a_p
            ot_p_1 = ot_p
            ox_p_1 = ox_p
            a_y_1 = a_y
            ot_y_1 = ot_y
            ox_y_1 = ox_y
            V_m_1 = V_m
            Ph_1 = Ph
            k_1 = k
            
            pd = True
            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
            pass

        elif (count == act_count +1):
            #I WRITE THE RESULTS
            #LINE TO BE WRITTEN

            line_to_override = ['Tentativo ' + str(act_count), round(x_1,3), round(y_1,3), round(dist,3), round(dist_per,3),round(dist_z_per,3), round(z_med / 3 ,3), round(a_p_1,3), round(ot_p_1,3), round(ox_p_1), round(a_y_1), round(ot_y_1), round(ox_y_1), round(V_m_1), round(Ph_1), round(k_1) ,round(en_p/200+en_y/200,3), round(en_p/200,3), round(en_y/200,3), round(effic, 3)]

            #APPENDING A NEW LINE
            with open(path, "a") as fp:
                wr = csv.writer(fp, dialect="excel")
                wr.writerow(line_to_override)
                fp.close()

            act_count = count

            pd = True
            while pd:
                try:
                    r.sleep()
                    pd = False
                except:
                    pass
            pass

        else :
            print("SOMETHING WENT REAAAAAAALLY WRONG")
