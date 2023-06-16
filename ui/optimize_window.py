import copy

from design_calculation import data_list
from ui.optimize_designed import Ui_optimize
from PyQt5 import QtWidgets
import matplotlib
import numpy as np
from blade_geometry import circle, calcu, figure_operation
from ui import Figure_Canvas
from PyQt5.QtWidgets import *
import math
from PyQt5 import QtCore

matplotlib.use('Qt5Agg')


class optimize(QtWidgets.QMainWindow, Ui_optimize):
    returnResultSignal = QtCore.pyqtSignal(bool)
    finish_optimize_flag = False

    def __init__(self, all_blade, all_pp_distance, all_ps_distance):
        super().__init__()
        self.setupUi(self)
        self.combo_init()
        self.init_UI()
        self.all_blade = copy.deepcopy(all_blade)
        self.all_pp_distance = copy.deepcopy(all_pp_distance)
        self.all_ps_distance = copy.deepcopy(all_ps_distance)
        self.comboBox_leixing.currentIndexChanged.connect(self.on_combo_change)
        self.comboBox_jishu.currentIndexChanged.connect(self.on_combo_change)
        self.comboBox_jisuanzhan.currentIndexChanged.connect(self.on_combo_change)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.confirm)
        self.on_combo_change(0, 0, 0)
        self.two_d_Figure.mpl_connect('motion_notify_event', self.mouse_move)

    def confirm(self):
        if self.finish_optimize_flag is False:
            self.returnResultSignal.emit(True)
            self.finish_optimize_flag = True
        self.close()

    def init_UI(self):
        self.two_d_Figure = Figure_Canvas.Figure_Canvas()
        self.two_d_FigureLayout = QGridLayout(self.groupBox)
        self.two_d_FigureLayout.addWidget(self.two_d_Figure)
        self.two_d_Figure.ax.remove()
        self.ax2d = self.two_d_Figure.fig.add_subplot()

    def combo_init(self):
        Z = []
        for i in range(1, data_list.Z_num + 1):
            Z.append(str(i))

        Zr = []
        for i in range(1, data_list.Zr + 1):
            Zr.append(str(i))

        self.comboBox_leixing.addItems(["静叶", "动叶"])
        self.comboBox_jishu.addItems(Z)
        self.comboBox_jisuanzhan.addItems(Zr)

    def on_combo_change(self, z=None, zr=None, opt=None):
        if z is None or zr is None or opt is None:
            if self.comboBox_leixing.currentText() == '静叶':
                opt = 0
            else:
                opt = 1
            z = int(self.comboBox_jishu.currentText()) - 1
            zr = int(self.comboBox_jisuanzhan.currentText()) - 1
        self.lineEdit_G_17.setText(f'{data_list.alpha1i[z][zr]}')
        self.lineEdit_G_12.setText(f'{data_list.Beta2i[z][zr]}')
        self.lineEdit_G_15.setText(f'{data_list.init_fitness[z]}')
        self.lineEdit_G_14.setText(f'{data_list.optimize_result[z][zr][0]}')
        self.lineEdit_G_16.setText(f'{90 - data_list.optimize_result[z][zr][1]}')
        self.lineEdit_G_13.setText(f'{data_list.optimize_fitness[z]}')
        self.ax2d.cla()
        tmp_re_p, tmp_re_s = self.get_rep_and_res_from_cp(z, zr, opt, self.all_blade[z][zr][opt][0])
        self.ax2d.plot(tmp_re_p[:, 0], tmp_re_p[:, 1], color='#1f77b4')
        self.ax2d.plot(tmp_re_s[:, 0], tmp_re_s[:, 1], color='#1f77b4')
        self.ax2d.scatter(self.all_blade[z][zr][opt][0][:, 0], self.all_blade[z][zr][opt][0][:, 1], color='#1f77b4')
        # if self.finish_optimize_flag is False:
        if opt == 0:
            beta1 = 90 - 2
            beta2 = data_list.optimize_result[z][zr][opt]
        else:
            beta1 = data_list.Beta1i[z, zr] - 2
            beta2 = 90 - data_list.optimize_result[z][zr][opt]
        beta2 = beta2 - (-0.2 * (90 - data_list.optimize_result[z][zr][opt]) + 14)  # 减2是攻角
        beta1 = (90 - beta1) / 180 * math.pi
        beta2 = (90 - beta2) / 180 * math.pi
        tmp_cp = copy.deepcopy(self.all_blade[z][zr][opt][0])
        if opt == 1:
            for i in range(len(tmp_cp)):
                tmp_cp[i, 1] = -tmp_cp[i, 1]
        tmpx = (math.tan(beta1) * tmp_cp[0, 0] + math.tan(beta2) * tmp_cp[2, 0] + tmp_cp[2, 1] - tmp_cp[0, 1]) / (
                math.tan(beta1) + math.tan(beta2))
        tmpy = math.tan(beta1) * (tmpx - tmp_cp[0, 0]) + tmp_cp[0, 1]
        tmp_cp[1, 0] = tmpx
        tmp_cp[1, 1] = tmpy
        if opt == 1:
            for i in range(len(tmp_cp)):
                tmp_cp[i, 1] = -tmp_cp[i, 1]
        tmp_re_p, tmp_re_s = self.get_rep_and_res_from_cp(z, zr, opt, tmp_cp)
        self.ax2d.plot(tmp_re_p[:, 0], tmp_re_p[:, 1], color='pink')
        self.ax2d.plot(tmp_re_s[:, 0], tmp_re_s[:, 1], color='pink')
        self.ax2d.scatter(tmp_cp[:, 0], tmp_cp[:, 1], color='pink')
        self.two_d_Figure.draw()

    def get_rep_and_res_from_cp(self, z, zr, opt, camber_cp):
        tmp_pp, waste = figure_operation.get_origin_control_point(figure_operation.num_p, False,
                                                                  self.all_pp_distance[z][zr][opt],
                                                                  self.all_blade[z][zr][opt][2][1], None,
                                                                  camber_cp)
        tmp_ps, waste = figure_operation.get_origin_control_point(figure_operation.num_s, True,
                                                                  self.all_ps_distance[z][zr][opt],
                                                                  self.all_blade[z][zr][opt][2][1], None,
                                                                  camber_cp)
        tmp_re_p = calcu.bezier_curve(tmp_pp, figure_operation.npoint - 1)
        xp = np.concatenate(([tmp_pp[0, 0]], tmp_re_p[:, 0]))
        yp = np.concatenate(([tmp_pp[0, 1]], tmp_re_p[:, 1]))
        tmp_re_p = np.column_stack((xp, yp))

        tmp_re_s = calcu.bezier_curve(tmp_ps, figure_operation.npoint - 1)
        xs = np.concatenate(([tmp_ps[0, 0]], tmp_re_s[:, 0]))
        ys = np.concatenate(([tmp_ps[0, 1]], tmp_re_s[:, 1]))
        tmp_re_s = np.column_stack((xs, ys))

        c21, c22 = circle.circle(8, tmp_pp[-1], tmp_ps[-1], 5, tmp_re_p[-2])
        c21 = c21[::-1]
        c22 = c22[::-1]
        c21 = np.delete(c21, 0, 0)
        c22 = np.delete(c22, 0, 0)
        tmp_re_p = np.concatenate([tmp_re_p, c21], axis=0)
        tmp_re_s = np.concatenate([tmp_re_s, c22], axis=0)
        return tmp_re_p, tmp_re_s

    def mouse_move(self, event):
        if event.inaxes:
            self.info.setText(f'{event.xdata:.3f},{event.ydata:.3f}')

    def closeEvent(self, event):
        self.returnResultSignal.emit(False)
        event.accept()
