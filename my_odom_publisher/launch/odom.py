#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Header
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

rospy.init_node('odom_pub')

odom_pub=rospy.Publisher ('/my_odom', Pose2D)

rospy.wait_for_service ('/gazebo/get_link_state')
get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

pos=Pose2D()

link = GetLinkStateRequest()
link.link_name='snake_body_4'

r = rospy.Rate(0.5)

	

while not rospy.is_shutdown():
    result = get_link_srv(link)

    pos.x = result.link_state.pose.position.x
    pos.y = result.link_state.pose.position.y

    odom_pub.publish(pos)

    r.sleep()


#    txt_file=open("~/Desktop/simsnake/demofile3.txt", "a+")
#    txt_file.write("x:" + str(pos.x) + "\n") 
#    txt_file.write("y:" + str(pos.y) + "\n")
#    txt_file.write("\n")
#    txt_file.close()
