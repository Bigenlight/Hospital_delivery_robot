import serial
import rclpy
import math
import time
from rclpy.node import Node
from rclpy.time import Time
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity='N',
    stopbits=1,
    bytesize=8,
)

# 시리얼포트 접속
ser.isOpen()

class OdomPublisher(Node):
    def __init__(self):
        super().__init__('odom_publisher')
        self.publisher = self.create_publisher(Odometry, 'odom_data', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.publish_callback)
        self.get_logger().info('Odom Publisher is created')

        # 이전 시각과 dt
        self.prevTime = 0
        self.dt = 0

        # 모터 파라미터
        self.wheelDiameter = 0.0702 # m unit
        self.wheelSeperation = 0.465  # m unit

        # 엔코더로 측정하는 값
        self.rightWheelPos = 0
        self.leftWheelPos = 0
        self.rightWheelVel = 0
        self.leftWheelVel = 0

        #Odom 값
        self.linear = 0
        self.angular = 0
        self.theta = 0
        self.x = 0
        self.y = 0

    def getEncoderData(self, command):
        axisUARTMessage = command
        ser.write(axisUARTMessage.encode())
        data = ser.readline()
        return float(data) / (math.pi * self.wheelDiameter) 

    def publish_callback(self):
        # callback 함수가 실행되는 데 걸린 시간 dt 구하기
        nowTime = time.time()
        self.dt = nowTime - self.prevTime
        self.prevTime = nowTime

        # # IMU 센서로부터 받은 데이터 값을 업데이트하는 코드 작성
        # # 시리얼 통신을 통해 데이터를 받아옴
        
        self.rightWheelPos = self.getEncoderData("r axis0.encoder.pos_estimate\n")
        self.leftWheelPos = self.getEncoderData("r axis1.encoder.pos_estimate\n")
        self.rightWheelVel = self.getEncoderData("r axis0.encoder.vel_estimate\n") * -0.05
        self.leftWheelVel = self.getEncoderData("r axis1.encoder.vel_estimate\n") * 0.05

        
        self.linear = (self.leftWheelVel + self.rightWheelVel) * 0.5
        self.angular = (self.rightWheelVel - self.leftWheelVel) / self.wheelSeperation

        self.theta += self.angular * self.dt   
        self.x += self.linear * math.cos(self.theta) * self.dt
        self.y += self.linear * math.sin(self.theta) * self.dt
        
        Odom_msg = Odometry()
        
        Odom_msg.header.frame_id = 'odom'
        Odom_msg.child_frame_id = 'base_link'
        
        Odom_msg.header.stamp = self.get_clock().now().to_msg()
        
        Odom_msg.header.stamp = self.get_clock().now().to_msg()
        Odom_msg.twist.twist.linear.x = self.linear * math.cos(self.theta)
        Odom_msg.twist.twist.linear.y = self.linear * math.sin(self.theta)
        Odom_msg.twist.twist.angular.z = self.angular
        
        Odom_msg.pose.pose.position.x = self.x
        Odom_msg.pose.pose.position.y = self.y
        Odom_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        Odom_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)
    
        self.publisher.publish(Odom_msg)


def main(args=None):
    rclpy.init(args=args)
    odom_publisher = OdomPublisher()
    rclpy.spin(odom_publisher)
    odom_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
