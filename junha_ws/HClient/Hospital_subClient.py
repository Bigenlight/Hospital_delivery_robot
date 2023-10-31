import cv2
import socket
import numpy as np
import keyboard


# 시작 전 IP ADDRESS 수정하기

cap = cv2.VideoCapture(0)


server_ip = socket.gethostbyname('192.168.0.33')

server_port1 = 3333 # 위에서 설정한 서버 포트번호
server_port2 = 4444 # 위에서 설정한 서버 포트번호

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect((server_ip, server_port1))

socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket2.connect((server_ip, server_port2))


encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:

    # --------------------------------------------------------------- socket1
    ret, frame = cap.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)

    data = np.array(frame)

    stringData = data.tostring()

    socket1.sendall((str(len(stringData))).encode().ljust(16) + stringData)


    # --------------------------------------------------------------- socket2
    if keyboard.is_pressed("e"):
        TCP_msg = "e"
        socket2.sendall(TCP_msg.encode(encoding='utf-8'))
