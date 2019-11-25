#!/usr/bin/env python

#--------INDICE---------#
#1- importo pacchetti
#2- inizializzo i publisher
#4- definisco i parametri
#5- respawn

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

pub_param = rospy.Publisher ('/param', param, queue_size = 1000)



#4--------------------------------------------------------------------- definisco i parametri

a_p = 0.4
ot_p = 1.8
ox_p = 0.66

a_y = 0.2
ot_y = 1.8
ox_y = 0

v_med = 0.0

#5--------------------------------------------------------------------- pubblico i parametri

P = param()

P.A_p = a_p
P.Ot_p = ot_p
P.Ox_p = ox_p
P.A_y = a_y
P.Ot_y = ot_y
P.Ox_y = ox_y

rospy.sleep(0.1)
pub_param.publish(P)



#6--------------------------------------------------------------------- pubblico nel topic 
tic = rospy.Time.now()
# rateo di pubblicazione in Hz
r = rospy.Rate(100)
#da usare quando pubblico
while not rospy.is_shutdown():
    
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
    msg1y = a_y*math.sin(t * ot_y + ox_y*0) + v_med 
    msg2y = a_y*math.sin(t * ot_y + ox_y*1) + v_med 
    msg3y = a_y*math.sin(t * ot_y + ox_y*2) + v_med
    msg4y = a_y*math.sin(t * ot_y + ox_y*3) + v_med
    msg5y = a_y*math.sin(t * ot_y + ox_y*4) + v_med
    msg6y = a_y*math.sin(t * ot_y + ox_y*5) + v_med
    msg7y = a_y*math.sin(t * ot_y + ox_y*6) + v_med
    
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










