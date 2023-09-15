import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import serial
import time

# serial 설치 필요
# 아래 py_serial에서 포트 설정 필요 (아두이노 들아가면 쉽게 볼 수 있음, 그거 쓰면 됨)

# 명령
# cd 23_HF110/Theo_ws/ros2_workspace/
# source install/setup.bash
# ros2 run py_arduino_pub Sending_py_order

# 아두이노와 연결 (home 뒤 theo는 바꿔야함)
# /bin/python3 /home/theo/23_HF110/Theo_ws/python_ws/ros2_arduino_communication.py


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'person',
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Sending Arduino: "%s"' % msg.data)
        
        commend = msg.data
        
        py_serial.write(commend.encode())
        
        #추가
        py_serial.reset_output_buffer()
        
        
        if py_serial.readable():
            # response = py_serial.readline()
            # print(response[:len(response)-1].decode())
            
            response = py_serial.readline()
            print("Arduino Response:", response)  # Print raw bytes
            # Process the response as needed, without attempting UTF-8 decoding
            # For example, you can convert the bytes to a hex representation
            #hex_response = " ".join([format(byte, '02x') for byte in response])
            #print("Hex Response:", hex_response)
            
        time.sleep(0.001)
    


py_serial = serial.Serial(
    
    #port='/dev/ttyUSB0',
    #port='/dev/ttyUSB1',
    port='/dev/ttyACM0',
    #port='/dev/ttyACM1',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)

while True:
    
    #time.sleep(0.1)
    
    rclpy.init(args=None)


    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
        