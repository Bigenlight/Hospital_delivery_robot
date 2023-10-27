import socket
import pickle
import struct
import time
import cv2
import torch
import statistics
import numpy as np

from numpy import random
from cv_bridge import CvBridge
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, check_requirements, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray, String

server_ip = socket.gethostbyname('192.168.0.33') # 위에서 설정한 서버 ip
server_port1 = 3333 # 위에서 설정한 서버 포트번호
server_port2 = 4444 # 위에서 설정한 서버 포트번호

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect((server_ip, server_port1))

socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket2.connect((server_ip, server_port2))

WEIGHTS_PERSON = 'weights/person_0911_200.pt'
WEIGHTS_CARD = 'weights/card_0904_200.pt'
IMG_SIZE = 640
DEVICE = ''
AUGMENT = False
CONF_THRES = 0.70
IOU_THRES = 0.45
CLASSES = None
AGNOSTIC_NMS = False

QUEUE_SIZE = 13
CLASS_MAP = ['per ', 'push ']

# Initialize
device = select_device(DEVICE)
half = device.type != 'cpu'  # half precision only supported on CUDA
print('device:', device)

# Initialize model and weights
def load_model(weights_path):
    global model, stride, imgsz
    model = attempt_load(weights_path, map_location=device)
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(IMG_SIZE, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

def change_weights(new_weights_path):
    load_model(new_weights_path)


load_model(WEIGHTS_CARD)

# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

# Run inference
if device.type != 'cpu':
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

class YOLOv7(Node):
    def __init__(self):

        super().__init__('yolo')                                                                                                             

        self.detected_pub = self.create_publisher(Image, "/detected_image", 10)       
        self.object_pub = self.create_publisher(String, "/detected_object", 10)
        self.image_sub = self.create_subscription(Image, "/image_raw", self.image_cb, 10)
        self.flag_sub = self.create_subscription(Int32MultiArray, "/flag", self.check_flag, 10)
        self.publisher_ = self.create_publisher(Image, '/image_raw', 10)    # 이미지 데이터를 게시하는 ROS 퍼블리셔를 생성. /image_raw 토픽으로 Image 메시지를 게시.
        self.bridge = CvBridge()                                            # CvBridge 인스턴스를 생성하여 OpenCV 이미지와 ROS Image 메시지 간의 변환을 수행.

        self.capture = cv2.VideoCapture(0)                                  # OpenCV를 사용하여 웹캠을 연결하고, 2번 웹캠을 사용하도록 설정.

        self.queue_list = [-1 for _ in range(QUEUE_SIZE)]

        self.timer = self.create_timer(0.1, self.yolo_pub)

        self.currentWeights = WEIGHTS_CARD
        self.mode = 'card_mode'
    
    def image_cb(self, img):
        check_requirements(exclude=('pycocotools', 'thop'))
        with torch.no_grad():
            bridge = CvBridge()
            cap = bridge.imgmsg_to_cv2(img, desired_encoding="bgr8")

            result = self.detect(cap)
            image_message = bridge.cv2_to_imgmsg(result, encoding="bgr8")

            image_message.header.stamp = self.get_clock().now().to_msg()
            self.detected_pub.publish(image_message)

    def check_flag(self, flag):
        if flag == 1:
            self.queue_list = [-1 for _ in range(QUEUE_SIZE)]
            if self.currentWeights == WEIGHTS_CARD:
                change_weights(WEIGHTS_PERSON)
                self.currentWeights = WEIGHTS_PERSON
                self.mode = "person_mode"
            elif self.currentWeights == WEIGHTS_PERSON:
                change_weights(WEIGHTS_CARD)
                self.currentWeights = WEIGHTS_CARD
                self.mode = "card_mode"


    # Detect function
    def detect(self, frame):
        # Load image
        img0 = frame

        # Padded resize
        img = letterbox(img0, imgsz, stride=stride)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)


        # Inference
        t0 = time_synchronized()
        pred = model(img, augment=AUGMENT)[0]

        # Apply NMS
        pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, classes=CLASSES, agnostic=AGNOSTIC_NMS)

        # Process detections
        det = pred[0]
        numClasses = len(det)

        s = ''
        s += '%gx%g ' % img.shape[2:]  # print string

        if numClasses:
            # Rescale boxes from img_size to img0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                id = int(cls)
                label = f'{names[id]} {conf:.2f}'
                plot_one_box(xyxy, img0, label=label, color=colors[id], line_thickness=3)
                xmin, ymin, xmax, ymax = [int(tensor.item()) for tensor in xyxy]

                ymean = (ymin + ymax) / 2

                if ymean < IMG_SIZE / 2:
                    self.queue_list.append(id)
                else:
                    self.queue_list.append(-1)

        else:
            self.queue_list.append(-1)

        # return results
        return img0


    # CLASS ==========================================================================
    # 0 : person 1 : card
    # ================================================================================
    def hard_vote(self, queue):
        return statistics.mode(queue)


    def yolo_pub(self):
        ret, frame = self.capture.read()                                    # 웹캠으로부터 프레임을 읽어옴. ret은 성공 여부를 나타내는 불리언 값, frame은 읽어온 이미지 데이터.
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")     # OpenCV 이미지를 ROS Image 메시지로 변환. bgr8 인코딩을 사용하여 BGR 컬러 형식의 이미지를 표현.
            self.publisher_.publish(img_msg)                                # 변환된 이미지 메시지를 /image_raw 토픽으로 게시합니다.

            # 프레임 직렬화하여 전송준비
            data = pickle.dumps(frame)
            # 메시지 길이 측정
            message_size = struct.pack("L", len(data))
            # 데이터 전송
            socket1.sendall(message_size + data)

        final_check = String()

        while len(self.queue_list) != QUEUE_SIZE: # delete first element
            del self.queue_list[0]

        queue_list = self.queue_list

        # queue voting
        final_id = self.hard_vote(queue_list)
        if final_id == -1:
            final_check.data = 'None'
        else:
            if self.mode == 'person_mode':
                # final_check.data = CLASS_MAP[final_id]
                final_check.data = CLASS_MAP[0]
            elif self.mode == 'card_mode':
                final_check.data = CLASS_MAP[1]

            if self.mode == 'card_mode':
                TCP_msg = "1"
                socket2.sendall(TCP_msg.encode(encoding='utf-8'))

        print(self.currentWeights)

        self.object_pub.publish(final_check)


def main(args=None):
    rclpy.init(args=args)

    try:
        yolo = YOLOv7()
        rclpy.spin(yolo)

    finally:
        yolo.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
