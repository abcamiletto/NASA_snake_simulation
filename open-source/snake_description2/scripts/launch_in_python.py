import rospy
import roslaunch
import time

#rospy.init_node('en_Mapping', anonymous=True)
#rospy.on_shutdown(self.shutdown)

uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/user/simulation_ws/src/parsel/snake_description/launch/init_snake_n.launch"])

launch.start()
time.sleep(10)
launch.shutdown()