#!/usr/bin/env python3

import smbus
import rospy
from math import pi
from sensor_msgs.msg import Imu
from imu_registers import *

ADDR = None
bus = None
IMU_FRAME = None

# read_word and read_word_2c from 
# http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html
def read_word(adr):
    high = bus.read_byte_data(ADDR, adr)
    low = bus.read_byte_data(ADDR, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def publish_imu(timer_event):

    imu_msg = Imu()
    imu_msg.header.frame_id = IMU_FRAME

    # Read the acceleration vals
    accel_x = read_word_2c(ACCEL_XOUT_H) / 16384.0
    accel_y = read_word_2c(ACCEL_YOUT_H) / 16384.0
    accel_z = read_word_2c(ACCEL_ZOUT_H) / 16384.0

    # Read the gyro vals
    # Turn degree to radius
    gyro_x = (read_word_2c(GYRO_XOUT_H)) * (pi / 180.) / 131.0
    gyro_y = (read_word_2c(GYRO_YOUT_H)) * (pi / 180.) / 131.0
    gyro_z = (read_word_2c(GYRO_ZOUT_H)) * (pi / 180.) / 131.0

    imu_msg.linear_acceleration.x = accel_x
    imu_msg.linear_acceleration.y = accel_y
    imu_msg.linear_acceleration.z = accel_z

    imu_msg.angular_velocity.x = gyro_x
    imu_msg.angular_velocity.y = gyro_y
    imu_msg.angular_velocity.z = gyro_z

    imu_msg.header.stamp = rospy.Time.now()

    imu_pub.publish(imu_msg)


imu_pub = None

if __name__ == '__main__':
    rospy.init_node('imu_readRaw')

    bus = smbus.SMBus(rospy.get_param('~bus', 1))
    ADDR = rospy.get_param('~device_address', 0x68)

    # ADDR get address
    # Address is by : hexadecimal
    if type(ADDR) == str:
        ADDR = int(ADDR, 16)

    # Get imu's frame
    # Default is imu_link
    IMU_FRAME = rospy.get_param('~imu_frame', 'imu_link')

    bus.write_byte_data(ADDR, PWR_MGMT_1, 0)

    # IMU publisher and Timer
    # Now callback function frequency : 50 hz
    topic = rospy.get_param('~driver_topic', 'raw')
    imu_pub = rospy.Publisher('/' + topic, Imu, queue_size=10)
    imu_timer = rospy.Timer(rospy.Duration(0.02), publish_imu)
    
    rospy.spin()
