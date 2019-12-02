#!/usr/bin/env python

from operator import truediv
import rospy, yaml, sys
from std_msgs.msg import Float64
from numpy import multiply
import math
import rospkg
from control_sn.msg import param
from std_srvs.srv import Empty
import time
from controller_manager_msgs.srv import SwitchController, SwitchControllerRequest
from sensor_msgs.msg import JointState

tor = [0] * 14

def Callback3(data):
    global tor
    tor = data.effort

rospy.init_node('mycontrol')

time.sleep(6.0)

#INIT PUBLISHER

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

en_consuption = rospy.Publisher('/adjusted_energy', JointState, queue_size=10)

rospy.Subscriber('/snake/joint_states', JointState, Callback3)

#GRID SEARCH PARAMETERS
a_p_span = [20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0] #20,25,30,35,40,45
a_y_span = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 15.0, 22.5, 30.0]
ox_y_span = [108.0, 162.0] #108,162
ph_span = [0.0,7.5,15.0,22.5,30.0]
v_med_span = [0.0,5.0,10.0,15.0,20.0,25.0]
k_span = [0]


a = 0
b = 150
c = 54
d = 0
e = 150
f = 0
g = 0
h = 0
i = 0
counter = 1

#BUG AVOIDANCE
P = param()

P.A_p = a
P.Ot_p = b
P.Ox_p = c
P.A_y = d
P.Ot_y = e
P.Ox_y = f
P.V_m = g
P.Ph = h
P.K = i
P.COUNTER = counter
rospy.sleep(0.1)
pub_param.publish(P)
rospy.sleep(0.3)

# GRID SEARCH
for f in ox_y_span:
    for a in a_p_span:
        for d in a_y_span:
            for h in ph_span:
                for g in v_med_span:

                    print("Tentativo n: " + str(counter) + "/10800 INIZIATO")
                    P = param()

                    P.A_p = a
                    P.Ot_p = b
                    P.Ox_p = c
                    P.A_y = d
                    P.Ot_y = e
                    P.Ox_y = f
                    P.V_m = g
                    P.Ph = h
                    P.K = i
                    P.COUNTER = counter
                    pub_param.publish(P)

                    a_p = a * 3.14159 / 180
                    ot_p = b * 3.14159 / 180
                    ox_p = c * 3.14159 / 180

                    a_y = d * 3.14159 / 180
                    ot_y = e * 3.14159 / 180
                    ox_y = f * 3.14159 / 180

                    v_med = g * 3.14159 / 180
                    ph = h * 3.14159 / 180
                    k = i * 3.14159 / 180

                    motor1p.publish(0.)
                    motor2p.publish(0.)
                    motor3p.publish(0.)
                    motor4p.publish(0.)
                    motor5p.publish(0.)
                    motor6p.publish(0.)
                    motor7p.publish(0.)

                    motor1y.publish(0.)
                    motor2y.publish(0.)
                    motor3y.publish(0.)
                    motor4y.publish(0.)
                    motor5y.publish(0.)
                    motor6y.publish(0.)
                    motor7y.publish(0.)

                    pd = True
                    while pd:
                        try:
                            rospy.sleep(0.1)
                            pd = False
                        except:
                            pass

                    #SNAKE RESPAWN

                    reset = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
                    resetta_tutto = reset()

                    #JOINT_STATE_PUBLISHER RESPAWN (TO AVOID GAZEBO BUG)

                    respawn = SwitchControllerRequest()
                    respawn.start_controllers = ["joint_state_controller"]
                    respawn.stop_controllers = ["joint_state_controller"]
                    respawn.strictness = 1

                    aaa = rospy.ServiceProxy('/snake/controller_manager/switch_controller', SwitchController)
                    resp1 = aaa(respawn)

                    # PUBLISHING
                    sec = 1
                    t = 0
                    tic = rospy.Time.now()
                    toc = rospy.Time.now() - tic

                    # rateo di pubblicazione in Hz
                    r = rospy.Rate(100)

                    # da usare quando pubblico
                    while t < 15:

                        toc = rospy.Time.now() - tic
                        t = (toc.secs * (10 ** 9) + toc.nsecs) / (10 ** 9 * 1.0000)

                        if (sec % 100 == 0):
                            print(str(sec / 100))

                        #PUBLISHING THE ADJUSTED ENERGY
                        pace = [0]*14
                        pace[0] = a_p * ot_p * math.cos(t * ot_p + ox_p * 0 + ph)
                        pace[1] = a_p * ot_p * math.cos(t * ot_p + ox_p * 0)
                        pace[2] = a_p * ot_p * math.cos(t * ot_p + ox_p * 1 + ph)
                        pace[3] = a_p * ot_p * math.cos(t * ot_p + ox_p * 1)
                        pace[4] = a_p * ot_p * math.cos(t * ot_p + ox_p * 2 + ph)
                        pace[5] = a_p * ot_p * math.cos(t * ot_p + ox_p * 2)
                        pace[6] = a_p * ot_p * math.cos(t * ot_p + ox_p * 3 + ph)
                        pace[7] = a_p * ot_p * math.cos(t * ot_p + ox_p * 3)
                        pace[8] = a_p * ot_p * math.cos(t * ot_p + ox_p * 4 + ph)
                        pace[9] = a_p * ot_p * math.cos(t * ot_p + ox_p * 4)
                        pace[10] = a_p * ot_p * math.cos(t * ot_p + ox_p *5 + ph)
                        pace[11] = a_p * ot_p * math.cos(t * ot_p + ox_p *5)
                        pace[12] = a_p * ot_p * math.cos(t * ot_p + ox_p *6 + ph)
                        pace[13] = a_p * ot_p * math.cos(t * ot_p + ox_p *6)

                        pot = multiply(pace, tor)
                        watt = JointState()
                        watt.effort = pot
                        en_consuption.publish(watt)

                        # DEFINING THE  PITCH MOVEMENTS
                        msg1p = a_p * math.sin(t * ot_p + ox_p * 0)
                        msg2p = a_p * math.sin(t * ot_p + ox_p * 1)
                        msg3p = a_p * math.sin(t * ot_p + ox_p * 2)
                        msg4p = a_p * math.sin(t * ot_p + ox_p * 3)
                        msg5p = a_p * math.sin(t * ot_p + ox_p * 4)
                        msg6p = a_p * math.sin(t * ot_p + ox_p * 5)
                        msg7p = a_p * math.sin(t * ot_p + ox_p * 6)

                        # DEFINING THE YAW MOVEMENTS
                        msg1y = a_y * math.sin(t * ot_y + ox_y * 0 + ph) + v_med + 0 * k
                        msg2y = a_y * math.sin(t * ot_y + ox_y * 1 + ph) + v_med + 1 * k
                        msg3y = a_y * math.sin(t * ot_y + ox_y * 2 + ph) + v_med + 2 * k
                        msg4y = a_y * math.sin(t * ot_y + ox_y * 3 + ph) + v_med + 3 * k
                        msg5y = a_y * math.sin(t * ot_y + ox_y * 4 + ph) + v_med + 4 * k
                        msg6y = a_y * math.sin(t * ot_y + ox_y * 5 + ph) + v_med + 5 * k
                        msg7y = a_y * math.sin(t * ot_y + ox_y * 6 + ph) + v_med + 6 * k

                        # PUBLISHING
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

                        sec += 1

                        pd = True
                        while pd:
                            try:
                                r.sleep()
                                pd = False
                            except:
                                pass

                    counter += 1
