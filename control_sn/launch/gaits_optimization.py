#! /usr/bin/env python

import os
from operator import truediv
import rospy, yaml, sys
from std_msgs.msg import Float64
import math
import rospkg
import numpy
from control_sn.msg import param, printresu
from my_odom_publisher.msg import odom
from std_srvs.srv import Empty
import time
from controller_manager_msgs.srv import SwitchController, SwitchControllerRequest
from sensor_msgs.msg import JointState
from bayes_opt import BayesianOptimization

def Callback1(data):
    global x, y, z, dy
    x = data.x
    y = data.y
    z = data.z
    dy = data.diffy

def Callback3(data):
    global tor, veloc
    tor = data.effort
    veloc = data.velocity

rospy.init_node('mycontrol')
num = rospy.get_param('~numb')
time.sleep(6.0)
#INIT PUBLISHER
for i in range(num):
    exec("motor{}p = rospy.Publisher('/snake/snake_body_{}_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))
    exec("motor{}y = rospy.Publisher('/snake/snake_body_{}_aux_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))


pub_param = rospy.Publisher('/param', param, queue_size=10)
PRINT = rospy.Publisher('/print', printresu, queue_size=10)

rospy.Subscriber('/snake/joint_states', JointState, Callback3)
rospy.Subscriber('/my_odom', odom, Callback1)


a = 0
b = 150.0
c = 54.0
d = 0
e = 150.0
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

n_pti_rand = int(raw_input("Number of random initial points: "))
n_iteraz = int(raw_input("Number of iterations: "))
global fre
fre = float(raw_input("Temporal frequence of pitch and yaw: "))
tsec = float(raw_input("Simulation period: "))

bounds_choose = raw_input("Do you want to choose the bounds of parameters?:\n[y/n]")
if bounds_choose == 'y':
    amp_p1 = float(raw_input("Lower bound amplitude pitch: "))
    amp_p2 = float(raw_input("Upper bound amplitude pitch: "))
    # omt_p1 = float(raw_input("Frequenza temporale pitch1: "))
    # omt_p2 = float(raw_input("Frequenza temporale pitch2: "))
    omx_p1 = float(raw_input("Lower bound spatial frequence pitch: "))
    omx_p2 = float(raw_input("Upper bound spatial frequence pitch: "))
    amp_y1 = float(raw_input("Lower bound amplitude yaw: "))
    amp_y2 = float(raw_input("Upper bound amplitude yaw: "))
    # omt_y1 = float(raw_input("Frequenza temporale yaw1: "))
    # omt_y2 = float(raw_input("Frequenza temporale yaw2: "))
    omx_y1 = float(raw_input("Lower bound spatial frequence yaw: "))
    omx_y2 = float(raw_input("Upper bound spatial frequence yaw: "))
    phas1 = float(raw_input("Lower bound phase: "))
    phas2 = float(raw_input("Upper bound phase: "))
    val1 = float(raw_input("Lower bound mean value: "))
    val2 = float(raw_input("Upper bound mean value: "))
    kos1 = float(raw_input("Lower bound constant: "))
    kos2 = float(raw_input("Upper bound constant: "))
    bounds =  {'a': (amp_p1, amp_p2), 'c': (omx_p1, omx_p2), 'd': (amp_y1, amp_y2), 'f': (omx_y1, omx_y2), 'g': (val1, val2), 'h': (phas1, phas2), 'i': (kos1, kos2)}
else:
    bounds = {'a': (30,60), 'c': (15, 85), 'd': (0,40), 'f': (0, 90), 'g': (0, 40), 'h': (0, 10), 'i': (0, 0)}

print("\nDo you want to start from a particular set of parameters? [y/n]\n")
assegnaz = raw_input()

# FUNZIONE DI COSTO DA OTTIMIZZARE

def cost_func(a, c, d, f, g, h, i):

    global counter

    rospy.sleep(0.2)

    attended_en_p = 0
    attended_en_y = 0
    real_en_p = 0.001
    real_en_y = 0.001

    P = param()

    P.A_p = a
    P.Ot_p = fre
    P.Ox_p = c
    P.A_y = d
    P.Ot_y = fre
    P.Ox_y = f
    P.V_m = g
    P.Ph = h
    P.K = i
    P.COUNTER = counter
    pub_param.publish(P)

    a_p = a * 3.14159 / 180
    ot_p = fre * 3.14159 / 180
    ox_p = c * 3.14159 / 180

    a_y = d * 3.14159 / 180
    ot_y = fre * 3.14159 / 180
    ox_y = f * 3.14159 / 180

    v_med = g * 3.14159 / 180
    ph = h * 3.14159 / 180
    k = i * 3.14159 / 180

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
    act_dy = 0.0

    # da usare quando pubblicokos = float(raw_input("Costante: "))
    while t < tsec:

        #UPDATING THE VARIABLES
        x_1 = x
        y_1 = y
        z_1 = z
        dy_1 = dy

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

        attendedpot = numpy.multiply(pace, tor)
        realpot = numpy.multiply(veloc, tor)

        for indx in range(num):
            attended_en_y += abs(attendedpot[int(2*indx)])
            attended_en_p += abs(attendedpot[int(2*indx+1)])
            real_en_y += abs(realpot[int(2*indx)])
            real_en_p += abs(realpot[int(2*indx+1)])

        # DEFINING THE MOVEMENTS

        for i in range(num):
            exec("msg{}p = a_p * math.sin(t * ot_p + ox_p * {})".format(i,i))
            exec("msg{}y = a_y * math.sin(t * ot_y + ox_y * {} + ph) + v_med + {}*k".format(i,i,i))

        # PUBLISHING

        for i in range(num):
            exec("motor{}p.publish(msg{}p)".format(i,i))
            exec("motor{}y.publish(msg{}y)".format(i,i))

        sec += 1

        #CALCULATING OUTPUT OF PROGRESSIVE VALUES
        dist_rel = math.sqrt((x_1-act_x)**2+(y_1-act_y)**2)
        dist_z_rel = math.fabs(z_1-act_z)
        z_to_add = z_1 / 1

            #DESYNC AVOIDANCE
        if (dist_rel < 0.1) :
            dist_per += dist_rel
        else :
            pass

                #HEIGHT TOTAL VARIATION COMPUTING
        if (dist_z_rel < 0.1) :
            dist_z_per += dist_z_rel
        else :
            pass

        z_med += z_to_add

        effic = (abs(y_1))/(attended_en_y + attended_en_p)*100000000

        #KEEPING LAST-1 VALUES IN MEMORY
        act_x = x_1
        act_y = y_1
        act_z = z_1

        pr = printresu()
        pr.x_1 = x_1
        pr.y_1 = y_1
        pr.diffy = dy_1
        pr.dist = math.sqrt(x_1**2+y_1**2)
        pr.dist_per = dist_per
        pr.dist_z_per = dist_z_per
        pr.z_med = z_med
        pr.effic = effic
        pr.real_p_en = real_en_p
        pr.real_y_en = real_en_y
        pr.attended_p_en = attended_en_p
        pr.attended_y_en = attended_en_y
        pr.realpot = realpot
        pr.attendedpot = attendedpot

        PRINT.publish(pr)


        pd = True
        while pd:
            try:
                r.sleep()
                pd = False
            except:
                pass
        pass

    counter += 1


    return effic



# PROCESSO DI OTTIMIZZAZIONE

# DEFINIZIONE DEI CONSTRAINTS

optimizer = BayesianOptimization(
    f=cost_func,
    pbounds=bounds,
    random_state=1,
)

# GUIDING THE OPTIMIZATION: PARTE DA PUNTI ASSEGNATI
if assegnaz == 'y':
    optimizer.probe(
        params={"a": 32,"b": 32, "c": 32, "d": 22, "e": 32, "f": 32, "g": 0.1, "h": 11, "i": 0.24})

optimizer.maximize(
    init_points=n_pti_rand,
    n_iter=n_iteraz,
)

print(optimizer.max)
