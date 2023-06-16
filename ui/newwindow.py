
from ui.new_designed import Ui_newwindow
from ui import Figure_Canvas

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

from blade_geometry import get_camber, camber_operation

from ui import main_leaf

class newwindow(QtWidgets.QMainWindow, Ui_newwindow):
    number_cnt = 1
    main = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.number()
        self.show_info = QTimer()
        self.show_info.start(100)
        self.slot_init()

    def slot_init(self):
        self.pushButton_down.clicked.connect(self.down)
        self.pushButton_up.clicked.connect(self.up)
        self.show_info.timeout.connect(self.show_coordinate)
        self.lineEdit_x.textChanged.connect(self.edit_show)
        self.lineEdit_y.textChanged.connect(self.edit_show)

    def edit_show(self):
        x = self.lineEdit_x.text()
        y = self.lineEdit_y.text()
        if x == '' or y == '':
            self.info.setText('请先选定一个点（或直接在文本框中输入坐标）再进行下一步操作')
        else:
            try:
                x = float(x)
                y = float(y)
                if len(get_camber.control_point) > get_camber.cnt:
                    get_camber.control_point.pop()
                    get_camber.control_point.append([x, y])
                else:
                    get_camber.control_point.append([x, y])
                get_camber.opt_plot(self.camber_Figure, self.ax_camber)
            except:
                self.info.setText('输入有误！')

    def show_coordinate(self):
        x = get_camber.x_mouse
        y = get_camber.y_mouse
        if x is not None and y is not None:
            self.info.setText(f'弧度曲线: {x:.3f},{y:.3f}')
            if get_camber.flag == 1:
                self.lineEdit_x.setText(f'{x:.3f}')
                self.lineEdit_y.setText(f'{y:.3f}')
                get_camber.flag = 0

    def initUI(self):
        self.camber_Figure = Figure_Canvas.Figure_Canvas()
        self.camber_FigureLayout = QGridLayout(self.camber)
        self.camber_FigureLayout.addWidget(self.camber_Figure)
        self.camber_Figure.ax.remove()
        self.ax_camber = self.camber_Figure.fig.add_subplot()
        self.get_camber()

    def get_camber(self):
        get_camber.auto_plot('camber.txt', self.camber_Figure, self.ax_camber)

    def up(self):
        if self.number_cnt != 1:  # 不是第一个
            self.number_cnt = self.number_cnt - 1
            if self.number_cnt == 2:
                self.pushButton_down.setText("下一个点")
            self.number()
            get_camber.cancel_opt(self.camber_Figure, self.ax_camber)

    def down(self):
        x = self.lineEdit_x.text()
        y = self.lineEdit_y.text()
        if x == '' or y == '':
            self.info.setText('请先选定一个点（或直接在文本框中输入坐标）再进行下一步操作')
        else:
            try:
                x = float(x)
                y = float(y)
                if self.number_cnt != 3:  # 没满
                    self.number_cnt = self.number_cnt + 1
                    self.number()
                    get_camber.confirm_opt(x, y, self.camber_Figure, self.ax_camber)
                    if self.number_cnt == 3:
                        self.pushButton_down.setText("确定")
                else:
                    get_camber.confirm_opt(x, y, self.camber_Figure, self.ax_camber)
                    camber_operation.control_point = np.array(get_camber.control_point)
                    self.show_info.stop()
                    self.main = main_leaf.blade_designer(1)
                    self.setVisible(False)  # 隐藏主界面
                    self.main.setVisible(True)
            except:
                self.info.setText('输入有误！')

    def number(self):
        self.label.setText(f'第{self.number_cnt}/3个点')
