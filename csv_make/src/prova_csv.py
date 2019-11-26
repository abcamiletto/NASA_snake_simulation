#! /usr/bin/env python

import csv
import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from control_sn.msg import param
import time

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
    x = data.x
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

rospy.init_node('writer_csv')


with open("/home/andrea/Desktop/results/test1.csv", "wb") as writeFile:
    wr=csv.writer(writeFile, dialect='excel')
    wr.writerows([['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j'],['k'],['l']])
    writeFile.close()

act_count = 1

while not rospy.is_shutdown():
    pos = rospy.Subscriber ('/my_odom', Pose2D, Callback1)
    par = rospy.Subscriber ('/param', param, Callback2)

    if not a_p:
        pass

    else:

        line_to_override = {(act_count-1)*12:['-------------------------Tentativo ' + str(act_count)], (act_count-1)*12+1:['Amplitude Pitch', a_p], (act_count-1)*12+2:['Spatial frequency Pitch', ox_p], (act_count-1)*12+3:['Temporal frequency Pitch', ot_p], (act_count-1)*12+4:['Amplitude Yaw',a_y], (act_count-1)*12+5:['Spatial frequency Yaw', ox_y], (act_count-1)*12+6:['Temporal frequency Yaw', ot_y], (act_count-1)*12+7:['Mean value', V_m], (act_count-1)*12+8:['Phase', Ph], (act_count-1)*12+9:['Constant', k], (act_count-1)*12+10:['x', x], (act_count-1)*12+11:['y', y]}
        if act_count == count:
            empty = []
            with open("/home/andrea/Desktop/results/test1.csv", 'r') as readFile:
                read = csv.reader(readFile, dialect='excel')
                empty.extend(read)
                readFile.close()
            with open("/home/andrea/Desktop/results/test1.csv", 'w') as writeFile:
                wr = csv.writer(writeFile, dialect='excel')
                for line, row in enumerate(empty):
                    data = line_to_override.get(line,row)
                    wr.writerow(data)
                writeFile.close()
            time.sleep(f)
            
        else:
            act_count = count
            with open("/home/andrea/Desktop/results/test1.csv", "a") as fp:
                wr = csv.writer(fp, dialect="excel")
                csvRow0 = ['-------------------------Tentativo' + str(act_count)]
                csvRow1 = ['Amplitude Pitch', a_p]
                csvRow2 = ['Spatial frequency Pitch', ox_p]
                csvRow3 = ['Temporal frequency Pitch', ot_p]
                csvRow4 = ['Amplitude Yaw',a_y]
                csvRow5 = ['Spatial frequency Yaw', ox_y]
                csvRow6 = ['Temporal frequency Yaw', ot_y]
                csvRow7 = ['Mean value', V_m]
                csvRow8 = ['Phase', Ph]
                csvRow9 = ['Constant', k]
                csvRow10 = ['x', x]
                csvRow11 = ['y', y]
                wr.writerow(csvRow0), wr.writerow(csvRow1), wr.writerow(csvRow2), wr.writerow(csvRow3), wr.writerow(csvRow4), wr.writerow(csvRow5), wr.writerow(csvRow6), wr.writerow(csvRow7), wr.writerow(csvRow8), wr.writerow(csvRow9), wr.writerow(csvRow10), wr.writerow(csvRow11)
                fp.close()
            time.sleep(f)
