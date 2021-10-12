# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtWidgets import QWidget, QLineEdit, QListWidget, QPushButton,\
    QVBoxLayout, QLabel
import time
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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.toolButton_2.clicked.connect(self.start)
        # Menu
        self.ui.retranslateUi(self)
        self.ui.actionClose.setShortcut('Ctrl+Q')
        self.ui.actionClose.triggered.connect(app.exit)
        self.ui.actionClose.setIcon(QtGui.QIcon('UI_Material/CloseIcon.png'))
        # ToolBar
        self.ui.toolButton.setShortcut('Ctrl+E')
        self.ui.toolButton.setIcon(QtGui.QIcon('UI_Material/CloseIcon.png'))
        self.ui.toolButton.clicked.connect(self.exit) #綁定觸發事件
        #宣告執行續
        self.thread1= Mythread()

    def exit(self):
        app.exit()
    def start(self):
        self.thread1.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())