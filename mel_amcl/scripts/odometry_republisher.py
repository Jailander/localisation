#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:38:47 2019

@author: michael
"""
# Alter covariance of an odomtry message 

from nav_msgs.msg import Odometry
import rospy

class OdomRepublisher:
    def __init__(self):
        rospy.Subscriber("odometry/base_raw", Odometry, self.odomCallback, queue_size = 10)
        self.odom_pub = rospy.Publisher('odometry/base_raw/new_covariances', Odometry, queue_size=10)
    
        self.covariance = (0.0025, 0, 0, 0, 0, 0,
                         0, 0.0025, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0.025)

    def odomCallback(self, data):
        print data.twist.covariance[0]
        #data.twist.covariance[0] = 0.01
        #data.twist.covariance[7] = 0.01
        #data.twist.covariance[35] = 0.06
        data.twist.covariance = self.covariance
        self.odom_pub.publish(data)

if __name__ == '__main__':
   # main()
    rospy.init_node('odometry_republisher', anonymous=True)
    OdomRepublisher()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down odometry republisher"
    
