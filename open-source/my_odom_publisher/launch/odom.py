#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Header
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

rospy.init_node('odom_pub')

odom_pub=rospy.Publisher ('/my_odom', Point, queue_size = 20)

rospy.wait_for_service ('/gazebo/get_link_state')
get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

pos=Point()

link1 = GetLinkStateRequest()
link1.link_name='snake_body_1'
link2 = GetLinkStateRequest()
link2.link_name='snake_body_2'
link3 = GetLinkStateRequest()
link3.link_name='snake_body_3'
link4 = GetLinkStateRequest()
link4.link_name='snake_body_4'
link5 = GetLinkStateRequest()
link5.link_name='snake_body_5'
link6 = GetLinkStateRequest()
link6.link_name='snake_body_6'
link7 = GetLinkStateRequest()
link7.link_name='snake_body_7'
link8 = GetLinkStateRequest()
link8.link_name='startpt'


r = rospy.Rate(100)

while not rospy.is_shutdown():
    res1 = get_link_srv(link1)
    res2 = get_link_srv(link2)
    res3 = get_link_srv(link3)
    res4 = get_link_srv(link4)
    res5 = get_link_srv(link5)
    res6 = get_link_srv(link6)
    res7 = get_link_srv(link7)
    res8 = get_link_srv(link8)

    x1 = res1.link_state.pose.position.x
    y1 = res1.link_state.pose.position.y
    z1 = res1.link_state.pose.position.z
    x2 = res2.link_state.pose.position.x
    y2 = res2.link_state.pose.position.y
    z2 = res1.link_state.pose.position.z
    x3 = res3.link_state.pose.position.x
    y3 = res3.link_state.pose.position.y
    z3 = res1.link_state.pose.position.z
    x4 = res4.link_state.pose.position.x
    y4 = res4.link_state.pose.position.y
    z4 = res1.link_state.pose.position.z
    x5 = res5.link_state.pose.position.x
    y5 = res5.link_state.pose.position.y
    z5 = res1.link_state.pose.position.z
    x6 = res6.link_state.pose.position.x
    y6 = res6.link_state.pose.position.y
    z6 = res1.link_state.pose.position.z
    x7 = res7.link_state.pose.position.x
    y7 = res7.link_state.pose.position.y
    z7 = res1.link_state.pose.position.z
    x8 = res8.link_state.pose.position.x
    y8 = res8.link_state.pose.position.y
    z8 = res1.link_state.pose.position.z


    pos.x = (x1+x2+x3+x4+x5+x6+x7+x8)/8
    pos.y = (y1+y2+y3+y4+y5+y6+y7+y8)/8
    pos.z = (z1+z2+z3+z4+z5+z6+z7+z8)/8

    odom_pub.publish(pos)

    pd = True

    while pd:
        try:
            r.sleep()
            pd = False
        except:
            pass


print("ODOM CLOSED")
