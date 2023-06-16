from ui.chushi_designed import Ui_chushi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

from blade_geometry import figure_operation, camber_operation, file_operation
from design_calculation import data_list

from ui import main_leaf
from ui import newwindow
from ui import gongkuang


class beginWindow(QtWidgets.QMainWindow, Ui_chushi):
    """
    初始窗口"""
    main = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.close)
        self.pushButton_new.clicked.connect(self.showset)
        self.pushButton_new_2.clicked.connect(self.showset_gongkuang)
        self.pushButton_read.clicked.connect(self.openFile)
        self.pushButton_open.clicked.connect(self.open)

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, caption='打开文件', directory='./', filter='ALL(*.*);;TEXT(*.txt)',
                                            initialFilter='TEXT(*.txt)')
        if fname[0] != '':
            camber, pp, ps, opt = file_operation.txtinput(str(fname[0]))
            if opt is False:  # 这里直接对ppps赋值，进入主界面后依然会被覆盖
                camber_operation.control_point = camber
                self.main = main_leaf.blade_designer(1, None, pp, ps)
            else:
                data_list.Z_num = opt[0]
                data_list.Zr = opt[1]
                camber_operation.control_point = camber[0][0][0][0]
                figure_operation.TE_radius = camber[0][0][0][2][1]
                figure_operation.blade_dis = camber[0][0][0][3]
                figure_operation.lim = camber[0][0][0][0][2, 0] / 20  # 最后一个控制点的x轴就是叶片宽度
                camber_operation.lim = camber[0][0][0][0][2, 0] / 20
                self.main = main_leaf.blade_designer(2, camber, pp, ps)

            self.setVisible(False)  # 隐藏主界面
            self.main.setVisible(True)

    def showset(self):
        self.main = newwindow.newwindow()
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)

    def showset_gongkuang(self):
        self.main = gongkuang.gongkuang()
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)

    def open(self):
        camber = np.array([[1.97803159, 1.53044833], [11.34468, -0.899818], [14.4335762, -9.90096959]])
        pp = np.array(
            [[1.97803159, 1.53044833], [2.28734559, 2.71255756], [5.97517806, 5.94936882], [9.42264596, 6.49978646],
             [10.50168597, 2.47052067], [12.5460801, 0.57288884], [12.80091383, -2.83838773],
             [13.62560187, -5.24045493], [13.85311348, -7.73692925], [14.47831949, -9.80933095]])
        ps = np.array(
            [[1.97803159, 1.53044833], [1.66871759, 0.3483391], [3.79754413, -0.75141551], [6.45725958, -0.69525079],
             [9.06433283, -1.33214082], [10.81007736, -3.24439291], [12.10524057, -5.45044471],
             [13.62782363, -7.48984497], [14.34180203, -9.85650496]])
        camber_operation.control_point = camber
        figure_operation.pp = pp
        figure_operation.ps = ps
        self.main = main_leaf.blade_designer(1)
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)
