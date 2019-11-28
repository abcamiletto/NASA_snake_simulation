#! /usr/bin/env python
from sensor_msgs.msg import JointState
import rospy
rospy.init_node('writer_csv')
v = [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
tor =  [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
def Callback3(data):
    global v, tor
    v = data.velocity
    tor = data.effort



while True:
    rospy.Subscriber('/snake/joint_states', JointState, Callback3)
    print(str(v[0]))
