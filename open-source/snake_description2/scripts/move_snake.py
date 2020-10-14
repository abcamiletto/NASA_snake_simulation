#!/usr/bin/env python
import sys
import rospy
import time
from math import pi, sin, cos, acos
import random
from std_msgs.msg import Float64



class SnakeJointMover(object):

    def __init__(self, number_segments_snake):
        rospy.init_node('Snake_jointmover', anonymous=True)
        rospy.loginfo("Snake Initialising...")

        self._number_segments_snake = number_segments_snake
        
        self.init_snake_pub_array()
        self._rate = rospy.Rate(5)

    def init_snake_pub_array(self):
        
        self._snake_pub_array = []
        
        # /tentacle/t2_2_joint_position_controller/command
        namespace = "/snake/"
        ending = "/command"

        base_name = "snake_body"

        for x in range(0, self._number_segments_snake):

            aux_controller_topic = namespace+base_name+"_"+str(x)+"_aux_joint_position_controller"+ending
            main_controller_topic = namespace+base_name+"_"+str(x)+"_joint_position_controller"+ending
            # Add Connector Joints
            aux_connector_controller_topic = namespace+base_name+"_"+str(x)+"_aux_connector_joint_position_controller"+ending
            main_connector_controller_topic = namespace+base_name+"_"+str(x)+"_connector_joint_position_controller"+ending

            pub_aux = rospy.Publisher(aux_controller_topic,
                                    Float64,
                                    queue_size=1)
            pub_main = rospy.Publisher(main_controller_topic,
                                        Float64,
                                        queue_size=1)
            # Add Connector Joints
            pub_aux_connector = rospy.Publisher(aux_connector_controller_topic,
                                    Float64,
                                    queue_size=1)
            pub_main_connector = rospy.Publisher(main_connector_controller_topic,
                                        Float64,
                                        queue_size=1)

            self._snake_pub_array.append(pub_aux)
            self._snake_pub_array.append(pub_main)
            self._snake_pub_array.append(pub_aux_connector)
            self._snake_pub_array.append(pub_main_connector)

    def move_snake_joints(self):
        
        alfa = 0.0
        delta = 0.05
        while not rospy.is_shutdown():
            
            position_command = Float64()
            position_command.data = sin(alfa)
            
            for joint_pub in self._snake_pub_array:
                joint_pub.publish(position_command)
            
            self._rate.sleep()
            alfa += delta
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python move_snake.py number_of_segments")
    else:
        des_number_segments_snake = int(sys.argv[1])
        snake_jointmover_object = SnakeJointMover(des_number_segments_snake)
        snake_jointmover_object.move_snake_joints()
