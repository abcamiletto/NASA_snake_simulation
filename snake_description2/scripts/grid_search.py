#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('commanding', String, queue_size=10)
    rospy.init_node('grid_search', anonymous=True)

    while not rospy.is_shutdown():
	for x in range(100)
		
        	#1- inizializzare nodo rosbag (lanciare comando "rosbag record /tf_static -o $(find snake_description2)/rosbag_rec/gridsearch.bag")
		#2- tic
		#3- faccio partire side winding con parametri opportuni (qui torna utile la variabile x)
		#4- toc while (toc<5 sec) toc
		#5- CTRL C
		#6- killare precedenti comandi rosbag (assicurarsi non ci sia respawn)

		hello_str = "hello world %s" % rospy.get_time()
        	rospy.loginfo(hello_str)
        	pub.publish(hello_str)
        	rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#The ROS Node Publisher template
 
#!usr/bin/env python
 
#remove or add the library/libraries for ROS
import rospy, time, math, random
 
#remove or add the message type
from std_msgs.msg import Int32, Float32, String
from basics.msg import TimerAction, TimerGoal, TimeResult
from time import sleep
 
#you can define functions to provide the required functionality
def body(arg):
    def_body_here
    return the_value
 
if __name__=='__main__':
    #add here the node name. In ROS, nodes are unique named.
    rospy.init_node('THE_NAME_OF_THE_NODE')
 
    #publish messages to a topic using rospy.Publisher class
    name_pub=rospy.Publisher('THE_NAME_OF_THE_TOPIC', THE_TYPE_OF_THE_MESSAGE, queue_size=1)
 
    #you can define functions to provide the required functionality
    if var1==var2:
        make_something()
        else:
            make_something()
 
    #set a publishing rate. Below is a publishing rate of 10 times/second
    rate=rospy.Rate(10)
 
    while not rospy.is_shutdown():
        #some calculation here
        if a1==a2:
            pub.publish(message1)
            else:
                pub.publish(message2)
rate.sleep()
