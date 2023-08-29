import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32

import serial
import time


import struct

# serial 설치 필요

# 명령
# cd ros2_workspace
# source install/setup.bash
# ros2 run py_arduino_pub Sending_py_order

# 아두이노와 연결
# /bin/python3 /home/theo/23_HF110/Theo_ws/python_ws/ros2_arduino_communication.py


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'topic',
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Sending Arduino: %d' % msg.data)
        
        commend = msg.data
        
        
        #py_serial.write(commend.encode())
        #py_serial.write(commend)
        
        
        data = struct.pack('>i', commend)
        py_serial.write(data)
        
        # #추가
        py_serial.reset_output_buffer()
        
        
        if py_serial.readable():
            # response = py_serial.readline()
            # print(response[:len(response)-1].decode())
            
            #response = py_serial.read_until(" ")
            
            response = py_serial.read()
            print("Arduino Response:", response)  # Print raw bytes
            # Process the response as needed, without attempting UTF-8 decoding
            # For example, you can convert the bytes to a hex representation
            #hex_response = " ".join([format(byte, '02x') for byte in response])
            #print("Hex Response:", hex_response)

        
        # # #추가
        py_serial.reset_input_buffer()
        
        time.sleep(0.01)
    


py_serial = serial.Serial(
    
    # Window
    #port='/dev/ttyUSB0',
    #port='/dev/ttyACM0',
    port='/dev/ttyACM1',
    
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
        