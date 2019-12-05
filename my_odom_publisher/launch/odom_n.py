#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Header
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

rospy.init_node('odom_pub')

odom_pub=rospy.Publisher ('/my_odom', Point, queue_size = 20)

num = rospy.get_param('~number')
lengh = rospy.get_param('~lengh')
radius = rospy.get_param('~radius')

rospy.wait_for_service ('/gazebo/get_link_state')
get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

pos=Point()

links = {}
for index in range(num):
    links[index] = ["link{} = GetLinkStateRequest()".format(index), "link{}.link_name='snake_body_{}'".format(index, index)]
    exec(links[index][0])
    exec(links[index][1])
exec("link{} = GetLinkStateRequest()".format(num))
exec("link{}.link_name='startpt'".format(num))


r = rospy.Rate(100)

while not rospy.is_shutdown():
    x = [None] * (num+1)
    y = [None] * (num+1)
    z = [None] * (num+1)
    for index in range(num+1):
        exec("res{} = get_link_srv(link{})".format(index, index))
        exec("x[{}] = res{}.link_state.pose.position.x".format(index, index))
        exec("y[{}] = res{}.link_state.pose.position.y".format(index, index))
        exec("z[{}] = res{}.link_state.pose.position.z".format(index, index))
        pos.x += x[index]/(num+1)
        pos.y += y[index]/(num+1)
        pos.z += z[index]/(num+1)


    pos.x = pos.x - lengh * num / 2 - 0.002
    pos.z = pos.z - radius
    odom_pub.publish(pos)

    pos.x = 0
    pos.y = 0
    pos.z = 0

    pd = True

    while pd:
        try:
            r.sleep()
            pd = False
        except:
            pass


print("ODOM CLOSED")
