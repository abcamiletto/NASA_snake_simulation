#!/usr/bin/env python

import Tkinter as tk
from Tkinter import *
from operator import truediv
import yaml, sys
from std_msgs.msg import Float64
from numpy import zeros, array, linspace
import math
import rospkg
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest
import roslaunch
import subprocess
from control_sn.msg import param
import rospy
from std_srvs.srv import Empty


a_p = 0
ot_p = 0
ox_p = 0
a_y = 0
ot_y = 0
ox_y = 0
v_med = 0
ph = 0
k = 0
counter = 0
timespan = 6

def init(event):
    global motor1p, motor2p, motor3p, motor4p, motor5p, motor6p, motor7p, motor1y, motor2y, motor3y, motor4y, motor5y, motor6y, motor7y, pub_param

    rospy.init_node('mycontrol')

    motor1p = rospy.Publisher('/snake/snake_body_1_joint_position_controller/command', Float64, queue_size=121)
    motor1y = rospy.Publisher('/snake/snake_body_1_aux_joint_position_controller/command', Float64, queue_size=121)

    motor2p = rospy.Publisher('/snake/snake_body_2_joint_position_controller/command', Float64, queue_size=121)
    motor2y = rospy.Publisher('/snake/snake_body_2_aux_joint_position_controller/command', Float64, queue_size=121)

    motor3p = rospy.Publisher('/snake/snake_body_3_joint_position_controller/command', Float64, queue_size=121)
    motor3y = rospy.Publisher('/snake/snake_body_3_aux_joint_position_controller/command', Float64, queue_size=121)

    motor4p = rospy.Publisher('/snake/snake_body_4_joint_position_controller/command', Float64, queue_size=121)
    motor4y = rospy.Publisher('/snake/snake_body_4_aux_joint_position_controller/command', Float64, queue_size=121)

    motor5p = rospy.Publisher('/snake/snake_body_5_joint_position_controller/command', Float64, queue_size=121)
    motor5y = rospy.Publisher('/snake/snake_body_5_aux_joint_position_controller/command', Float64, queue_size=121)

    motor6p = rospy.Publisher('/snake/snake_body_6_joint_position_controller/command', Float64, queue_size=121)
    motor6y = rospy.Publisher('/snake/snake_body_6_aux_joint_position_controller/command', Float64, queue_size=121)

    motor7p = rospy.Publisher('/snake/snake_body_7_joint_position_controller/command', Float64, queue_size=121)
    motor7y = rospy.Publisher('/snake/snake_body_7_aux_joint_position_controller/command', Float64, queue_size=121)

    pub_param = rospy.Publisher('/param', param, queue_size=1000)

    print("HO INIZIALIZZATO I PUBLISHER")

def start_pub(event):
    # 5--------------------------------------------------------------------- pubblico i parametri

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

    pub_param.publish(P)

    # 6--------------------------------------------------------------------- pubblico nel topic
    tic = rospy.Time.now()
    toc = rospy.Time.now() - tic
    print("ORA PUBBLICOOOOO")
    # rateo di pubblicazione in Hz
    r = rospy.Rate(120)
    # da usare quando pubblico
    while toc.secs < timespan :
        toc = rospy.Time.now() - tic
        t = (toc.secs * (10 ** 9) + toc.nsecs) / (10 ** 9 * 1.0000)
        print(t)
        # ora assegno le sinusoidali al pitch
        msg1p = a_p * math.sin(t * ot_p + ox_p * 0)
        msg2p = a_p * math.sin(t * ot_p + ox_p * 1)
        msg3p = a_p * math.sin(t * ot_p + ox_p * 2)
        msg4p = a_p * math.sin(t * ot_p + ox_p * 3)
        msg5p = a_p * math.sin(t * ot_p + ox_p * 4)
        msg6p = a_p * math.sin(t * ot_p + ox_p * 5)
        msg7p = a_p * math.sin(t * ot_p + ox_p * 6)

        # ora allo yaw
        msg1y = a_y * math.sin(t * ot_y + ox_y * 0 + ph) + v_med + 0*k
        msg2y = a_y * math.sin(t * ot_y + ox_y * 1 + ph) + v_med + 1*k
        msg3y = a_y * math.sin(t * ot_y + ox_y * 2 + ph) + v_med + 2*k
        msg4y = a_y * math.sin(t * ot_y + ox_y * 3 + ph) + v_med + 3*k
        msg5y = a_y * math.sin(t * ot_y + ox_y * 4 + ph) + v_med + 4*k
        msg6y = a_y * math.sin(t * ot_y + ox_y * 5 + ph) + v_med + 5*k
        msg7y = a_y * math.sin(t * ot_y + ox_y * 6 + ph) + v_med + 6*k

        # pubblico
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

def stop_pub(event):
    # 6--------------------------------------------------------------------- pubblico nel topic
    #tic = rospy.Time.now()
    #toc = rospy.Time.now() - tic
    print("ORA PUBBLICOOOOO")
    # rateo di pubblicazione in Hz
    #r = rospy.Rate(120)
    # da usare quando pubblico
    #while toc.secs < 3 :
        # pubblico
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

    #    r.sleep()

def getInput():
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k, timespan

    a_p = float(entry1.get()) * 3.14159
    ot_p = float(entry2.get()) * 3.14159
    ox_p = float(entry3.get()) * 3.14159
    a_y = float(entry4.get()) * 3.14159
    ot_y = float(entry5.get()) * 3.14159
    ox_y= float(entry6.get()) * 3.14159
    v_med = float(entry7.get()) * 3.14159
    ph = float(entry8.get()) * 3.14159
    k = float(entry9.get()) * 3.14159
    timespan = float(entry10.get()) 

    entry10_var.set(timespan)

def LinearProgression(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 0.33
    ot_p = 0.88
    ox_p = 0.29
    a_y = 0.05
    ot_y = 0.88
    ox_y = 0.58
    v_med = 0
    ph = 0
    k = 0.02

    entry1_var.set(a_p)
    entry2_var.set(ot_p)
    entry3_var.set(ox_p)
    entry4_var.set(a_y)
    entry5_var.set(ot_y)
    entry6_var.set(ox_y)
    entry7_var.set(v_med)
    entry8_var.set(ph)
    entry9_var.set(k)


def LateralOndulation(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 0.33
    ot_p = 0.88
    ox_p = 0.29
    a_y = 0.12
    ot_y = 0.88
    ox_y = 0.58
    v_med = 0.1
    ph = 0
    k = 0

    entry1_var.set(a_p)
    entry2_var.set(ot_p)
    entry3_var.set(ox_p)
    entry4_var.set(a_y)
    entry5_var.set(ot_y)
    entry6_var.set(ox_y)
    entry7_var.set(v_med)
    entry8_var.set(ph)
    entry9_var.set(k)

def Rolling():
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 0
    ot_p = 0
    ox_p = 0
    a_y = 0
    ot_y = 0
    ox_y = 0
    v_med = 0
    ph = 0
    k = 0

    entry1_var.set(a_p)
    entry2_var.set(ot_p)
    entry3_var.set(ox_p)
    entry4_var.set(a_y)
    entry5_var.set(ot_y)
    entry6_var.set(ox_y)
    entry7_var.set(v_med)
    entry8_var.set(ph)
    entry9_var.set(k)



def SideWinding(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 0.5
    ot_p = 0.8
    ox_p = 0.6
    a_y = 0.1
    ot_y = 0.8
    ox_y = 0.6
    v_med = 0.0
    ph = 0.0
    k = 0.0

    entry1_var.set(a_p)
    entry2_var.set(ot_p)
    entry3_var.set(ox_p)
    entry4_var.set(a_y)
    entry5_var.set(ot_y)
    entry6_var.set(ox_y)
    entry7_var.set(v_med)
    entry8_var.set(ph)
    entry9_var.set(k)


def Respawn():
    reset = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
    resetta_tutto = reset()




root = tk.Tk()
root.title("Gaits GUI")
root.geometry('500x470')
stline = Frame(root)
stline.pack(side = TOP)
ndline = Frame(root)
ndline.pack(side = TOP)
rdline = Frame(root)
rdline.pack(side = TOP)
forline = Frame(root)
forline.pack(side = TOP)
fifline = Frame(root)
fifline.pack(side = TOP)
sixline = Frame(root)
sixline.pack(side = TOP)
sevline = Frame(root)
sevline.pack(side = TOP)
eigline = Frame(root)
eigline.pack(side = TOP)
ninline = Frame(root)
ninline.pack(side = TOP)
mod = Frame(root)
mod.pack(side = TOP)
las = Frame(root)
las.pack(side = TOP)
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)


entry1_var = DoubleVar()
entry2_var = DoubleVar()
entry3_var = DoubleVar()
entry4_var = DoubleVar()
entry5_var = DoubleVar()
entry6_var = DoubleVar()
entry7_var = DoubleVar()
entry8_var = DoubleVar()
entry9_var = DoubleVar()
entry10_var = DoubleVar()

entry1_var.set(0)
entry2_var.set(0)
entry3_var.set(0)
entry4_var.set(0)
entry5_var.set(0)
entry6_var.set(0)
entry7_var.set(0)
entry8_var.set(0)
entry9_var.set(0)
entry10_var.set(timespan)



initi = Button(stline, text = "Initializing")
lab1 = Label(ndline, text = "Ap", padx=0, pady=5)
lab2 = Label(ndline, text = "Otp", padx=145, pady=5)
lab3 = Label(ndline, text = "Oxp", padx=0, pady=5)
entry1 = Entry(rdline, text=entry1_var)
entry2 = Entry(rdline, text=entry2_var)
entry3 = Entry(rdline, text=entry3_var)
lab4 = Label(forline, text = "Ay", padx=0, pady=5)
lab5 = Label(forline, text = "Oty", padx=145, pady=5)
lab6 = Label(forline, text = "Oxy", padx=0, pady=5)
entry4 = Entry(fifline, text=entry4_var)
entry5 = Entry(fifline, text=entry5_var)
entry6 = Entry(fifline, text=entry6_var)
lab7 = Label(sixline, text = "Vm", padx=0, pady=5)
lab8 = Label(sixline, text = "Ph1", padx=145, pady=5)
lab9 = Label(sixline, text = "Dxl", padx=0, pady=5)
entry7 = Entry(sevline, text=entry7_var)
entry8 = Entry(sevline, text=entry8_var)
entry9 = Entry(sevline, text=entry9_var)
lab10 = Label(ninline, text = "TimeSpan")
entry10 = Entry(ninline, text = entry10_var)
linprog = Button(mod, text = "Magia di Kape")
latond = Button(mod, text = "Magia di Delf")
roll = Button(mod, text = "Rolling")
sidwin = Button(mod, text = "Side Winding")
startpub = Button(bottomFrame, text = "Start Publishing")
stoppub = Button(bottomFrame, text = "Stop Publishing")
shut = Button(bottomFrame, text = "Shutdown")
refresh = Button(eigline, text = "Submit", command = getInput, pady = 10)
respawn = Button(las, text = "Respawn", command = Respawn, pady = 10)

initi.bind("<Button-1>", init)
latond.bind("<Button-1>", LateralOndulation)
startpub.bind("<Button-1>", start_pub)
stoppub.bind("<Button-1>", stop_pub)
sidwin.bind("<Button-1>", SideWinding)


initi.grid(columnspan = 3)
lab1.grid(row=1, column=0)
lab2.grid(row=1, column=1)
lab3.grid(row=1, column=2)
entry1.grid(row=2, column=0)
entry2.grid(row=2, column=1)
entry3.grid(row=2, column=2)
lab4.grid(row=3, column=0)
lab5.grid(row=3, column=1)
lab6.grid(row=3, column=2)
entry4.grid(row=4, column=0)
entry5.grid(row=4, column=1)
entry6.grid(row=4, column=2)
lab7.grid(row=5, column=0)
lab8.grid(row=5, column=1)
lab9.grid(row=5, column=2)
entry7.grid(row=6, column=0)
entry8.grid(row=6, column=1)
entry9.grid(row=6, column=2)
refresh.grid(row= 7, column=0, columnspan = 3)
linprog.grid(row=8, column=0)
latond.grid(row=8, column=1)
roll.grid(row=9, column=0)
sidwin.grid(row=9, column=1)
lab10.grid(row=10, column=0, pady = 10)
entry10.grid(row=10, column=1)
respawn.grid(row=10, column=0)
startpub.grid(row=12, column=0, pady=20)
stoppub.grid(row=12, column=1)
shut.grid(row=12, column=2)
root.mainloop()
