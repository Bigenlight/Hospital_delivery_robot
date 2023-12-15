import pickle
import socket
import struct
import threading
import cv2

# IP주소, 포트번호(포트번호는 임의로 지정하는 고유번호라고 생각하면 됨.)
HOST = '192.168.0.33'
PORT1 = 3333
PORT2 = 4444

# 데이터를 수신하는 함수
def receive_data(conn, data_buffer):
    while True:
        data = conn.recv(4096)
        data_buffer.append(data)

# server1(카메라 영상) 소켓 만들기(소켓 하나로 영상, 응급상황 둘 다 받으려니까 잘 안돼서 좀 짜치긴 하지만 소켓 두 개 팠습니다.)
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓1 생성')
s1.bind((HOST, PORT1))
s1.listen()

# server2(응급상황 소식) 소켓 만들기(소켓 하나로 영상, 응급상황 둘 다 받으려니까 잘 안돼서 좀 짜치긴 하지만 소켓 두 개 팠습니다.)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓2 생성')
s2.bind((HOST, PORT2))
s2.listen()

# 연결됨(클라이언트 소켓, 주소 정보 얻고 출력)
conn1, addr1 = s1.accept()
conn2, addr2 = s2.accept()
print('connected client1 addr:', addr1)
print('connected client2 addr:', addr2)

# server1 데이터 저장할 변수
data = b''
payload_size = struct.calcsize("L")

# server2 데이터를 저장할 리스트, 이전 데이터 리스트 길이 저장하는 변수(데이터 들어왔는지 확인히기 위한 용도)
data_buffer = []
prev_len = len(data_buffer)

# 쓰레드 생성(쓰레드를 안 쓰면 같은 IP 주소로 데이터를 수신했을 때 두번째 건 수신이 안돼서 server2 쓰레드 생성함)
data_thread = threading.Thread(target=receive_data, args=(conn2, data_buffer))
data_thread.start()

while True:
    
    # server2에서 응급상황 받았다는 조건문! 여기서 화면에 막 사이렌 울리고 왜앵왜앵 잘 하면 될 듯.(데이터 배열 길이 계속 체크하면서 이전 길이와 다르면 데이터 들어왔다고 판단)
    if prev_len != len(data_buffer):
        print("emergency!!")
    prev_len = len(data_buffer)


    # 이 밑은 server1에서 영상 데이터 받아서 해당 데이터를 우리가 써먹을 수 있는 형태로 잘 변환하는 과정인 것 같은데 아직 잘 알아보진 않았음. 
    # 프레임 사이즈 측정
    while len(data) < payload_size:
        data += conn1.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # 메시지 사이즈 기준으로 데이터 구성
    while len(data) < msg_size:
        data += conn1.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # 프레임 로드
    frame = pickle.loads(frame_data)

    # 일단은 numpy배열 변수 'frame'을 그냥 imshow 함수로 띄우기만 했는데 이 변수를 잘 사용해서 GUI에 띄우면 될 듯 합니다.
    # 창으로 나타내기
    cv2.imshow('frame', frame)
    cv2.waitKey(1)