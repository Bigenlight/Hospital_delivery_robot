import pickle
import socket
import struct
import threading
import cv2

import numpy as np

# -------------------------------- QT Designer #
import sys                                     #
from PyQt5.QtWidgets import *                  #
from PyQt5.QtCore import *                     #
from PyQt5.QtGui import *                      #
from PyQt5 import uic                          #
from PyQt5 import QtWidgets, QtGui, QtCore     #
import datetime                                #
# -------------------------------------------- #


# 코드 시작 전 IP ADDRESS 수정하기



Main_ui = uic.loadUiType("/home/junha/23_HF110/junha_ws/HServer/Hospital_server.ui")[0]



class WindowClass(QMainWindow, Main_ui) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btnConnect.clicked.connect(self.thr_start)

        # self.btnLog.clicked.connect(self.open_EmergencyLog)

    def thr_start(self):

        thr_openserver_socket1 = threading.Thread(target=self.open_server_socket1)
        thr_openserver_socket2 = threading.Thread(target=self.open_server_socket2)

        thr_openserver_socket1.start()
        thr_openserver_socket2.start()


    def open_server_socket1(self):


        HOST = '192.168.0.6'
        PORT1 = 3333



        def recvall(sock, count):
            buf = b''
            while count:
                newbuf = sock.recv(count)
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
            return buf


        socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


        socket1.bind((HOST,PORT1))
        socket1.listen(10)

        self.lblConn1_Status.setText("Waiting for connection...")

        conn1, addr1 = socket1.accept()


        self.lblConn1_Status.setText("Camera Connected " + "[" + str(addr1)[2:13] + "]")

        while True:
            length = recvall(conn1, 16)
            stringData = recvall(conn1, int(length))
            data = np.fromstring(stringData, dtype = 'uint8')

            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)



            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)

            qPix = QPixmap.fromImage(qImg.scaled(1280, 720))
            self.lblPixmap.setPixmap(qPix)



    def open_server_socket2(self):



        def receive_data(conn, data_buffer):
            while True:
                data = conn.recv(4096)
                data_buffer.append(data)



        HOST = '192.168.0.6'
        PORT2 = 4444

        socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket2.bind((HOST, PORT2))
        socket2.listen()

        self.lblConn2_Status.setText("Waiting for connection...")

        conn2, addr2 = socket2.accept()

        self.lblConn2_Status.setText("Alert System Connected " + "[" + str(addr2)[2:13] + "]")


        data_buffer = []
        prev_len = len(data_buffer)


        data_thread = threading.Thread(target=receive_data, args=(conn2, data_buffer))
        data_thread.start()


        while True:

            if prev_len != len(data_buffer):

                print("emergency!!!!!!!!!!")

                self.now = datetime.datetime.now()
                self.str_status = "Emergency at " + self.now.strftime("%H시 %M분 %S초")

                self.lblStatus.setText(self.str_status)

                # self.temp = QListWidgetItem(self.str_status)
                # subWindow_Log.listEmergency.addItem(self.temp)

            prev_len = len(data_buffer)


#     def open_EmergencyLog(self):
#         second_window = second()
#         second_window.exec()


# class second(QDialog):

#     def __init__(self):
#         super().__init__()
#         self.ui = uic.loadUi("/home/junha/Desktop/Pixmap_study/Hospital_sub_Emergency.ui", self)
#         self.show()



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


