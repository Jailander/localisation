# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 09:57:15 2019

@author: michael
"""

import rospy
from sensor_msgs.msg import Imu
import numpy as np
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



#plt.ion()

x = []
y = []
x2= []
y2= []
x3 = []
y3 = []
x4= []
y4= []



fig, ax = plt.subplots()
plt.rcParams.update({'font.size': 22})
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
#fig = plt.figure()
#ax = fig.add_subplot(111)

ln, = plt.plot([], [], 'g-', label='Wheel Odometry (WO)', linewidth=3)
ln2, = plt.plot([], [], 'm-', label='IMU & WO EKF', linewidth=3)
ln3, = plt.plot([], [], 'k-', label='Laser Odometry (LO)', linewidth=3)
ln4, = plt.plot([], [], 'b-', label='IMU & WO & LO EKF', linewidth=3)



#line1, = ax.plot(y, 'r')

def initf():
    ax.set_xlim([-10,40])
    ax.set_ylim([-25, 10])
    return ln,

    
def update(frame):
    ln.set_data(x, y)
    ln2.set_data(x2, y2)
    ln3.set_data(x3, y3)
    ln4.set_data(x4, y4)
    legend = plt.legend(loc = 'lower right')
    return ln, ln2, ln3, ln4, legend
  

def odomCallback(data):
    x.append(data.pose.pose.position.x)
    y.append(data.pose.pose.position.y)

def odomIMUCallback(data):
    x2.append(data.pose.pose.position.x)
    y2.append(data.pose.pose.position.y)
    
 
def laserCallback(data):
    x3.append(data.pose.pose.position.x)
    y3.append(data.pose.pose.position.y)
    
def odomIMULaserCallback(data):
    x4.append(data.pose.pose.position.x)
    y4.append(data.pose.pose.position.y)
   
   
   
#def main():

    
 #   plotOdomData()

if __name__ == '__main__':
   # main()
    rospy.init_node('odometry_analyzer', anonymous=True)
    rospy.Subscriber("odometry/base_raw", Odometry, odomCallback, queue_size = 10)
    rospy.Subscriber("odometry/odom_imu", Odometry, odomIMUCallback, queue_size = 10)
    rospy.Subscriber("odometry/odom_imu_laser", Odometry, odomIMULaserCallback, queue_size = 10)
    rospy.Subscriber("odometry/laser_scan_match", PoseWithCovarianceStamped, laserCallback, queue_size = 10)

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128), init_func=initf, blit=False)
    #plt.show()    
    plt.show(block=True)    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down odom plotter module"
    