#! /usr/bin/env python

import os
from operator import truediv
import rospy, yaml, sys
from std_msgs.msg import Float64
import math
import rospkg
import numpy
from control_sn.msg import param
from geometry_msgs.msg import Point
from std_srvs.srv import Empty
import time
from controller_manager_msgs.srv import SwitchController, SwitchControllerRequest
from sensor_msgs.msg import JointState
from bayes_opt import BayesianOptimization

def Callback1(data):
    global x, y
    x = data.x
    y = data.y

def Callback3(data):
    global tor
    tor = data.effort

rospy.init_node('mycontrol')
num = rospy.get_param('~numb')
time.sleep(6.0)
#INIT PUBLISHER
for i in range(num):
    exec("motor{}p = rospy.Publisher('/snake/snake_body_{}_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))
    exec("motor{}y = rospy.Publisher('/snake/snake_body_{}_aux_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))


pub_param = rospy.Publisher('/param', param, queue_size=10)

en_consuption = rospy.Publisher('/adjusted_energy', JointState, queue_size=10)

rospy.Subscriber('/snake/joint_states', JointState, Callback3)
rospy.Subscriber('/my_odom', Point, Callback1)


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
rospy.sleep(0.1)
pub_param.publish(P)
rospy.sleep(0.3)

n_pti_rand = int(raw_input("Numero di punti iniziali randomici: "))
n_iteraz = int(raw_input("Numero di iterazioni: "))
global fre
fre = float(raw_input("Inserire la frequenza temporale del pitch e dello yaw: "))

bounds_choose = raw_input("Vuoi scegliere gli intervalli dei parametri?:\n[y/n]")
if bounds_choose == 'y':
    amp_p1 = float(raw_input("Ampiezza pitch1: "))
    amp_p2 = float(raw_input("Ampiezza pitch2: "))
    # omt_p1 = float(raw_input("Frequenza temporale pitch1: "))
    # omt_p2 = float(raw_input("Frequenza temporale pitch2: "))
    omx_p1 = float(raw_input("Frequenza spaziale pitch1: "))
    omx_p2 = float(raw_input("Frequenza spaziale pitch2: "))
    amp_y1 = float(raw_input("Ampiezza yaw1: "))
    amp_y2 = float(raw_input("Ampiezza yaw2: "))
    # omt_y1 = float(raw_input("Frequenza temporale yaw1: "))
    # omt_y2 = float(raw_input("Frequenza temporale yaw2: "))
    omx_y1 = float(raw_input("Frequenza spaziale yaw1: "))
    omx_y2 = float(raw_input("Frequenza spaziale yaw2: "))
    phas1 = float(raw_input("Fase1: "))
    phas2 = float(raw_input("Fase2: "))
    val1 = float(raw_input("Valore medio1: "))
    val2 = float(raw_input("Valore medio2: "))
    kos1 = float(raw_input("Costante1: "))
    kos2 = float(raw_input("Costante2: "))
    bounds =  {'a': (amp_p1, amp_p2), 'c': (omx_p1, omx_p2), 'd': (amp_y1, amp_y2), 'f': (omx_y1, omx_y2), 'g': (val1, val2), 'h': (phas1, phas2), 'i': (kos1, kos2)}
else:
    bounds = {'a': (1,2), 'c': (1, 2), 'd': (1,2), 'f': (1, 2), 'g': (1, 2), 'h': (1, 2), 'i': (1, 2)}

print("\nPartire da un valore assegnato? [y/n]\n")
assegnaz = raw_input()

# FUNZIONE DI COSTO DA OTTIMIZZARE

def cost_func(a, c, d, f, g, h, i):

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
    # P.COUNTER = counter
    pub_param.publish(P)

    en = 0
    dist_per = 0
    dist_per_y = 0
    dist_per_x = 0

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
    for i in range(num):
        exec("motor{}p.publish(0.)".format(i))
        exec("motor{}y.publish(0.)".format(i))


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

    # da usare quando pubblicokos = float(raw_input("Costante: "))
    while t < 5:

        x_1 = x
        y_1 = y
        toc = rospy.Time.now() - tic
        t = (toc.secs * (10 ** 9) + toc.nsecs) / (10 ** 9 * 1.0000)

        if (sec % 100 == 0):
            print(str(sec / 100))

        #PUBLISHING THE ADJUSTED ENERGY
        pace = [0]*(num * 2)

        for i in range(num*2):

            if (i % 2) == 0:
                exec("pace[{}] = abs(a_p * ot_y * math.cos(t * ot_y + ox_y * {}))".format(i,i/2))
            else:
                exec("pace[{}] = abs(a_y * ot_p * math.cos(t * ot_p + ox_p * {} + ph))".format(i,(i-1)/2))

        for var in range(num * 2):
            torq = [0] * 2 * num
            torq[var] = abs(tor[var])

        pot = numpy.multiply(pace, torq)
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

        # Con questo if non considero i tempi di accelerazione
        if t < 1:
            pass
        else:    
            # dist_rel = math.sqrt((x-x_1)**2+(y-y_1)**2)
            # dist_per += dist_rel
            en += numpy.sum(pot)
            # vel = dist_per/(sec-100)*100
            # dist_per_y += y - y_1
            # dist_per_x += x - x_1
        pd = True
        while pd:
            try:
                r.sleep()
                pd = False
            except:
                pass

    # counter += 1
    print(en)
    eff = 1/en
    # if x < y/10: 
    return eff*(abs(y)**5)
    # else:
    #     return eff*(abs(y / x)**5)


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

dir = os.path.dirname(os.path.expanduser("~/Scrivania"))
filenm = "parametri_ottimizzati"
path = dir + "/Scrivania/" + filenm + ".txt"

a = optimizer.max['params']
intr = ["\nNel seguente file di testo puoi trovare i parametri ottimi:\nLEGENDA:\n'a' == amp_pitch\t'b' == omega_temp_pitch\t'c' == omega_sp_pitch\t'd' == amp_yaw\t'e' == omega_temp_yaw\t'f' == omega_sp_yaw\t'g' == mean value\t'h' == phase\t'i' == constant\n"]
Row = str(a)
file1 = open(path, "a")
file1.writelines(intr)
file1.write(Row)
file1.close()