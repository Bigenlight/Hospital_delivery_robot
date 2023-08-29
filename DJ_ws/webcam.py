import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_publisher')                                # 부모 클래스(Node)의 생성자를 호출하여 ROS 노드를 초기화. 노드 이름은 "webcam_publisher"로 설정.
        self.publisher_ = self.create_publisher(Image, '/image_raw', 10)    # 이미지 데이터를 게시하는 ROS 퍼블리셔를 생성. /image_raw 토픽으로 Image 메시지를 게시.
        self.bridge = CvBridge()                                            # CvBridge 인스턴스를 생성하여 OpenCV 이미지와 ROS Image 메시지 간의 변환을 수행.

        self.timer = self.create_timer(0.1, self.publish_frame)             # 주기적으로 publish_frame 메서드를 호출하는 타이머를 생성. 0.1초마다 프레임을 게시.

        self.capture = cv2.VideoCapture(2)                                  # OpenCV를 사용하여 웹캠을 연결하고, 2번 웹캠을 사용하도록 설정.

    def publish_frame(self):
        ret, frame = self.capture.read()                                    # 웹캠으로부터 프레임을 읽어옴. ret은 성공 여부를 나타내는 불리언 값, frame은 읽어온 이미지 데이터.
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")     # OpenCV 이미지를 ROS Image 메시지로 변환. bgr8 인코딩을 사용하여 BGR 컬러 형식의 이미지를 표현.
            self.publisher_.publish(img_msg)                                # 변환된 이미지 메시지를 /image_raw 토픽으로 게시합니다.


def main(args=None):
    rclpy.init(args=args)                   # ROS 2 노드를 초기화.
    webcam_publisher = WebcamPublisher()    # WebcamPublisher 클래스의 인스턴스를 생성합니다.   
    rclpy.spin(webcam_publisher)            # 노드를 실행하고, 이벤트 루프를 시작하여 노드의 동작을 유지.

    webcam_publisher.destroy_node()         # 노드를 종료하기 전에 정리 작업을 수행.
    rclpy.shutdown()                        # ROS 2 노드를 종료.

if __name__ == '__main__':
    main()