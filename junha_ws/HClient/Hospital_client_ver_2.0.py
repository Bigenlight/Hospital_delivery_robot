import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from PyQt5.QtMultimedia import QSound

from gtts import gTTS
import speech_recognition as sr

import datetime
import os.path
from os import path
import time

from Hospital import Hospital_pkg as Hospital

import threading

from queue import Queue




form_class = uic.loadUiType("/home/junha/23_HF110/junha_ws/HClient/Hospital_client.ui")[0]
# .ui 파일이 있는 경로로 설정 하면 됨.
# "/home/[이름]/23_HF110/junha_ws/Hospital_client.ui"




# 전역 큐 (클래스끼리 값을 주고 받기 위함)
que = Queue()



#
# ---------------------- 사용자 정의 시그널 ----------------------
#

class Signal(QObject):

    user_signal = pyqtSignal()

    def run(self):
        self.user_signal.emit()


sig_analyzing_speech = Signal()
sig_set_default = Signal()






#
# ---------------------- 메인 스레드 ----------------------
#

class WindowClass(QMainWindow, form_class) :


    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 버튼 정의
        self.btnLocation.setEnabled(True)
        self.btnMeal.setEnabled(True)
        self.btnService.setEnabled(True)

        # 초기 창 상태
        self.lblSpeechRec.setText("원하시는 단어를 말씀해주세요")
        self.lblResult.setText("")

        # 클릭 이벤트 발생 시 함수
        self.btnLocation.clicked.connect(lambda: self.start_service("location"))
        self.btnService.clicked.connect(lambda: self.start_service("administration"))
        self.btnMeal.clicked.connect(lambda: self.start_service("meal"))

        # 사용자 정의 시그널 함수
        sig_analyzing_speech.user_signal.connect(self.analyzing_speech) # 음성에 대한 병원 해석 함수 호출
        sig_set_default.user_signal.connect(self.set_default)           # 초기화면 세팅 함수 호출





    # 위치, 행정, 식사 안내를 하나의 함수로 처리할 수 있게 만듬.
    # srv: 서비스의 종류 (location, administration, meal)
    def start_service(self, srv):

        self.service_type = srv
        self.hospital_class = Hospital(srv)

        if srv == "meal":
            self.lblSpeechRec.setText("양식과 한식 중 원하시는 메뉴를 선택해주세요.\n\nListening...")
        else:
            self.lblSpeechRec.setText("Listening...")




        self.btnLocation.setEnabled(False)
        self.btnService.setEnabled(False)
        self.btnMeal.setEnabled(False)

        QSound.play("/home/junha/23_HF110/junha_ws/sample_sound/start_listening_1.wav")
        # 역시 각자에 맞게 파일 경로 수정 해야 함


        self.speech_recognizer = Thr_SpeechRecognizer()
        self.speech_recognizer.start()



    def analyzing_speech(self):

        self.result_data = que.get()


        if(self.result_data == sr.UnknownValueError):
            self.lblSpeechRec.setText("")
            self.lblResult.setText("다시 한번 말씀해 주세요")
            QSound.play("/home/junha/23_HF110/junha_ws/sample_sound/error_1.wav")

        elif(self.result_data == sr.RequestError):
            self.lblSpeechRec.setText("")
            self.lblResult.setText("오류가 발생하였습니다. 관리자에게 문의하세요.")
            QSound.play("/home/junha/23_HF110/junha_ws/sample_sound/error_1.wav")

        else:
            self.lblSpeechRec.setText(self.result_data)
            QSound.play("/home/junha/23_HF110/junha_ws/sample_sound/stop_listening_1.wav")

            self.hos_output = self.hospital_class.text_analysis(self.result_data)
            time.sleep(1) # 스레드간 충돌을 막기 위해 1초 쉬게 함
            self.lblResult.setText(self.hos_output)

        self.thr_setDefault = Thr_QWindow_setDefault()
        self.thr_setDefault.start()




    def set_default(self):

        # 버튼 정의
        self.btnLocation.setEnabled(True)
        self.btnMeal.setEnabled(True)
        self.btnService.setEnabled(True)

        # 초기 창 상태
        self.lblSpeechRec.setText("원하시는 단어를 말씀해주세요")
        self.lblResult.setText("")






#
# ---------------------- 스레드 함수 정의 ----------------------
#

class Thr_QWindow_setDefault(QThread):

    def __init__(self):
        super().__init__()

    def run(self):

        time.sleep(4) # 초기화면으로 돌아오는 시간
        self.quit()
        sig_set_default.run()


class Thr_SpeechRecognizer(QThread):

    def __init__(self):
        super().__init__()


    def run(self):


        rec = sr.Recognizer()

        with sr.Microphone() as source:
            audio = rec.listen(source, None, 5)
            # audio >> <speech_recognition.audio.AudioData object at 0x7f8b81780a00>
            # 즉 audio는 AudioData 객체

        try:
            self.result = rec.recognize_google(audio, language='ko')
            # result : 말한 음성을 인식한 문자열

            que.put(self.result) # 전역 큐에 결과 값을 집어넣음 (다른 클래스에서도 값을 사용하기 위함)
            self.quit()          # 스레드 종료 함수 > 그냥 혹시 몰라서 넣어본거
            sig_analyzing_speech.run()

        except sr.UnknownValueError :
            self.result = sr.UnknownValueError
            que.put(self.result)
            self.quit()
            sig_analyzing_speech.run()

        except sr.RequestError :
            self.result = sr.RequestError
            que.put(self.result)
            self.quit()
            sig_analyzing_speech.run()






if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
