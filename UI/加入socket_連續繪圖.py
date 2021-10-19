# -*- coding: utf-8 -*-
import PyQt5.QtWidgets
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from random import randint
from ver1 import Ui_MainWindow
import sys
import socket
from _thread import *
import math
import numpy as np


class Mythread(QThread):
    SENSOR_DATA = pyqtSignal(object)
    ThreadCount = pyqtSignal(int)
    print("成功開啟現成")
    def __init__(self,*args, **kwargs):
        super(Mythread, self).__init__()

    # 重写QThread的run函数
    def run(self):
        ServerSocket = socket.socket()
        host ='172.20.10.3'
        port = 8090
        ThreadCount = 0
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Waitiing for a Connection..')
        ServerSocket.listen(5)
        self.ThreadCounts = 0
        while True:
            Client, address = ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client,))
            self.ThreadCounts += 1
            self.ThreadCount.emit(self.ThreadCounts)#向LCD顯示函式發射目前現成連接數量
            print('Thread Number: ' + str(ThreadCount))
        ServerSocket.close()
    def threaded_client(self,connection):
        connection.send(str.encode('Welcome to the Servern'))
        while True:
            self.data = connection.recv(2048)
            self.SENSOR_DATA.emit(self.data)#向GET DATA函式發射目前數據
            self.reply = 'Server Says: ' + self.data.decode('utf-8')
            if not self.data:
                break
            connection.sendall(str.encode(self.reply))
        connection.close()



class MySingnal(QThread):
   # 信号创建记得放在__init__()之外，作为类属性
   Data_Signal = QtCore.pyqtSignal(list)
   Tip_Singal = QtCore.pyqtSignal(str,str)
   Paint_Singal = QtCore.pyqtSignal(int)

   def __init__(self):
       super(MySingnal,self).__init__()

   def Data_Sender(self,Data):
       self.Data_Signal.emit(Data)

   def Tip_Sender(self,title,message):
       self.Tip_Singal.emit(title,message)

   def Paint_Sender(self,int_data):
       self.Paint_Singal.emit(int_data)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        self.startstate = False#是否開始監控 初始化為否
        self.connectstate = False#初始化連線狀態 為否
        self.testmodestate_self =False
        self.ThreadCount = 0 #感測器連線數量
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)#這邊的ui指的是我設計的ver1
        #self.ui.toolButton_2.clicked.connect(self.start)
        # Menu
        self.ui.retranslateUi(self)
        self.ui.actionClose.setShortcut('Ctrl+Q')
        self.ui.actionClose.triggered.connect(app.exit)
        self.ui.actionClose.setIcon(QtGui.QIcon('UI_Material/CloseIcon.png'))
        # ToolBar
        self.ui.toolButton.setShortcut('Ctrl+E')
        self.ui.toolButton.setIcon(QtGui.QIcon('UI_Material/CloseIcon.png'))
        self.ui.toolButton.clicked.connect(self.exit) #綁定觸發事件
        #測試內網鈕
        self.ui.toolButton_4.clicked.connect(self.test_mode)
        #開始監控
        self.ui.toolButton_2.clicked.connect(self.moniter)
        #連線
        self.ui.toolButton_3.clicked.connect(self.connect_socket)
        #設定UI背景
        image = QtGui.QPixmap()
        image.load('UI_Material/BG.png')
        image = image.scaled(self.width(), self.height())
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(image))
        self.setPalette(palette)
        #設定APP Icon
        self.setWindowIcon(QtGui.QIcon('UI_Material/Icon.jpg'))
        #宣告執行續
        self.thread1= Mythread()
        #Label2文字
        self.ui.label_2.setStyleSheet("color:blue;background-color:white;")#給他框起來
        self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_2.setText("Normal State")
        #初始化IP顯示
        self.ip = self.get_host_ip()
        #self.ui.label_4.setStyleSheet("color:black;background-color:white;")  # 給他框起來
        self.ui.label_4.setText("當前連線IP = "+self.ip)
        #lcd顯示線程數量
        self.ui.lcdNumber.setDigitCount(12)
        self.ui.lcdNumber.setMode(PyQt5.QtWidgets.QLCDNumber.Dec)
        self.ui.lcdNumber.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        self.ui.lcdNumber.display(str(self.ThreadCount))
        #ComboBox
        #self.ui.comboBox.currentIndexChanged.connect(self.display)
        #self.ui.comboBox.currentIndexChanged.connect(self.datasourse)
        #Thread連結
        # 宣告執行緒例項
        self.ServerThread = Mythread()
        #繫結SENSOR_DATA函式傳遞
        self.ServerThread.SENSOR_DATA.connect(self.GET_DATA)
        self.ServerThread.ThreadCount.connect(self.display_threadCount)


        self.x = list(range(100))  # 100 time points
        #self.y = [randint(0, 100) for _ in range(100)]  # 100 data points
        self.y =list(0 for _ in range(100))
        self.ui.graphWidget.setBackground('w')
        self.ui.graphWidget.setTitle("Measure")
        pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)

        #self.ui.graphWidget.plot(hour, temperature, pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))
        self.ui.graphWidget.setLabel('left', "<span style=\"color:red;font-size:20px\">Voltage (mV)</span>")
        self.ui.graphWidget.setLabel('bottom', "<span style=\"color:red;font-size:20px\">Time (ms)</span>")
        #self.ui.graphWidget.
        pen = pg.mkPen(color=(255, 0, 0),style=QtCore.Qt.DashLine)
        self.data_line = self.ui.graphWidget.plot(self.x, self.y, pen=pen)
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
    # def plot(self, hour, temperature):
    #     self.ui.graphWidget.plot(hour, temperature)
        self.tcont=0

    def update_plot_data(self):
        if(self.ui.comboBox_2.currentText() == "模擬數據"):
            self.y = self.y[1:]  # Remove the first
            self.y.append(randint(0, 100))  # Add a new random value.
            self.data_line.setData(self.x, self.y,symbol='+')  # Update the data.
        elif(self.ui.comboBox_2.currentText() == "清空數據"):
            self.y =list(0 for _ in range(100))
            self.data_line.setData(self.x, self.y)  # Update the data.
        elif(self.ui.comboBox_2.currentText() == "即時數據"):
            x = np.linspace(self.tcont, self.tcont+100, 100)

            self.tcont+=100
            self.y = self.y[1:]  # Remove the first
            #self.y.append( )  # Add a new random value.
            self.data_line.setData(self.x,  np.sin(x/2)+0.1*randint(1,2),symbol='+')  # Update the data.
            #self.data_line.setData(self.x, self.Y_DATA)  # Update the data.
    def exit(self):
        app.exit()
    def start(self):
        self.thread1.start()
    def connect_socket(self):
        self.ui.label_2.setText("伺服器已開啟")
        self.ui.label_2.setStyleSheet("color:red;background-color:white;")  # 給他框起來
        self.server_thread()

    def moniter(self):
        if(self.startstate ==False):
            print("開始監控",self.startstate)
            self.ui.label_2.setText("Normal Monitoring")
            self.ui.label_2.setStyleSheet("color:green;background-color:white;")  # 給他框起來
            self.timer.start()
            self.startstate = True
        elif(self.startstate==True):
            print("停止監控",self.startstate)
            self.ui.label_2.setStyleSheet("color:red;background-color:white;")  # 給他框起來
            self.ui.label_2.setText("STop  Monitoring")
            self.timer.stop()
            self.startstate =False
    def get_host_ip(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.connect(('8.8.8.8', 80))
            self.ip = self.s.getsockname()[0]
        finally:
            self.s.close()
        return self.ip
    def test_mode(self):
        self.testmodestate_self = not self.testmodestate_self
        self.ui.label_5.setText("內網模式"+str(self.testmodestate_self))
        if(self.testmodestate_self == True):
            self.ui.label_4.setText("當前連線IP = 127.0.0.1" )
            self.testmodestate.emit(True)
        else:
            self.ip = self.get_host_ip()
            self.ui.label_4.setText("當前連線IP = " + self.ip)
            self.testmodestate.emit(False)
    def server_thread(self):
        print("成功進入serverThread")

        self.ServerThread.start()
    def GET_DATA(self,DATA):
        print(DATA)
        print("哈囉")
        self.Y_DATA = list(map(int ,bytes.decode(DATA).split(' ')))
        #print("成功GET DATA = ",self.Y_DATA)
    def display_threadCount(self,ThreadCount):
        self.ui.lcdNumber.display(str(ThreadCount))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #app.setStyle(QStyleFactory.create("Windows"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())