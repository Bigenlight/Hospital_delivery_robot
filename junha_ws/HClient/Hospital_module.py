# Hospital_module.py 는 추후 병원 데이터베이스 모듈로 설계 예정
import datetime
import socket
from queue import Queue

class Hospital():

    def __init__(self):

        self.queue_meal = Queue()

    def text_analysis(self, speech_string, service_type):

        if service_type == 'location' :
            if '외과' in speech_string or '내과' in speech_string or '편의점' in speech_string :
                if '외과' in speech_string: return '외과는 2층 입니다.'
                if '내과' in speech_string: return '내과는 3층 입니다.'
                if '편의점' in speech_string: return '편의점은 지하 1층 입니다.'
            else: return '원하시는 위치를 찾지 못 하였습니다.'

        if service_type == 'administration' :
            if '접수' in speech_string or '수납' in speech_string :
                if '접수' in speech_string: return '접수는 1층으로 가셔야 합니다. 번호표를 뽑고 대기하시면 됩니다.'
                if '수납' in speech_string: return '수납은 1층으로 가셔야 합니다. 무인수납기를 이용해 주세요.'
            else : return '원하시는 서비스를 찾지 못 하였습니다.'

        if service_type == 'meal' :
            if '양식' in speech_string or '한식' in speech_string :

                if '양식' in speech_string:
                    self.create_meal_list('양식')
                    return '양식으로 접수 되었습니다.'

                if '한식' in speech_string:
                    self.create_meal_list('한식')
                    return '한식으로 접수 되었습니다.'

            else : return '원하시는 메뉴를 찾지 못 하였습니다. 다시 한번 말씀해 주세요'

    def create_meal_list(self, meal):

        self.now = datetime.datetime.now()

        self.meal_str = self.now.strftime("%H시 %M분 %S초") + " : " + meal + "\n"
        self.queue_meal.put(self.meal_str)

        '''
        file_name = "/home/junha/23_HF110/junha_ws/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt"
        # 식사 리스트 저장경로 역시 각자의 컴퓨터에 맞게 지정해야 함.
        # "/home/[이름]/23_HF110/junha_ws/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt"

        with open(file_name, 'a') as file:
            file.write(self.now.strftime("%H시 %M분 %S초") + " : " + meal + "\n")
        '''


    def TCP_start(self, IP_ADDRESS, TCP_PORT):

        self.server_ip = socket.gethostbyname(IP_ADDRESS)

        self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        while True:
            try:
                self.TCP_socket.connect((self.server_ip, TCP_PORT))
                break
            except ConnectionRefusedError:
                continue


        while True:
            if self.queue_meal.empty():
                continue
            else:
                self.msg = self.queue_meal.get()
                self.TCP_socket.sendall(self.msg.encode(encoding='utf-8'))





