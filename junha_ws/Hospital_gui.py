import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

import datetime
import os.path
from os import path
import time

import Hospital as Hos




form_class = uic.loadUiType("/home/junha/23_HF110/junha_ws/Hospital_gui.ui")[0]
# .ui 파일이 있는 경로로 설정 하면 됨.
# "/home/[이름]/23_HF110/junha_ws/Hospital_gui.ui"

class Recognition(QThread):

    def __init__(self, class_name, srv_type):
        super().__init__()
        self.parent = class_name
        self.service = srv_type

    def run(self):

        if self.service == 'meal':
            self.parent.lblResult.setText("양식과 한식 중 원하시는 메뉴를 말씀해주세요")
            self.text_to_speech("양식과 한식 중 원하시는 메뉴를 말씀해주세요")
            self.parent.lblSpeechRec.setText("Listening...")


        rec = sr.Recognizer()

        with sr.Microphone() as source:
            audio = rec.listen(source)

        try:
            text = rec.recognize_google(audio, language='ko')
            self.parent.lblSpeechRec.setText(text)

            H = Hos.Hospital_pkg(text)
            result = H.text_analysis(self.service)

            self.parent.lblResult.setText(result)
            self.text_to_speech(result)



            self.parent.lblSpeechRec.setText("원하시는 단어를 말씀해주세요")
            self.parent.lblResult.setText("")

            self.parent.btnLocation.setEnabled(True)
            self.parent.btnService.setEnabled(True)
            self.parent.btnMeal.setEnabled(True)

        except sr.UnknownValueError:
            self.parent.lblSpeechRec.setText("")
            self.parent.lblResult.setText("다시한번 말씀해 주세요")
            self.text_to_speech("다시한번 말씀해 주세요")

            self.run()

        except sr.RequestError:
            self.parent.lblSpeechRec.setText("")
            self.parent.lblResult.setText("오류가 발생하였습니다. 관리자에게 문의하세요.")
            self.text_to_speech("오류가 발생하였습니다. 관리자에게 문의하세요.")


    def text_to_speech(self,input_text):

        file_name = "sample.mp3"
        tts_ko = gTTS(text=input_text, lang='ko')
        tts_ko.save(file_name)

        playsound(file_name)


class WindowClass(QMainWindow, form_class) :


    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btnLocation.setEnabled(True)
        self.btnMeal.setEnabled(True)
        self.btnService.setEnabled(True)

        self.lblSpeechRec.setText("원하시는 단어를 말씀해주세요")
        self.lblResult.setText("")

        self.btnLocation.clicked.connect(self.location_srv)
        self.btnService.clicked.connect(self.administration_srv)
        self.btnMeal.clicked.connect(self.meal_srv)




    def location_srv(self):

        self.btnLocation.setEnabled(False)
        self.btnService.setEnabled(False)
        self.btnMeal.setEnabled(False)

        self.recognition = Recognition(self, "location")

        self.lblSpeechRec.setText("Listening...")
        self.recognition.start()

    def administration_srv(self):

        self.btnLocation.setEnabled(False)
        self.btnService.setEnabled(False)
        self.btnMeal.setEnabled(False)

        self.recognition = Recognition(self, "administration")

        self.lblSpeechRec.setText("Listening...")
        self.recognition.start()

    def meal_srv(self):

        self.btnLocation.setEnabled(False)
        self.btnService.setEnabled(False)
        self.btnMeal.setEnabled(False)

        self.recognition = Recognition(self, "meal")

        self.lblSpeechRec.setText("")

        self.recognition.start()





if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
