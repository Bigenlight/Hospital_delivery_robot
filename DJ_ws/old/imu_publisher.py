import serial
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import Imu

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity='N',
    stopbits=1,
    bytesize=8,
)

# 시리얼포트 접속
ser.isOpen()

class ImuPublisher(Node):
    def __init__(self):
        super().__init__('imu_publisher')
        # ROS2 publisher 생성
        self.publisher = self.create_publisher(Imu, 'imu_data', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.publish_callback)
        self.get_logger().info('IMU Publisher is created')

    def publish_callback(self):
        # IMU 센서로부터 받은 데이터 값을 업데이트하는 코드 작성
        # 시리얼 통신을 통해 데이터를 받아옴
        data = ser.readline()
        data_str = data.decode().strip()  # 바이트 문자열을 문자열로 변환하고, 공백 및 개행 문자를 제거
        data_str = data_str[1:]

        # IMU 센서로부터 받은 데이터 값을 저장하기 위한 배열(순서대로 쿼터니언 방향, 각속도, 가속도)
        self.IMU_data = [0 for _ in range(10)]

        self.IMU_data = list(map(str, data_str.split(',')))

        # 업데이트된 데이터 값을 사용하여 Imu 메시지를 생성하고 publish
        IMU_msg = Imu()
        IMU_msg.header.frame_id = 'base_link'
        IMU_msg.header.stamp = self.get_clock().now().to_msg()
        IMU_msg.orientation.x = float(self.IMU_data[0])
        IMU_msg.orientation.y = float(self.IMU_data[1])
        IMU_msg.orientation.z = float(self.IMU_data[2])
        IMU_msg.orientation.w = float(self.IMU_data[3])
        IMU_msg.angular_velocity.x = float(self.IMU_data[4])
        IMU_msg.angular_velocity.y = float(self.IMU_data[5])
        IMU_msg.angular_velocity.z = float(self.IMU_data[6])
        IMU_msg.linear_acceleration.x = float(self.IMU_data[7])
        IMU_msg.linear_acceleration.y = float(self.IMU_data[8])
        IMU_msg.linear_acceleration.z = float(self.IMU_data[9])
        self.publisher.publish(IMU_msg)


def main(args=None):
    rclpy.init(args=args)
    imu_publisher = ImuPublisher()
    rclpy.spin(imu_publisher)
    imu_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
