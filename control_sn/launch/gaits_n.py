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


def Callback3(data):
    global tor
    tor = data.effort

rospy.init_node('mycontrol')
num = rospy.get_param('~numb')
time.sleep(6.0)
tor = [0] * (num * 2)
#INIT PUBLISHER
for i in range(num):
    exec("motor{}p = rospy.Publisher('/snake/snake_body_{}_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))
    exec("motor{}y = rospy.Publisher('/snake/snake_body_{}_aux_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))


pub_param = rospy.Publisher('/param', param, queue_size=10)

en_consuption = rospy.Publisher('/adjusted_energy', JointState, queue_size=10)

rospy.Subscriber('/snake/joint_states', JointState, Callback3)

#GRID SEARCH PARAMETERS
a_p_span = [20.0, 30.0, 40.0, 50.0, 60.0] #20,25,30,35,40,45
ot_p_span = [150.0]
ox_p_span = [20.0,40.0,50.0]
a_y_span = [0.0, 5.0, 10.0, 25.0]
ot_y_span = [150.0]
ox_y_span = [20.0, 40.0, 60.0] #108,162
ph_span = [0.0, 5.0]
v_med_span = [0.0, 10.0]

tent = len(a_p_span)*len(ot_p_span)*len(ox_p_span)*len(a_y_span)*len(ot_y_span)*len(ox_y_span)*len(ph_span)*len(v_med_span)

a = 0
b = 150.0
c = 54.0
d = 0
e = 150.0
f = 0
g = 0
h = 0
noneed = 0.0
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
P.K = noneed
P.COUNTER = counter
rospy.sleep(0.1)
pub_param.publish(P)
rospy.sleep(0.3)

# GRID SEARCH
for b in ot_p_span:
    for e in ot_y_span:
        for c in ox_p_span:
            for f in ox_y_span:
                for a in a_p_span:
                    for d in a_y_span:
                        for h in ph_span:
                            for g in v_med_span:

                                print("TRY n: " + str(counter) + "/" + str(tent) + " STARTED")
                                print("PARAMETERS:     ( " + str(a)+"  "+str(b)+"  "+str(c)+" )     ( "+str(d)+"  "+str(e)+"  "+str(f)+" )    ( "+str(g)+"  "+str(h)) + " )"
                                P = param()

                                P.A_p = a
                                P.Ot_p = b
                                P.Ox_p = c
                                P.A_y = d
                                P.Ot_y = e
                                P.Ox_y = f
                                P.V_m = g
                                P.Ph = h
                                P.K = noneed
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
                                k = noneed * 3.14159 / 180

                                #STRAIGHT LINE
                                for pm in range(num):
                                    exec("motor{}p.publish(0.)".format(pm))
                                    exec("motor{}y.publish(0.)".format(pm))


                                pd = True
                                while pd:
                                    try:
                                        rospy.sleep(0.05)
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
                                    pace = [0]*(num * 2)

                                    for i in range(num*2):

                                        if (i % 2) == 0:
                                            exec("pace[{}] = a_y * ot_y * math.cos(t * ot_y + ox_y * {})".format(i,i/2))
                                        else:
                                            exec("pace[{}] = a_p * ot_p * math.cos(t * ot_p + ox_p * {} + ph)".format(i,(i-1)/2))

                                    pot = multiply(pace, tor)
                                    watt = JointState()
                                    watt.effort = pot
                                    en_consuption.publish(watt)

                                    # DEFINING THE MOVEMENTS

                                    for i in range(num):
                                        exec("msg{}p = a_p * math.sin(t * ot_p + ox_p * {})".format(i,i))
                                        exec("msg{}y = a_y * math.sin(t * ot_y + ox_y * {} + ph) + v_med + {}*k".format(i,i,i))

                                    # PUBLISHING

                                    for i in range(num):
                                        exec("motor{}p.publish(msg{}p)".format(i,i))
                                        exec("motor{}y.publish(msg{}y)".format(i,i))

                                    sec += 1

                                    pd = True
                                    while pd:
                                        try:
                                            r.sleep()
                                            pd = False
                                        except:
                                            pass

                                counter += 1
