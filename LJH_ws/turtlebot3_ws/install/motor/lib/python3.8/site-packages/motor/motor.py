import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray, Int32MultiArray, String
from rclpy.qos import QoSProfile
import odrive
from odrive.enums import *
import math
import serial
import os
import numpy as np

class Motor(Node):
    SERIAL_PORT = '/dev/ttyACM1'
    odrv0 = odrive.find_any()
    flag=0.
    def __init__(self):
        super().__init__("motor")
        self.flag = 0
        self.odrv0 = None
        self.count = 0.0
        self.wheelDiameter = 0.0702 # m unit
        self.wheelSeperation = 0.465  # m unit

        if not os.path.exists(self.SERIAL_PORT):
            self.get_logger().error("Serial Port not found")
            rclpy.shutdown()

        self.ser = serial.Serial(self.SERIAL_PORT, 115200)
        self.flag_sub = self.create_subscription(Int32MultiArray, "/flag", self.check_flag, 10)
        self.twist_subscriber = self.create_subscription(Twist, "/cmd_vel", self.send_cmd_vel, 10)
        self.get_logger().info("motor has started")
        self.position_publisher = self.create_publisher(Float32MultiArray, "/position", 10)
        self.timer_ = self.create_timer(0.02, self.pub_velocity)


    def check_flag(self, msg):
        self.flag = msg.data[0]
        if self.flag == 1:
            self.get_logger().info("Static object detected")
   
    def send_cmd_vel(self, msg):
        if self.flag == 2:
            self.get_logger().info("Moving object detected")
            self.odrv0.axis1.controller.input_vel = 0
            self.odrv0.axis0.controller.input_vel = 0
        else:
            self.get_logger().info("Twist: Linear: %f Angular velocity: %f" % (msg.linear.x, msg.angular.z))
            self.odrv0.axis1.controller.input_vel = (msg.linear.x + msg.angular.z * 0.54/2) *-0.5
            self.odrv0.axis0.controller.input_vel = (msg.linear.x - msg.angular.z * 0.54/2) *0.5

    def getEncoderData(self, command):
        self.ser.write(command.encode())
        data = self.ser.readline().decode().strip()
        return float(data) / (math.pi * self.wheelDiameter)

    def pub_velocity(self):
        if not self.odrv0:
            try:
                self.odrv0 = odrive.find_any()
            except odrive.utils.TimeoutError:
                self.get_logger().warning("ODrive not found. Retrying...")
                return

        msg = Float32MultiArray()
        self.rightWheelPos = self.getEncoderData("r axis0.encoder.pos_estimate\n") * 0.5
        self.leftWheelPos = self.getEncoderData("r axis1.encoder.pos_estimate\n") * -0.5
        self.rightWheelVel = self.getEncoderData("r axis0.encoder.vel_estimate\n") * 0.05 * 0.03 
        self.leftWheelVel = self.getEncoderData("r axis1.encoder.vel_estimate\n") * -0.05 * 0.03 

        wheel_r_pos = self.rightWheelPos
        wheel_l_pos = self.leftWheelPos
        wheel_r_vel = self.rightWheelVel
        wheel_l_vel = self.leftWheelVel

    #    if self.mode == "green":  # Add this condition to check traffic sign
     #     wheel_l_vel += 5  # Add force to the left motor
      #  if self.mode == "red":  # Add this condition to check traffic sign
       #   wheel_r_vel += 5  # Add force to the left motor  
       
        self.count += 1.0
        msg.data = [wheel_l_pos,wheel_r_pos,wheel_l_vel,wheel_r_vel,self.count]
        self.position_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Motor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
