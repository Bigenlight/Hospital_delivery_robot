import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from enum import Enum
import datetime
import os.path
from os import path


form_class = uic.loadUiType("/home/junha/Desktop/Hanium/Meal_gui/Hanium_Meal_Test.ui")[0]
# loadUiType() 에 작동시키는 .ui 파일의 위치 입력


# 모드 분류
class Mode(Enum):
    Driving = "Driving" # 평상시 주행 모드
    Patient = "Patient" # 환자 케어 모드 (식판 나르기 등)
    Emergency = "Emergency" # 긴급 상황 모드


class WindowClass(QMainWindow, form_class) :
    __Meal_buffer = ""
    __mode = Mode.Driving

    # 현재 시간을 불러오는 클래스 함수
    now = datetime.datetime.now()


    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 버튼을 누르기 전 까지 코드 진행을 중지해야 하므로 비동기 프로그래밍 코드를 넣음.
        self.local_event_loop = QEventLoop()

        self.btnMeal_1.setEnabled(False)
        self.btnMeal_2.setEnabled(False)
        self.btnMeal_3.setEnabled(False)
        self.btnMeal_4.setEnabled(False)
        self.btnStartSelect.setEnabled(False)
        self.btnUndo.setEnabled(False)
        self.btnExport.setEnabled(False)


        self.radDriving.clicked.connect(self.mode_select)
        self.radPatient.clicked.connect(self.mode_select)
        self.radEmergency.clicked.connect(self.mode_select)

        self.btnCreate.clicked.connect(self.create_new_file)


        self.btnMeal_1.clicked.connect(self.meal1_chosen)
        self.btnMeal_2.clicked.connect(self.meal2_chosen)
        self.btnMeal_3.clicked.connect(self.meal3_chosen)
        self.btnMeal_4.clicked.connect(self.meal4_chosen)


        self.btnStartSelect.clicked.connect(self.start_to_select)
        self.btnUndo.clicked.connect(self.selecting_meal)

        self.btnExport.clicked.connect(self.export)

        self.lblStatus.setText("Create Meal List File")



    def mode_select(self):
        if self.radDriving.isChecked(): self.__mode = Mode.Driving
        if self.radPatient.isChecked(): self.__mode = Mode.Patient
        if self.radEmergency.isChecked(): self.__mode = Mode.Emergency



    def create_new_file(self):
        file_name = "/home/junha/Desktop/Hanium/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt"


        if path.exists(file_name):
            self.lblStatus.setText("Already existed file. Start to select meal or export meal list")

            self.btnStartSelect.setEnabled(True)
            self.btnExport.setEnabled(True)

        else:
            # f = open(file_name, "w")
            # f.close()

            self.btnStartSelect.setEnabled(True)
            self.btnExport.setEnabled(True)




    def start_to_select(self):

        if(self.__mode == Mode.Driving):
            self.btnStartSelect.setEnabled(False)

            self.now = datetime.datetime.now()

            with open("/home/junha/Desktop/Hanium/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt", 'a') as file:
                file.write(self.now.strftime("%H%M%S") + " : ")

            self.btnMeal_1.setEnabled(True)
            self.btnMeal_2.setEnabled(True)
            self.btnMeal_3.setEnabled(True)
            self.btnMeal_4.setEnabled(True)

            self.btnUndo.setEnabled(False)

            self.lblStatus.setText("Select your meal")

            self.selecting_meal()
        else:
            self.lblStatus.setText("NOT THIS MODE! Only available in Driving Mode.")



    def selecting_meal(self):

        if(self.__mode == Mode.Driving):

            self.local_event_loop.exec()

            with open("/home/junha/Desktop/Hanium/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt", 'a') as file:
                file.write(self.__Meal_buffer + "\n")

            self.lblStatus.setText(self.__Meal_buffer + " is chosen.")

            self.btnMeal_1.setEnabled(False)
            self.btnMeal_2.setEnabled(False)
            self.btnMeal_3.setEnabled(False)
            self.btnMeal_4.setEnabled(False)
            self.btnStartSelect.setEnabled(True)

            self.btnUndo.setEnabled(True)

        else:
            self.lblStatus.setText("NOT THIS MODE! Only available in Driving Mode.")


    def meal1_chosen(self): self.__Meal_buffer = "양식"; self.local_event_loop.exit()
    def meal2_chosen(self): self.__Meal_buffer = "한식"; self.local_event_loop.exit()
    def meal3_chosen(self): self.__Meal_buffer = "중식"; self.local_event_loop.exit()
    def meal4_chosen(self): self.__Meal_buffer = "일식"; self.local_event_loop.exit()


    def export(self):
        open("/home/junha/Desktop/Hanium/Meal_list/Meal_list_" + self.now.strftime("%Y%m%d") + ".txt")






if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
