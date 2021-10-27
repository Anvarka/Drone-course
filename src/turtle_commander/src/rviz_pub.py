#! /usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import MapMetaData
from geometry_msgs.msg import Pose
import sensor_msgs.msg

pub = rospy.Publisher('/my_scan', LaserScan, queue_size = 10)
# pub2 = rospy.Publisher('/my_map', OccupancyGrid, queue_size = 10)
msg_for_rviz = LaserScan()

def callback(msg):

    msg_for_rviz.header.stamp = msg.header.stamp
    msg_for_rviz.header.frame_id = 'base_link'
    msg_for_rviz.angle_min = msg.angle_min
    msg_for_rviz.angle_max = msg.angle_max
    msg_for_rviz.angle_increment = msg.angle_increment
    msg_for_rviz.time_increment = msg.time_increment
    msg_for_rviz.range_min = msg.range_min
    msg_for_rviz.range_max = msg.range_max
    msg_for_rviz.ranges = filter2(msg.ranges)
    msg_for_rviz.intensities = msg.intensities
    
    pub.publish(msg_for_rviz)
    

def listener():
    rospy.init_node('my_scan', anonymous=True)
    # rospy.init_node('my_map', anonymous=True)
    
    sub = rospy.Subscriber('/base_scan', LaserScan, callback)
    rospy.spin()
    

def filter2(arr):
    arr = np.array(arr, dtype=np.float64)
    res_ids = []
    i = 0
    while i < len(arr) - 1:
        check_arr_ids = [i]
        
        while (i + 1 < len(arr) - 1) and (arr[i + 1] -  arr[check_arr_ids[-1]] < 0.10):
            check_arr_ids.append(i + 1)
            i += 1

        if len(check_arr_ids) > 25:
            res_ids.extend(check_arr_ids) 

        i += 1

    return tuple(arr[res_ids])


listener()


