#!/usr/bin/python3

import rospy
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time

class Karusel:
    def __init__(self):
        rospy.Subscriber("/turtle1/pose", Pose, self.callback_turtle1)
        rospy.Subscriber("/leo/pose", Pose, self.callback_leo)
        self.pub_leo = rospy.Publisher("/leo/cmd_vel", Twist, queue_size=1)

        self.turtle1_x = 0
        self.turtle1_y = 0

        self.phi = 0
        self.msg_for_leo = Twist()

    def callback_turtle1(self, msg):
        self.turtle1_x = msg.x
        self.turtle1_y = msg.y
  
    def callback_leo(self, msg):
        leo_x = msg.x
        leo_y = msg.y
        leo_theta = msg.theta
        
        phi = self.get_angle(self.turtle1_x, self.turtle1_y, leo_x, leo_y)

        ang = phi - leo_theta
        self.smart_turn(ang)
        self.msg_for_leo.linear.x = math.dist([self.turtle1_x, self.turtle1_y], [leo_x, leo_y])

    def smart_turn(self, ang):
        if ang > math.pi:
            ang = -2 * math.pi + ang
        if ang < -math.pi:
            ang = 2 * math.pi + ang
        self.msg_for_leo.angular.z = ang


    def send_twist(self, get_dist=False):
        final_msg = Twist()
        if get_dist:
            final_msg.angular.z = 0.0
            final_msg.linear.x = self.msg_for_leo.linear.x
        else:
            final_msg.angular.z = self.msg_for_leo.angular.z
            final_msg.linear.x = 0.0

        self.pub_leo.publish(final_msg)

    def get_angle(self, x1, y1, x2, y2):
        return math.atan2((y1-y2), (x1-x2))


rospy.init_node("turtle_log_pose")
r = rospy.Rate(1) # Hz

karusel = Karusel()

while not rospy.is_shutdown():
    karusel.send_twist()
    r.sleep()
    karusel.send_twist(get_dist=True)
    r.sleep()
