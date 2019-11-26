#!/usr/bin/env python

#--------INDICE---------#
#1- importo pacchetti
#2- inizializzo i publisher
#4- definisco i parametri
#5- respawn
#
#1--------------------------------------------------------------------- importo pacchetti
from operator import truediv
import rospy, yaml, sys
from std_msgs.msg import Float64
from numpy import zeros, array, linspace
import math
import rospkg
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest
import roslaunch
import subprocess
from control_sn.msg import param

rospy.init_node('mycontrol')


#2--------------------------------------------------------------------- inizializzo i publisher

motor1p = rospy.Publisher('/snake/snake_body_1_joint_position_controller/command',Float64, queue_size = 121)
motor1y = rospy.Publisher('/snake/snake_body_1_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor2p = rospy.Publisher('/snake/snake_body_2_joint_position_controller/command',Float64, queue_size = 121)
motor2y = rospy.Publisher('/snake/snake_body_2_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor3p = rospy.Publisher('/snake/snake_body_3_joint_position_controller/command',Float64, queue_size = 121)
motor3y = rospy.Publisher('/snake/snake_body_3_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor4p = rospy.Publisher('/snake/snake_body_4_joint_position_controller/command',Float64, queue_size = 121)
motor4y = rospy.Publisher('/snake/snake_body_4_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor5p = rospy.Publisher('/snake/snake_body_5_joint_position_controller/command',Float64, queue_size = 121)
motor5y = rospy.Publisher('/snake/snake_body_5_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor6p = rospy.Publisher('/snake/snake_body_6_joint_position_controller/command',Float64, queue_size = 121)
motor6y = rospy.Publisher('/snake/snake_body_6_aux_joint_position_controller/command',Float64, queue_size = 121)
    
motor7p = rospy.Publisher('/snake/snake_body_7_joint_position_controller/command',Float64, queue_size = 121)
motor7y = rospy.Publisher('/snake/snake_body_7_aux_joint_position_controller/command',Float64, queue_size = 121)

pub_param = rospy.Publisher('/param', param, queue_size=10)




#4--------------------------------------------------------------------- ricevo i parametri

# def Callback2(data):
#     global a_p, ot_p, ox_p, a_y, ot_y, ox_y, V_m, Ph, k, count
#     a = data.A_p
#     b = data.Ot_p
#     c = data.Ox_p
#     d = data.A_y
#     e = data.Ot_y
#     f = data.Ox_y
#     g = data.V_m
#     h = data.Ph
#     i = data.K
#     count = data.COUNTER
#
# par = rospy.Subscriber ('/param', param, Callback2)


# GRID SEARCH DEFINITIVO
# for ox_y in range()
#     for a_p in range()
#         for a_y in range()
#             for v_med in range()

#
#             for k in range()


a_p = 0
ot_p = 0
ox_p = 0
a_y = 0
ot_y = 0
ox_y = 0
v_med = 0
ph = 0
k = 0
counter = 1

a = range(25)
var1span = [(x*0.35/24 + 0.05) for x in a]




for a_p in var1span:

    print("Tentativo n: " + str(counter) + "/8000 INIZIATO")
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

    a_p = a_p * 3.14159
    ot_p = ot_p * 3.14159
    ox_p = ox_p * 3.14159

    a_y = a_y * 3.14159
    ot_y = ot_y * 3.14159
    ox_y = ox_y * 3.14159

    v_med = v_med * 3.14159
    ph = ph * 3.14159
    k = k * 3.14159



    #6--------------------------------------------------------------------- pubblico nel topic
    tic = rospy.Time.now()
    toc = rospy.Time.now() - tic
    # rateo di pubblicazione in Hz
    r = rospy.Rate(120)
    #da usare quando pubblico
    while toc.secs < 12:

        toc = rospy.Time.now() - tic
        t = (toc.secs * (10**9) + toc.nsecs)/(10**9 * 1.0000)
        print(t)
        #ora assegno le sinusoidali al pitch
        msg1p = a_p*math.sin(t * ot_p + ox_p*0)
        msg2p = a_p*math.sin(t * ot_p + ox_p*1)
        msg3p = a_p*math.sin(t * ot_p + ox_p*2)
        msg4p = a_p*math.sin(t * ot_p + ox_p*3)
        msg5p = a_p*math.sin(t * ot_p + ox_p*4)
        msg6p = a_p*math.sin(t * ot_p + ox_p*5)
        msg7p = a_p*math.sin(t * ot_p + ox_p*6)

        #ora allo yaw
        msg1y = a_y * math.sin(t * ot_y + ox_y * 0 + ph) + v_med + 0 * k
        msg2y = a_y * math.sin(t * ot_y + ox_y * 1 + ph) + v_med + 1 * k
        msg3y = a_y * math.sin(t * ot_y + ox_y * 2 + ph) + v_med + 2 * k
        msg4y = a_y * math.sin(t * ot_y + ox_y * 3 + ph) + v_med + 3 * k
        msg5y = a_y * math.sin(t * ot_y + ox_y * 4 + ph) + v_med + 4 * k
        msg6y = a_y * math.sin(t * ot_y + ox_y * 5 + ph) + v_med + 5 * k
        msg7y = a_y * math.sin(t * ot_y + ox_y * 6 + ph) + v_med + 6 * k

        #pubblico

        motor1p.publish(msg1p)
        motor2p.publish(msg2p)
        motor3p.publish(msg3p)
        motor4p.publish(msg4p)
        motor5p.publish(msg5p)
        motor6p.publish(msg6p)
        motor7p.publish(msg7p)

        motor1y.publish(msg1y)
        motor2y.publish(msg2y)
        motor3y.publish(msg3y)
        motor4y.publish(msg4y)
        motor5y.publish(msg5y)
        motor6y.publish(msg6y)
        motor7y.publish(msg7y)



        r.sleep()

    counter += 1












