#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
import time

rospy.init_node("turtle_square")

pub_left = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 1)
pub_right = rospy.Publisher("/leo/cmd_vel", Twist, queue_size = 1)
msg = Twist()

r = rospy.Rate(0.5) # Hz

while not (rospy.is_shutdown()):
    msg.linear.x = 1.0
    msg.angular.z = 0.0
    
    pub_left.publish(msg)
    pub_right.publish(msg)
    r.sleep()
    
    msg.linear.x = 0.0
    msg.angular.z = 1.57
    
    pub_left.publish(msg)
    msg.angular.z = -1.57
    pub_right.publish(msg)
    r.sleep()
