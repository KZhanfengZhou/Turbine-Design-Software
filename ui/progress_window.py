from PyQt5.QtGui import QFont
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import optimize.genetic_algorithm
from design_calculation import data_list


class Thread_num(QThread):
    i = 0

    def __init__(self):
        super().__init__()

    def run(self):
        for self.i in range(data_list.Z_num):
            bestind = optimize.genetic_algorithm.genetic_algorithm_optimize(self.i)
            # print(bestind)
            ret = []
            for j in range(data_list.Zr):
                ret.append([bestind['Gene'].data[j], bestind['Gene'].data[j + data_list.Zr * 3]])
            data_list.optimize_result.append(ret)
            data_list.optimize_fitness.append(bestind['fitness'])


class ProgressWindow(QWidget):
    def __init__(self, optimize_values):
        super().__init__()
        self.pv = 0
        # 申明一个时钟控件
        self.timer1 = QBasicTimer()
        self.thread = Thread_num()
        self.initUI()
        # 连接结束信号
        self.thread.finished.connect(self.optimize_finished)
        # 线程启动
        self.thread.start()
        self.timer1.start(100, self)
        optimize.genetic_algorithm.CXPB = float(optimize_values[0])
        optimize.genetic_algorithm.MUTPB = float(optimize_values[1])
        optimize.genetic_algorithm.NGEN = int(optimize_values[2])
        optimize.genetic_algorithm.popsize = int(optimize_values[3])

    def initUI(self):
        self.setWindowTitle("正在优化")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/source/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(300, 130)
        self.setFixedSize(self.width(), self.height())
        # 载入进度条控件
        self.pgb = QProgressBar(self)
        self.pgb.move(25, 30)
        self.pgb.resize(250, 20)

        self.btn_cancel = QPushButton("隐藏", self)
        self.btn_cancel.move(180, 70)

        # self.pgb.setStyleSheet(
        # "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);  background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: 10px; margin: 0.1px;  width: 1px;}")
        # 其中 width 是设置进度条每一步的宽度
        # margin 设置两步之间的间隔
        self.pgb.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background:QLinearGradient(x1:0,y1:0,x2:1,y2:0,stop:0 #666699,stop:1  #DB7093); }")
        # 设置字体
        font = QFont()
        font.setBold(True)
        font.setWeight(30)
        self.pgb.setFont(font)
        # 设置一个值表示进度条的当前进度

        # 设置进度条的范围
        self.pgb.setMinimum(0)
        self.pgb.setMaximum(100)
        self.pgb.setValue(self.pv)
        # 设置进度条文字格式
        self.pgb.setFormat('优化中… %p%'.format(self.pgb.value() - self.pgb.minimum()))  # 只能显示整数

        self.btn_cancel.clicked.connect(self.close)

    def optimize_finished(self):
        self.timer1.stop()
        self.pv = 100
        self.pgb.setValue(self.pv)
        data_list.optimize_flag = 1
        QMessageBox.information(self, '优化计算完成', '优化计算已完成，再次点击优化按钮即可查看结果')
        # print('优化前：')
        # print(data_list.init_fitness)
        # print('优化后')
        # print(data_list.optimize_fitness)
        # print(data_list.optimize_result)

        self.close()

    def cancel(self):
        # self.thread.stop()

        self.close()

    def closeEvent(self, event):
        if data_list.optimize_flag != 1:
            result = QMessageBox.question(self, "警告", "优化算法正在计算，强行停止会造成严重错误。\n此操作是将不会停止优化算法的工作，仅仅只是隐藏进度条。\n是否执行？",
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def timerEvent(self, e):
        self.pv = (self.thread.i * optimize.genetic_algorithm.NGEN + optimize.genetic_algorithm.generation) / \
                  data_list.Z_num / optimize.genetic_algorithm.NGEN * 100
        self.pgb.setValue(self.pv)
