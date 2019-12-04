#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import Header
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

rospy.init_node('odom_pub')

odom_pub=rospy.Publisher ('/my_odom', Point, queue_size = 20)

num = rospy.get_param('number')

rospy.wait_for_service ('/gazebo/get_link_state')
get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

pos=Point()

links = {}
for index in range(num)
    links[index] = ["link{} = GetLinkStateRequest()".format(index), link{}.link_name='snake_body_{}'.format(index, index)]
    exec(links[index][0])
    exec(links[index][1])


r = rospy.Rate(100)

while not rospy.is_shutdown():
    x = [] * num
    y = [] * num
    z = [] * num
    for index in range(num)
        exec("res{} = gel_link_srv(link{})".format(index, index))
        exec("x[{}] = res{}.link_state.pose.position.x".format(index, index))
        exec("y[{}] = res{}.link_state.pose.position.y".format(index, index))
        exec("z[{}] = res{}.link_state.pose.position.z".format(index, index))
        pos.x += x[index]/8
        pos.y += y[index]/8
        pos.z += z[index]/8

    odom_pub.publish(pos)

    pd = True

    while pd:
        try:
            r.sleep()
            pd = False
        except:
            pass


print("ODOM CLOSED")
