import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import serial
import time

import subprocess

#pos0
terminal_command = """ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 1.14, y: 39.51, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: -0.999, w: 0.00}}}" """

# serial 설치 필요
# 아래 py_serial에서 포트 설정 필요 (아두이노 들아가면 쉽게 볼 수 있음, 그거 쓰면 됨)

# 예제 명령 보내기
# cd 23_HF110/Theo_ws/ros2_workspace/
# source install/setup.bash
# ros2 run py_arduino_pub Sending_py_order


# 아두이노와 연결 (home 뒤 theo는 바꿔야함)
# 명령 보내는 다른 터미널에서 이거 실행 (실행할 명령에 필요한 과정은 거쳐야됨 scource install 등등)
# /bin/python3 /home/theo/23_HF110/Theo_ws/python_ws/ros2_aruinod_communication2.0.py



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            '/detected_object',
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning


    def listener_callback(self, msg):
        self.get_logger().info('Sending Arduino: "%s"' % msg.data)
        command = msg.data
        py_serial.write(command.encode())
        py_serial.reset_output_buffer()

        #받기
        if py_serial.readable():
            response = py_serial.readline()
            print("Arduino Response:", response)
            if b"return" in response:
                print("Sending to return")
                print("command:", terminal_command)
                # 실행할 명령어

                # 명령어 실행 및 결과 출력
                result = subprocess.run(terminal_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # 명령어 실행 결과 출력
                if result.returncode == 0:
                    print("명령어 실행 성공:")
                    print(result.stdout)
                else:
                    print("명령어 실행 실패:")
                    print(result.stderr)

    # def listener_callback(self, msg):
    #     self.get_logger().info('Sending Arduino: "%s"' % msg.data)
        
    #     commend = msg.data
        
    #     py_serial.write(commend.encode())
        
    #     #추가
    #     py_serial.reset_output_buffer()
        
        
    #     if py_serial.readable():
    #         # response = py_serial.readline()
    #         # print(response[:len(response)-1].decode())
            
    #         response = py_serial.readline()
    #         print("Arduino Response:", response)  # Print raw bytes
            
    #         returning = response.decode('utf-8')
    #         # Process the response as needed, without attempting UTF-8 decoding
    #         # For example, you can convert the bytes to a hex representation
    #         #hex_response = " ".join([format(byte, '02x') for byte in response])
    #         #print("Hex Response:", hex_response)
    #         if b"return" in response:
    #             print("Sendind to return")
    #             print("Sendind to return")
    #             # while(True):
                    
    #             #     command = "glpush"

    #             #     # 명령어 실행 및 결과 출력
    #             #     result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    #             #     # 명령어 실행 결과 출력
    #             #     if result.returncode == 0:
    #             #         print("명령어 실행 성공:")
    #             #         print(result.stdout)
    #             #     else:
    #             #         print("명령어 실행 실패:")
    #             #         print(result.stderr)
                
                       #
        time.sleep(0.0005)
        
        #

    


py_serial = serial.Serial(
    
    #port='/dev/ttyUSB0',
    port='/dev/ttyUSB1',
    #port='/dev/ttyACM0',
    #port='/dev/ttyACM1',
    
    # 보드 레이트 (통신 속도)
    #baudrate=9600,
    baudrate=300,
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
        
