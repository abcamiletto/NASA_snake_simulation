#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState
from control_sn.msg import param
import math
import os

#STARTING THE NODE
rospy.init_node('writer_csv')
leng = rospy.get_param('~leng')

#DEFINING A DIRECTORY and file name
dir = os.path.dirname(os.path.expanduser("~/Desktop"))
filenm = "PROVA_NNNNNNNN"
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
power = [0] * (leng*2)
dist_per = 0.0
dist_z_per = 0.0
en_y = 0.0
en_p = 0.0
z_to_add = 0.0
z_med = 0.0


#CALLBACKS FUNCTIONS
def Callback1(data):
    global x, y, z
    x = data.x
    y = data.y
    z = data.z

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

def Callback3(data):
    global power
    power = data.effort

#SUBSCRIBERS
rospy.Subscriber('/snake/joint_states', JointState, Callback3)
rospy.Subscriber('/my_odom', Point, Callback1)
rospy.Subscriber('/param', param, Callback2)

#WRITING THE FIRST LINE
with open(path, "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerow(['Attempt', 'x', 'y', 'Total Distance', 'Traveled space','Height Variation Stability', 'Mean Height', 'Amplitude Pitch', 'Time frequency Pitch', 'Spatial frequency Pitch', 'Amplitude Yaw', 'Time frequency Yaw', 'Spatial frequency Yaw', 'Mean value', 'Phase', 'Constant', 'Total Energy', 'Pitch Energy', 'Yaw Energy'])
    writeFile.close()

#PARAMETERS I NEED
act_count = 1
act_x = 0
act_y = 0
act_z = 0

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
            #UPDATING THE VARIABLES
            a_p_1 = a_p
            ot_p_1 = ot_p
            ox_p_1 = ox_p
            a_y_1 = a_y
            ot_y_1 = ot_y
            ox_y_1 = ox_y
            V_m_1 = V_m
            Ph_1 = Ph
            k_1 = k
            x_1 = x
            y_1 = y
            z_1 = z

            #CALCULATING OUTPUT OF PROGRESSIVE VALUES
            dist_rel = math.sqrt((x_1-act_x)**2+(y_1-act_y)**2)
            dist_z_rel = math.fabs(z_1-act_z)
            z_to_add = z_1 / 1

                #DESYNC AVOIDANCE
            if (dist_rel < 0.1) :
                dist_per += dist_rel
            else :
                pass

                #ENERGY COMPUTING
            for indx in range(0,leng):
                if power[int(2*indx)] > 0 and power[int(2*indx)] < 0.5:
                    en_y += power[int(2*indx)]
                if power[int(2*indx+1)] > 0 and power[int(2*indx+1)] < 0.5 :
                    en_p += power[int(2*indx+1)]

                    #HEIGHT TOTAL VARIATION COMPUTING
            if (dist_z_rel < 0.1) :
                dist_z_per += dist_z_rel
            else :
                pass

            z_med += z_to_add

                #KEEPING LAST-1 VALUES IN MEMORY
            act_x = x_1
            act_y = y_1
            act_z = z_1

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
            line_to_override = ['Tentativo ' + str(act_count), round(x_1,3), round(y_1,3), round(math.sqrt(act_x**2+act_y**2),3), round(dist_per,3),round(dist_z_per,3), round(z_med,4), a_p_1, ot_p_1, ox_p_1, a_y_1, ot_y_1, ox_y_1, V_m_1, Ph_1, k_1,round(en_p/200+en_y/200,3), round(en_p/200,3), round(en_y/200,3)]

            #APPENDING A NEW LINE
            with open(path, "a") as fp:
                wr = csv.writer(fp, dialect="excel")
                wr.writerow(line_to_override)
                fp.close()

            act_count = count

            #RESETTING NEEDED PARAMETERS
            act_x = 0.0
            act_y = 0.0
            act_z = 0.0
            dist_rel= 0.0
            dist_per = 0.0
            dist_z_per = 0.0
            dist_z_rel = 0.0
            z_med = 0.0
            z_to_add = 0.0
            en_p = 0.0
            en_y = 0.0

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
