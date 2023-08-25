import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import serial
import time

# source install/setup.bash
# ros2 run py_pubsub listener


#####################################################################################
class MinimalPublisher(Node):
    
    
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.result = ""

    def timer_callback(self):
        commend = input('아두이노에게 내릴 명령:')
    
        py_serial.write(commend.encode())
    
        commend = input('아두이노에게 내릴 명령:')
        if py_serial.readable():
            # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
            response = py_serial.readline()
            
            # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            self.result = response[:len(response)-1].decode()
    
        
        
        
        msg = String()
        msg.data = "responce: %s" %self.result
        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        #self.i += 1
        


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
###################################################################################

py_serial = serial.Serial(
    
    # Window
    port='/dev/ttyACM1',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)

while True:
      
    # commend = input('아두이노에게 내릴 명령:')
    
    # py_serial.write(commend.encode())
    
    # time.sleep(0.1)
    
    rclpy.init(args=None)

    minimal_publisher = MinimalPublisher()
    
    # if py_serial.readable():
        
    #     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    #     # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    #     response = py_serial.readline()
        
    #     # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    #     minimal_publisher.result = response[:len(response)-1].decode()
    
    
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
        