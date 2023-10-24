#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float32MultiArray

class detection(Node):

    pre_X=0.
    pre_y=0.
    pre_obstacle_distance=9999
    vec_x=0.
    vec_y=0.
    def __init__(self):
        super().__init__("detection")
        self.scan_ranges = []
        self.Scan_subscriber = self.create_subscription(LaserScan,'scan',self.scan_callback,qos_profile=qos_profile_sensor_data)
        self.get_logger().info("Detection has started")
        ##self.position_publisher=self.create_publisher(Float32MultiArray, "/position",10)
        ##self.timer_=self.create_timer(0.02,self.pub_velocity)
        ##self.count=0.0


    def scan_callback(self,msg):
        self.scan_ranges = msg.ranges
        dect=max(self.scan_ranges)
        self.get_logger().info("Input")
        print(msg.angle_increment07)
        ##print(self.scan_ranges)
"""
    def pub_velocity(self):
        msg = Float32MultiArray()
        wheel_r_pos=self.odrv0.axis0.encoder.pos_estimate*2*math.pi/17*-1
        wheel_l_pos=self.odrv0.axis1.encoder.pos_estimate*2*math.pi/17*-1
        wheel_r_vel=self.odrv0.axis0.encoder.vel_estimate*0.1
        wheel_l_vel=self.odrv0.axis1.encoder.vel_estimate*0.1
        count=self.count
        msg.data =[wheel_r_pos,wheel_l_pos,wheel_r_vel,wheel_l_vel,count]
        self.position_publisher.publish(msg)
        self.count += 1.0
   """     
        


def main(args=None):
    rclpy.init(args=args)
    node = detection()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    
    main()