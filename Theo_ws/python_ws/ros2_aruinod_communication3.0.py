import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import subprocess

brate = 9600
#port_name = '/dev/ttyUSB0'
port_name = '/dev/ttyUSB1'
#port_name = '/dev/ttyUSB0'

#/bin/python3 /home/theo/23_HF110/Theo_ws/python_ws/ros2_aruinod_communication3.0.py

terminal_command = """ros2 topic pub /goal_pose geometry_msgs/msg/PoseStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 18.55, y: 40.17, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0575, w: 0.998}}}" """

class MinimalSubscriber(Node):
    def __init__(self, py_serial):
        super().__init__('minimal_subscriber')
        self.py_serial = py_serial
        self.subscription = self.create_subscription(
            String,
            '/detected_object',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Sending Arduino: "%s"' % msg.data)
        command = msg.data
        self.py_serial.write(command.encode())
        self.py_serial.reset_output_buffer()
        
        if self.py_serial.readable():
            response = self.py_serial.readline()
            print("Arduino Response:", response)
            if b"return" in response:
                self.execute_terminal_command()
        #if self.py_serial.in_waiting > 0:  # Check if data is available
        #    response = self.py_serial.readline().decode().strip()
         #   self.get_logger().info('Arduino Response: "%s"' % response)
        #    if "return" in response:
                
        self.py_serial.reset_input_buffer()  # Clear input buffer if necessary


    def execute_terminal_command(self):
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


def main(args=None):
    rclpy.init(args=args)
    py_serial = serial.Serial(port=port_name, baudrate=brate)  # Adjust the baud rate as needed
    minimal_subscriber = MinimalSubscriber(py_serial)

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C if needed
    finally:
        # Destroy the node explicitly
        minimal_subscriber.destroy_node()
        py_serial.close()  # Close the serial port
        rclpy.shutdown()

if __name__ == '__main__':
    main()
