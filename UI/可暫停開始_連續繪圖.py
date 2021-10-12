# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime

import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from random import randint

from ver1 import Ui_MainWindow
import sys


class Mythread(QThread):
    def __init__(self, parent=None):
        super(Mythread, self).__init__()

    # 重写QThread的run函数
    def run(self):
        i = 0
        while i < 100:
            i += 1
            print(i)
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
        self.startstate = False
        #super(MainWindow, self).__init__()
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
        #開始監控
        self.ui.toolButton_2.clicked.connect(self.moniter)
        #設定UI背景
        image = QtGui.QPixmap()
        image.load('UI_Material/BG.jpg')
        image = image.scaled(self.width(), self.height())
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(image))
        self.setPalette(palette)
        #設定APP Icon
        self.setWindowIcon(QtGui.QIcon('UI_Material/Icon.jpg'))
        #宣告執行續
        self.thread1= Mythread()


        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        #self.graphWidget.setBackground('w')

        #self.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [30, 32, 34, 32, 33, 31, 29, 32, 35, 45])

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.ui.graphWidget.plot(self.x, self.y, pen=pen)

        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)


    # def plot(self, hour, temperature):
    #     self.ui.graphWidget.plot(hour, temperature)

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.
        self.data_line.setData(self.x, self.y)  # Update the data.

    def exit(self):
        app.exit()
    def start(self):
        self.thread1.start()
    def moniter(self):
        if(self.startstate ==False):
            print("開始監控")
            self.timer.start()
            self.startstate = True
        elif(self.startstate==True):
            print("停止監控")
            self.timer.stop()
            self.startstate==False

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #app.setStyle(QStyleFactory.create("Windows"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())