# 웹캠 사용, 이미지 변환, 전송하기 위한 라이브러리들
import cv2
import numpy as np
import socket
import pickle
import struct

# 키보드 입력 감지하기 위한 라이브러리
import keyboard

# 비디오 경로 읽어오기
cap=cv2.VideoCapture(0)

server_ip = socket.gethostbyname('192.168.0.33') # 위에서 설정한 서버 ip
server_port1 = 3333 # 위에서 설정한 서버 포트번호
server_port2 = 4444 # 위에서 설정한 서버 포트번호

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect((server_ip, server_port1))

socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket2.connect((server_ip, server_port2))

while True:
    ret,frame=cap.read()

	# 프레임 직렬화하여 전송준비
    data = pickle.dumps(frame)

    # 메시지 길이 측정
    message_size = struct.pack("L", len(data))

    # 데이터 전송
    socket1.sendall(message_size + data)

    if keyboard.is_pressed("e"):
        TCP_msg = "e"
        socket2.sendall(TCP_msg.encode(encoding='utf-8'))