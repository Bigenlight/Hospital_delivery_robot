#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from rclpy.qos import QoSProfile
import odrive
from odrive.enums import *
import math
import numpy as np
import serial
import os

class vel_send(Node):
    odrv0 = odrive.find_any()
    def __init__(self):
        super().__init__("vel_send")
        #self.send_serial("")
        self.get_logger().info("motor has started")
        self.position_publisher=self.create_publisher(Float32MultiArray, "/position",10)
        self.timer_=self.create_timer(0.1,self.pub_velocity)

    def pub_velocity(self):
        msg = Float32MultiArray()
        wheel_r=self.getEncoderData("r axis1.encoder.vel_estimate\n")* -0.05 * 0.03 * 0.1
        wheel_l=self.getEncoderData("r axis0.encoder.vel_estimate\n")* 0.05 * 0.03 * 0.1
        msg.data =[wheel_r/0.1,wheel_l/0.1]
        self.position_publisher.publish(msg)
        


def main(args=None):
    rclpy.init(args=args)
    node = vel_send()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    
    main()
