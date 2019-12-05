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


num = 0
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

rospy.init_node('mycontrol')
num = rospy.get_param('~numb')

global pub_param, num
for i in range(num):
    exec("global motor{}p, motor{}p".format(i,i))

for i in range(num):
        exec("motor{}p = rospy.Publisher('/snake/snake_body_{}_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))
        exec("motor{}y = rospy.Publisher('/snake/snake_body_{}_aux_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))

pub_param = rospy.Publisher('/param', param, queue_size=1000)


def init(event):

    rospy.init_node('mycontrol')
    num = rospy.get_param('~numb')

    for i in range(num):
        exec("motor{}p = rospy.Publisher('/snake/snake_body_{}_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))
        exec("motor{}y = rospy.Publisher('/snake/snake_body_{}_aux_joint_position_controller/command',Float64, queue_size = 121)".format(i,i))

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
        for i in range(num):
            exec("msg{}p = a_p * math.sin(t * ot_p + ox_p * {})".format(i,i))
            exec("msg{}y = a_y * math.sin(t * ot_y + ox_y * {} + ph) + v_med + {}*k".format(i,i,i))

        # PUBLISHING

        for i in range(num):
            exec("motor{}p.publish(msg{}p)".format(i,i))
            exec("motor{}y.publish(msg{}y)".format(i,i))

        r.sleep()

def stop_pub(event):
    # 6--------------------------------------------------------------------- pubblico nel topic

    print("ORA PUBBLICOOOOO")

    for i in range(num):
        exec("motor{}p.publish(0.)".format(i))
        exec("motor{}y.publish(0.)".format(i))


def getInput():
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k, timespan

    a_p = float(entry1.get()) * 3.14159 / 180
    ot_p = float(entry2.get()) * 3.14159 / 180
    ox_p = float(entry3.get()) * 3.14159 / 180
    a_y = float(entry4.get()) * 3.14159 / 180
    ot_y = float(entry5.get()) * 3.14159 / 180
    ox_y= float(entry6.get()) * 3.14159 / 180
    v_med = float(entry7.get()) * 3.14159 / 180
    ph = float(entry8.get()) * 3.14159 / 180
    k = float(entry9.get()) * 3.14159 / 180
    timespan = float(entry10.get())

    entry10_var.set(timespan)

def LinearProgression(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 60.0
    ot_p = 150.0
    ox_p = 54.0
    a_y = 2.0
    ot_y = 150.0
    ox_y = 27.0
    v_med = 15.0
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


def LateralOndulation(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 20.0
    ot_p = 150.0
    ox_p = 54.0
    a_y = 30.0
    ot_y = 150.0
    ox_y = 54.0
    v_med = 15.0
    ph = 15.0
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

def Rolling(event):
    global a_p, ot_p, ox_p, a_y, ot_y, ox_y, v_med, ph, k

    a_p = 70.0
    ot_p = 150.0
    ox_p = 54.0
    a_y = 15.0
    ot_y = 150.0
    ox_y = 162.0
    v_med = 20.0
    ph = 0.0
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

    a_p = 65.0
    ot_p = 150.0
    ox_p = 54.0
    a_y = 0.0
    ot_y = 150.0
    ox_y = 27.0
    v_med = 15.0
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
linprog = Button(mod, text = "Best 1")
latond = Button(mod, text ="Most Efficient 1")
roll = Button(mod, text = "Best 2")
sidwin = Button(mod, text = "Most Efficient 2")
startpub = Button(bottomFrame, text = "Start Publishing")
stoppub = Button(bottomFrame, text = "Straight Position")
shut = Button(bottomFrame, text = "Shutdown")
refresh = Button(eigline, text = "Submit Values", command = getInput, pady = 10)
respawn = Button(las, text = "Respawn", command = Respawn, pady = 10)

initi.bind("<Button-1>", init)
linprog.bind("<Button-1>", LinearProgression)
latond.bind("<Button-1>", LateralOndulation)
roll.bind("<Button-1>", Rolling)
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
