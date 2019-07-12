#!/usr/bin/env python2
# -*- coding: utf-8 -*-


''' Convert quarternion values to euler for testing imu '''



import rospy
from sensor_msgs.msg import Imu
import numpy as np
from geometry_msgs.msg import Vector3Stamped
import tf
import math



def imu_callback(data):
    input_quat = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
    orientation_input_data = tf.transformations.euler_from_quaternion(input_quat, axes='sxyz')
    
    rpy_pub = rospy.Publisher('imu/rpy_deg', Vector3Stamped, queue_size=10)
    rpy_msg = Vector3Stamped()
    rpy_msg.vector.x = orientation_input_data[0]*180/math.pi
    rpy_msg.vector.y = orientation_input_data[1]*180/math.pi
    rpy_msg.vector.z = orientation_input_data[2]*180/math.pi
    print rpy_msg.vector.z # + 180 # OFFSET from output
    
    rpy_pub.publish(rpy_msg)

def main():
    rospy.init_node('imu test', anonymous=True)
    imu_subscriber = rospy.Subscriber('/imu/data', Imu, imu_callback, queue_size = 10)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down GPS to map pose conversion module"
        
if __name__ == '__main__':
    main()