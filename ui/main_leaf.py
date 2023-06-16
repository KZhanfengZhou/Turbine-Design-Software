from ui.leaf_designed import Ui_sCO2blade_designer
from ui import Figure_Canvas

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

from design_calculation import data_list
from blade_geometry import circle, calcu, figure_operation, hub_shroud_operation, plot_3d, camber_operation, \
    file_operation, Slope
import math

import copy
from ui import canshu
from ui import progress_window
from ui import optimize_window
import base_blade_class
import matplotlib.pyplot as plt
from ui.optimize_input_window import InputDialog


class blade_designer(QtWidgets.QMainWindow, Ui_sCO2blade_designer):
    """
    主窗口
    """
    cnt1 = 0
    cnt = 0
    cnt2 = 0
    camber_cnt = 0
    drag_cnt = 0
    cp_cnt = 0
    square_cnt = 0
    all_blade = None  # 叶片初始数据
    all_pp_distance = None
    all_ps_distance = None
    current_z = None
    current_zr = None
    current_opt = None
    ready_flag = False
    last_z = None
    last_opt = None
    turbine = None

    def __init__(self, opt_type, data=None, pp_init=None, ps_init=None):
        super().__init__()
        self.setupUi(self)
        self.show_info = QTimer()
        self.show_info.start(100)
        self.type = opt_type
        self.current_z = 0
        self.current_zr = 0
        self.current_opt = 0
        if data is None:
            self.combo_init(1, 1)
            data_list.Z_num = 1
            data_list.Zr = 1
            if camber_operation.control_point[0, 0] != 0 or camber_operation.control_point[0, 1] != 0:
                base_point = copy.deepcopy(camber_operation.control_point[0])
                for i in range(3):
                    camber_operation.control_point[i][0] = camber_operation.control_point[i][0] - base_point[0]
                    camber_operation.control_point[i][1] = camber_operation.control_point[i][1] - base_point[1]
            if pp_init is not None:  # 打开单个叶片文件
                self.all_pp_distance = [[[]]]
                self.all_ps_distance = [[[]]]
                self.all_pp_distance[0][0].append(pp_init)
                self.all_ps_distance[0][0].append(ps_init)
                self.initUI(pp_init, ps_init)  # 设置malplotlib的连接
            else:
                self.initUI()  # 设置malplotlib的连接
                self.all_pp_distance = [[[np.array(
                    [0.55265057, 1.45065745, 1.9049298, 1.4, 1.2, 0.90225495, 0.5696306, 0.12181866,
                     0.03256453384853942])]]]
                self.all_ps_distance = [[[np.array(
                    [0.48356924, 0.64079172, 0.17364286, 0.1846661, 0.09128979, 0.05147349, 0.06818834,
                     0.028493967117471992])]]]
            self.all_blade = [[[]]]
            self.all_blade[0][0].append([camber_operation.control_point, [190, 211.83], [0.2, 0.072], 13.3])
            self.all_blade[0][0].append([camber_operation.control_point, [190, 211.83], [0.2, 0.072], 13.3])
            self.turbine = base_blade_class.Turbine(data_list.Z_num, data_list.Zr, self.all_blade, self.all_pp_distance,
                                                    self.all_ps_distance)
            for i in range(data_list.Z_num):
                data_list.stacking_line.append(
                    np.array([[190, 0], [(190 + 211.83) / 2, -(190 + 211.83) / 300], [211.83, 0]]))
            data_list.Stator_Beta1_g = [[[]]]
            data_list.Stator_Beta2_g = [[[]]]
            data_list.Stator_Gamma = [[[]]]
            data_list.Stator_Beta1_g[0][0], data_list.Stator_Beta2_g[0][0], data_list.Stator_Gamma[0][
                0] = calcu.cp_to_angle(self.all_blade[0][0][0][0])
            data_list.Stator_Cmax = [[0]]
            data_list.Stator_r1 = [[0.2]]
            data_list.Stator_r2 = [[0.072]]
            data_list.Stator_t = [[13.3]]
            data_list.Stator_z = [[90]]
            data_list.Stator_B = [[self.all_blade[0][0][0][0][2, 0] - self.all_blade[0][0][0][0][0, 0]]]

            data_list.Rotor_Beta1_g = [[0]]
            data_list.Rotor_Beta2_g = [[0]]
            data_list.Rotor_Gamma = [[0]]
            data_list.Rotor_Cmax = [[0]]
            data_list.Rotor_r1 = [[0]]
            data_list.Rotor_r2 = [[0]]
            data_list.Rotor_t = [[0]]
            data_list.Rotor_z = [[0]]
        else:  # 只要是一组叶片，不管是通过打开文件还是新建项目，都会有self.all_blade
            self.all_blade = copy.deepcopy(data)
            self.combo_init(data_list.Z_num, data_list.Zr)
            # 堆叠规律不管通过什么方式都需要有，所以放在这里 只有静叶有堆叠规律
            for i in range(data_list.Z_num):
                data_list.stacking_line.append(np.array([[data[i][0][0][1][0], 0], [
                    (data[i][0][0][1][0] + data[i][0][0][1][1]) / 2,
                    -(data[i][0][0][1][0] + data[i][0][0][1][1]) / 300],
                                                         [data[i][0][0][1][1], 0]]))
            if pp_init is None:  # 新建一组叶片
                self.all_pp_distance = [[[np.array(
                    [0.55265057, 1.45065745, 1.9049298, 1.4, 1.2, 0.90225495, 0.5696306, 0.12181866,
                     0.03256453384853942]), np.array(
                    [0.55265057, 1.45065745, 1.9049298, 1.4, 1.2, 0.90225495, 0.5696306, 0.12181866,
                     0.03256453384853942])] for j in range(data_list.Zr)] for i in range(data_list.Z_num)]
                self.all_ps_distance = [[[np.array(
                    [0.48356924, 0.64079172, 0.17364286, 0.1846661, 0.09128979, 0.05147349, 0.06818834,
                     0.028493967117471992
                     ]),
                    np.array(
                        [0.48356924, 0.64079172, 0.17364286, 0.1846661, 0.09128979, 0.05147349, 0.06818834,
                         0.028493967117471992
                         ])]
                    for j
                    in range(data_list.Zr)] for i in range(data_list.Z_num)]
                self.initUI()  # 设置malplotlib的连接
            else:  # 打开一组叶片文件
                self.all_pp_distance = pp_init
                self.all_ps_distance = ps_init
                self.initUI(pp_init[0][0][0], ps_init[0][0][0])  # 设置malplotlib的连接
            self.turbine = base_blade_class.Turbine(data_list.Z_num, data_list.Zr, data, self.all_pp_distance,
                                                    self.all_ps_distance)
            for i in range(data_list.Z_num):
                for j in range(data_list.Zr):
                    self.on_combo_change(i, j, 1)
            self.on_combo_change(0, 0, 0)
            self.last_z = self.turbine.current_z
            self.last_opt = self.turbine.current_opt

        self.ready_flag = True
        self.slot_init()
        # 两个默认关闭的按钮
        self.camber_opt()
        self.plot_square()
        self.comboBox_leixing.setContextMenuPolicy(Qt.CustomContextMenu)
        self.comboBox_jishu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.comboBox_jisuanzhan.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_3.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_4.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_5.setContextMenuPolicy(Qt.CustomContextMenu)
        self.comboBox_leixing.customContextMenuRequested.connect(self.showContextMenu)
        self.comboBox_jishu.customContextMenuRequested.connect(self.showContextMenu)
        self.comboBox_jisuanzhan.customContextMenuRequested.connect(self.showContextMenu)
        self.label_3.customContextMenuRequested.connect(self.showContextMenu)
        self.label_4.customContextMenuRequested.connect(self.showContextMenu)
        self.label_5.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        menu = QMenu(self)
        addAction = QAction("添加计算站", self)
        addAction.triggered.connect(self.addItem)
        menu.addAction(addAction)
        menu.exec_(self.sender().mapToGlobal(pos))

    def addItem(self):
        for i in range(data_list.Z_num):
            self.all_blade[i].append(copy.deepcopy(self.all_blade[i][-1]))
            self.all_pp_distance[i].append(copy.deepcopy(self.all_pp_distance[i][-1]))
            self.all_ps_distance[i].append(copy.deepcopy(self.all_ps_distance[i][-1]))

            data_list.Stator_Beta1_g[i].append(data_list.Stator_Beta1_g[i][-1])
            data_list.Stator_Beta2_g[i].append(data_list.Stator_Beta2_g[i][-1])
            data_list.Stator_Gamma[i].append(data_list.Stator_Gamma[i][-1])
            data_list.Stator_Cmax[i].append(data_list.Stator_Cmax[i][-1])
            data_list.Stator_r1[i].append(data_list.Stator_r1[i][-1])
            data_list.Stator_r2[i].append(data_list.Stator_r2[i][-1])
            data_list.Stator_t[i].append(data_list.Stator_t[i][-1])
            data_list.Stator_z[i].append(data_list.Stator_z[i][-1])
            data_list.Stator_B[i].append(data_list.Stator_B[i][-1])

            data_list.Rotor_Beta1_g.append(data_list.Rotor_Beta1_g[i][-1])
            data_list.Rotor_Beta2_g.append(data_list.Rotor_Beta2_g[i][-1])
            data_list.Rotor_Gamma.append(data_list.Rotor_Gamma[i][-1])
            data_list.Rotor_Cmax.append(data_list.Rotor_Cmax[i][-1])
            data_list.Rotor_r1.append(data_list.Rotor_r1[i][-1])
            data_list.Rotor_r2.append(data_list.Rotor_r2[i][-1])
            data_list.Rotor_t.append(data_list.Rotor_t[i][-1])
            data_list.Rotor_z.append(data_list.Rotor_z[i][-1])

        self.comboBox_jisuanzhan.addItems([f'{data_list.Zr + 1}'])
        data_list.Zr = data_list.Zr + 1
        self.confirm_change()
        QMessageBox.information(self, "提示", f"计算站添加成功，当前计算站数: {data_list.Zr}", QMessageBox.Yes)

    def switch1(self):
        self.camber.setVisible(True)
        self.sanwei.setVisible(True)
        self.hubshroud.setVisible(True)
        self.yexing.setVisible(True)

    def switch2(self):
        self.camber.setVisible(True)
        self.sanwei.setVisible(False)
        self.hubshroud.setVisible(False)
        self.yexing.setVisible(False)

    def switch3(self):
        self.camber.setVisible(False)
        self.sanwei.setVisible(True)
        self.hubshroud.setVisible(False)
        self.yexing.setVisible(False)

    def switch4(self):
        self.camber.setVisible(False)
        self.sanwei.setVisible(False)
        self.hubshroud.setVisible(False)
        self.yexing.setVisible(True)

    def optimize(self):
        if data_list.optimize_flag == -1:  # 没有计算
            if self.type == 2:
                reply = QMessageBox.question(self, '是否开始优化',
                                             '叶片优化计算时间可能会比较长，在推荐参数下，可能会超过10分钟，具体时间与电脑配置有关。\n优化过程中软件出现卡顿为正常现象。\n是否执行操作？',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    input_dialog = InputDialog(self)
                    if input_dialog.exec_() == QDialog.Accepted:
                        optimize_values = input_dialog.get_values()
                        self.progresswindow = progress_window.ProgressWindow(optimize_values)
                        data_list.optimize_flag = 0
                        self.progresswindow.show()
            else:
                QMessageBox.information(self, "错误", "叶片优化功能仅限一组叶片，不可用于单个叶片。\n请从工况开始项目，以体验叶片优化功能",
                                        QMessageBox.Yes)
        elif data_list.optimize_flag == 0:
            if self.progresswindow.isVisible() is False:
                self.progresswindow.show()
            else:
                QMessageBox.information(self, "错误", "正在进行优化计算，请勿重复点击",
                                        QMessageBox.Yes)
        else:  # 已经优化完成
            if data_list.optimize_flag == 1:
                self.optimizewindow = optimize_window.optimize(self.all_blade, self.all_pp_distance,
                                                               self.all_ps_distance)
                self.optimizewindow.returnResultSignal.connect(self.handle_optimize_window_result)
                data_list.optimize_flag = 2
                self.optimizewindow.show()
            else:
                self.optimizewindow.show()

    def handle_optimize_window_result(self, result):
        if result is True:
            for z in range(data_list.Z_num):
                for zr in range(data_list.Zr):
                    for opt in range(2):
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
                        tmpx = (math.tan(beta1) * tmp_cp[0, 0] + math.tan(beta2) * tmp_cp[2, 0] + tmp_cp[2, 1] - tmp_cp[
                            0, 1]) / (
                                       math.tan(beta1) + math.tan(beta2))
                        tmpy = math.tan(beta1) * (tmpx - tmp_cp[0, 0]) + tmp_cp[0, 1]
                        tmp_cp[1, 0] = tmpx
                        tmp_cp[1, 1] = tmpy
                        if opt == 1:
                            for i in range(len(tmp_cp)):
                                tmp_cp[i, 1] = -tmp_cp[i, 1]
                        for i in range(3):
                            self.all_blade[z][zr][opt][0][i, 0] = tmp_cp[i, 0]
                            self.all_blade[z][zr][opt][0][i, 1] = tmp_cp[i, 1]

            self.current_z = 0
            self.current_zr = 0
            self.current_opt = 0
            self.turbine.current_z = 0
            self.turbine.current_zr = 0
            self.turbine.current_opt = 0
            self.ready_flag = False

            for i in range(data_list.Z_num):
                for j in range(data_list.Zr):
                    self.on_combo_change(i, j, 1)

            self.ready_flag = True
            self.on_combo_change(0, 0, 0)
            self.comboBox_leixing.setCurrentIndex(0)
            self.comboBox_jisuanzhan.setCurrentIndex(0)
            self.comboBox_jishu.setCurrentIndex(0)
            self.last_z = self.turbine.current_z
            self.last_opt = self.turbine.current_opt
            QMessageBox.information(self, "提示", "叶片优化应用完成", QMessageBox.Yes)

    def initUI(self, init_pp=None, init_ps=None):
        # 先有camber，再有2d，再有3d
        self.camber_Figure = Figure_Canvas.Figure_Canvas()
        self.camber_FigureLayout = QGridLayout(self.camber)
        self.camber_FigureLayout.addWidget(self.camber_Figure)
        self.camber_Figure.ax.remove()
        self.ax_camber = self.camber_Figure.fig.add_subplot()
        self.show_camber()

        self.two_d_Figure = Figure_Canvas.Figure_Canvas()
        self.two_d_FigureLayout = QGridLayout(self.yexing)
        self.two_d_FigureLayout.addWidget(self.two_d_Figure)
        self.two_d_Figure.ax.remove()
        self.ax2d = self.two_d_Figure.fig.add_subplot()

        self.hubshroud_Figure = Figure_Canvas.Figure_Canvas()
        self.hubshroud_FigureLayout = QGridLayout(self.hubshroud)
        self.hubshroud_FigureLayout.addWidget(self.hubshroud_Figure)
        self.hubshroud_Figure.ax.remove()
        self.ax_hubshroud = self.hubshroud_Figure.fig.add_subplot()
        self.show_hubshroud()

        self.three_d_Figure = Figure_Canvas.Figure_Canvas()
        self.three_d_FigureLayout = QGridLayout(self.sanwei)
        self.three_d_FigureLayout.addWidget(self.three_d_Figure)
        self.three_d_Figure.ax.remove()
        self.ax3d = self.three_d_Figure.fig.add_subplot(projection='3d')
        self.ax3d.grid(False)
        self.ax3d.set_axis_off()
        self.three_d_Figure.mpl_connect('axes_enter_event', plot_3d.on_figure_enter)
        self.three_d_Figure.mpl_connect('axes_leave_event', plot_3d.on_figure_leave)

        figure_operation.default_2d_fig = self.two_d_Figure
        figure_operation.default_2d_ax = self.ax2d
        self.show_2d_plot(init_pp, init_ps)
        # figure_operation.default_3d_fig = self.three_d_Figure
        # figure_operation.default_3d_ax = self.ax3d
        self.show_3d()
        # # # 这里需要一个初始的3d画图

    def slot_init(self):
        self.show_info.timeout.connect(self.show_coordinate)
        # self.calcu_3d.clicked.connect(self.show_3d)
        self.pushButton_zhonghu.clicked.connect(self.camber_opt)
        self.pushButton_drag.clicked.connect(self.drag_opt)
        self.pushButton_control.clicked.connect(self.ctrl_point_opt)
        self.pushButton_resize.clicked.connect(self.plot_resize)
        self.pushButton_square.clicked.connect(self.plot_square)
        self.pushButton_about.clicked.connect(self.show_about)
        self.pushButton_meridional.clicked.connect(self.show_meridional)
        self.pushButton_thick.clicked.connect(self.show_cascade_thickness)
        self.pushButton_plot3d.clicked.connect(self.show_3d)
        self.pushButton_optimize.clicked.connect(self.optimize)
        self.pushButton_alter.clicked.connect(self.confirm_change)

        self.pushButton_number.clicked.connect(self.showset_number)
        self.pushButton_output.clicked.connect(self.output)
        self.pushButton_save.clicked.connect(self.save_txt)
        self.pushButton_undo.clicked.connect(self.undo)
        self.pushButton_remake.clicked.connect(self.remake)

        self.pushButton_zong.clicked.connect(self.switch1)
        self.pushButton_hudu.clicked.connect(self.switch2)
        self.pushButton_xiaoguo.clicked.connect(self.switch3)
        self.pushButton_jiemian.clicked.connect(self.switch4)

        self.comboBox_leixing.currentIndexChanged.connect(self.on_combo_change)
        self.comboBox_jishu.currentIndexChanged.connect(self.on_combo_change)
        self.comboBox_jisuanzhan.currentIndexChanged.connect(self.on_combo_change)

    def showset_number(self):
        if self.type == 1 or (self.type == 2 and self.current_zr >= len(data_list.Radial_omega[self.current_z])):
            # QMessageBox.information(self, "警告", "请从工况开始项目，以体验显示参数功能",
            #                         QMessageBox.Yes)
            # 警告
            self.data_window = canshu.canshu(self.turbine.current_z, self.turbine.current_zr, self.turbine.current_opt)
            self.data_window.widget.setVisible(False)
            self.data_window.widget1.setVisible(False)
            self.data_window.widget2.setVisible(True)
            self.data_window.pushButton_yiwei.setEnabled(False)
            self.data_window.pushButton_jingxiang.setEnabled(False)
            self.data_window.widget_dong.setVisible(False)
            self.data_window.widget_jing.setVisible(True)
            self.show_data()
            self.data_window.show()
        else:
            self.data_window = canshu.canshu(self.turbine.current_z, self.turbine.current_zr, self.turbine.current_opt)
            self.show_data()
            self.data_window.show()
        self.data_window.returnResultSignal.connect(self.handle_data_window_result)
        # print(self.data_window.exec())

    def handle_data_window_result(self, result):
        z = result[-3]
        zr = result[-2]
        opt = result[-1]
        if opt == 0:
            data_list.Stator_Beta1_g[z][zr] = result[0]  # 静叶进口几何角
            data_list.Stator_Beta2_g[z][zr] = result[1]  # 静叶出口几何角
            data_list.Stator_Gamma[z][zr] = result[2]  # 静叶安装角
            data_list.Stator_Cmax[z][zr] = result[3]/1000  # 静叶最大厚度
            data_list.Stator_r1[z][zr] = result[4]/1000  # 静叶前缘半径
            data_list.Stator_r2[z][zr] = result[5]/1000  # 静叶尾缘半径
            data_list.Stator_t[z][zr] = result[6]/1000  # 静叶节距
            data_list.Stator_z[z][zr] = result[7]  # 静叶叶片数
            data_list.Stator_B[z][zr] = result[8]/1000  # 静叶叶宽
        else:
            data_list.Rotor_Beta1_g[z][zr] = result[0]  # 动叶进口几何角
            data_list.Rotor_Beta2_g[z][zr] = result[1]  # 动叶出口几何角
            data_list.Rotor_Gamma[z][zr] = result[2]  # 动叶安装角
            data_list.Rotor_Cmax[z][zr] = result[3]/1000  # 动叶最大厚度
            data_list.Rotor_r1[z][zr] = result[4]/1000  # 动叶前缘半径
            data_list.Rotor_r2[z][zr] = result[5]/1000  # 动叶尾缘半径
            data_list.Rotor_t[z][zr] = result[6]/1000  # 动叶节距
            data_list.Rotor_z[z][zr] = result[7]  # 动叶叶片数
            data_list.Rotor_B[z][zr] = result[8]/1000  # 动叶叶宽

        for i in range(3):
            cp = calcu.angle_to_cp(result[0], result[1], result[2], result[8], opt)
            self.all_blade[z][zr][opt][0][i, 0] = cp[i, 0]
            self.all_blade[z][zr][opt][0][i, 1] = cp[i, 1]
        self.all_blade[z][zr][opt][2][0] = result[4]
        self.all_blade[z][zr][opt][2][1] = result[5]
        self.all_blade[z][zr][opt][3] = result[6]
        # self.confirm_change()
        self.feed_back_to_figure_and_camber(z, zr, opt)

    def show_data(self):
        if self.type == 2 and self.current_zr < len(data_list.p2i[self.current_z]):
            # 一维设计的参数在data_list中有
            self.data_window.lineEdit_Z_2.setText(f'{data_list.Z_num}')  # 初始级数
            self.data_window.lineEdit_Z.setText(f'{data_list.Tt0M[self.current_z]:.2f}')  # 级进口总温
            self.data_window.lineEdit_G_10.setText(f'{data_list.pt0M[self.current_z] / 1000:.2f}')  # 级进口总压
            self.data_window.lineEdit_pz_7.setText(f'{data_list.Dm1M[self.current_z] * 1000:.2f}')  # 平均直径
            self.data_window.lineEdit_Tt0_8.setText(f'{data_list.alph1M[self.current_z]:.2f}')  # 静叶出口气流角
            self.data_window.lineEdit_pz_8.setText(f'{data_list.um1M[self.current_z]:.2f}')  # 静叶出口平均周向速度
            self.data_window.lineEdit_Efft0_5.setText(f'{data_list.p2M[self.current_z] / 1000:.2f}')  # 级出口静压
            self.data_window.lineEdit_Eff_14.setText(f'{data_list.omagaM[self.current_z]:.2f}')  # 反动度
            self.data_window.lineEdit_Maz_14.setText(f'{data_list.c1M[self.current_z]:.2f}')  # 静叶出口实际速度
            self.data_window.lineEdit_n_5.setText(f'{data_list.c1uM[self.current_z]:.2f}')  # 静叶出口圆周分速度
            self.data_window.lineEdit_omaga_10.setText(f'{data_list.T1_mixM[self.current_z]:.2f}')  # 静叶出口静温
            self.data_window.lineEdit_xaz_10.setText(f'{data_list.p1M[self.current_z] / 1000:.2f}')  # 静叶出口静压
            self.data_window.lineEdit_alph2z_14.setText(f'{data_list.G1M[self.current_z]:.2f}')  # 静叶出口流量

            self.data_window.lineEdit_Tt0_5.setText(f'{data_list.l1M[self.current_z] * 1000:.2f}')  # 静叶出口叶高
            self.data_window.lineEdit_G_9.setText(f'{data_list.Beta1M[self.current_z]:.2f}')  # 动叶进口相对气流角
            self.data_window.lineEdit_pz_5.setText(f'{data_list.Tt11_mixM[self.current_z]:.2f}')  # 动叶进口总温
            self.data_window.lineEdit_Tt0_6.setText(f'{data_list.Ma2M[self.current_z]:.2f}')  # 动叶出口马赫数
            self.data_window.lineEdit_pz_6.setText(f'{data_list.pt2M[self.current_z] / 1000:.2f}')  # 动叶出口总压
            self.data_window.lineEdit_Efft0_4.setText(f'{data_list.H_to_W1M[self.current_z]:.2f}')  # 静叶叶高叶宽比
            self.data_window.lineEdit_Eff_13.setText(f'{data_list.H_to_W2M[self.current_z]:.2f}')  # 动叶叶高叶宽比
            self.data_window.lineEdit_Maz_13.setText(f'{data_list.Bz1M[self.current_z] * 1000:.2f}')  # 静叶中径处叶宽
            self.data_window.lineEdit_n_4.setText(f'{data_list.Bz2M[self.current_z] * 1000:.2f}')  # 动叶中径处叶宽
            self.data_window.lineEdit_omaga_9.setText(f'{data_list.ACM[self.current_z] * 1000:.2f}')  # 轴向间隙
            self.data_window.lineEdit_xaz_9.setText(f'{data_list.LM[self.current_z] * 1000:.2f}')  # 通流部分长度
            # self.data_window.lineEdit_alph2z_13.setText(
            #     f'{data_list.YM[self.current_z][self.turbine.current_opt]}')  # 通流部分扩张角
            if data_list.blade_layout_method == 0:
                if self.current_opt == 1:
                    self.data_window.lineEdit_alph2z_13.setText(f'{data_list.YM[self.current_z]:.2f}')  # 通流部分扩张角
                else:
                    self.data_window.lineEdit_alph2z_13.setText(f'{0}')  # 通流部分扩张角
            elif data_list.blade_layout_method == 1:
                self.data_window.lineEdit_alph2z_13.setText(f'{data_list.YM[self.current_z]:.2f}')  # 通流部分扩张角

            self.data_window.lineEdit_G_12.setText(f'{data_list.c1i[self.current_z][self.current_zr]:.2f}')  # 静叶出口绝对速度
            self.data_window.lineEdit_Eff_19.setText(
                f'{data_list.c2i[self.current_z][self.current_zr]:.2f}')  # 动叶出口绝对速度
            self.data_window.lineEdit_Eff_20.setText(
                f'{data_list.w1i[self.current_z][self.current_zr]:.2f}')  # 静叶出口相对速度
            self.data_window.lineEdit_Eff_17.setText(
                f'{data_list.w2i[self.current_z][self.current_zr]:.2f}')  # 动叶出口相对速度
            self.data_window.lineEdit_Maz_17.setText(
                f'{data_list.alpha1i[self.current_z][self.current_zr]:.2f}')  # 静叶出口气流角
            self.data_window.lineEdit_k_8.setText(f'{data_list.Beta1i[self.current_z][self.current_zr]:.2f}')  # 动叶进口气流角
            self.data_window.lineEdit_R_8.setText(f'{data_list.T1i[self.current_z][self.current_zr]:.2f}')  # 动叶进口静温
            self.data_window.lineEdit_omaga_12.setText(
                f'{data_list.p1i[self.current_z][self.current_zr] / 1000:.2f}')  # 动叶进口静压
            self.data_window.lineEdit_xaz_12.setText(f'{data_list.G1i[self.current_z]:.2f}')  # 流量
            # self.data_window.lineEdit_alph2z_17.setText(f'{data_list.YM[self.current_z]}')  # 相对速度 重复定义 需要删除
            self.data_window.lineEdit_Eff_18.setText(
                f'{data_list.alpha2i[self.current_z][self.current_zr]:.2f}')  # 绝对速度方向角 动叶出口绝对方向角
            self.data_window.lineEdit_faiz_8.setText(
                f'{data_list.Beta2i[self.current_z][self.current_zr]:.2f}')  # 动叶出口气流角
            self.data_window.lineEdit_rouz_8.setText(f'{data_list.Tt2[self.current_z]:.2f}')  # 气体总温
            self.data_window.lineEdit_taoz_8.setText(f'{data_list.T2i[self.current_z][self.current_zr]:.2f}')  # 气体静温
            self.data_window.lineEdit_fRz_z_8.setText(
                f'{data_list.Ma_c2i[self.current_z][self.current_zr]:.4f}')  # 绝对速度马赫数
            self.data_window.lineEdit_Maz_18.setText(
                f'{data_list.pt2i[self.current_z][self.current_zr] / 1000:.2f}')  # 出口绝对总压
            self.data_window.lineEdit_pt0_8.setText(
                f'{data_list.p2i[self.current_z][self.current_zr] / 1000:.2f}')  # 出口绝对静压
            self.data_window.lineEdit_alph2z_18.setText(
                f'{data_list.Radial_omega[self.current_z][self.current_zr]:.2g}')  # 反动度

            self.data_window.lineEdit_Eff_25.setText(
                f'{data_list.Rotor_Beta1_g[self.current_z][self.current_zr]}')  # 动叶进口几何角
            self.data_window.lineEdit_k_11.setText(
                f'{data_list.Rotor_Beta2_g[self.current_z][self.current_zr]}')  # 动叶出口几何角
            self.data_window.lineEdit_omaga_15.setText(
                f'{data_list.Rotor_Gamma[self.current_z][self.current_zr]}')  # 动叶安装角
            self.data_window.lineEdit_alph2z_22.setText(
                f'{data_list.Rotor_Cmax[self.current_z][self.current_zr] * 1000}')  # 动叶最大厚度
            self.data_window.lineEdit_faiz_11.setText(
                f'{data_list.Rotor_r1[self.current_z][self.current_zr] * 1000}')  # 动叶前缘半径
            self.data_window.lineEdit_taoz_11.setText(
                f'{data_list.Rotor_r2[self.current_z][self.current_zr] * 1000}')  # 动叶尾缘半径
            self.data_window.lineEdit_Maz_24.setText(
                f'{data_list.Rotor_t[self.current_z][self.current_zr] * 1000}')  # 动叶节距
            self.data_window.lineEdit_alph2z_23.setText(
                f'{data_list.Rotor_z[self.current_z][self.current_zr]}')  # 动叶叶片数
            self.data_window.lineEdit_taoz_14.setText(
                f'{data_list.Rotor_B[self.current_z][self.current_zr] * 1000}')  # 动叶叶宽
        self.data_window.lineEdit_Eff_26.setText(
            f'{data_list.Stator_Beta1_g[self.current_z][self.current_zr]}')  # 静叶进口几何角
        self.data_window.lineEdit_k_12.setText(
            f'{data_list.Stator_Beta2_g[self.current_z][self.current_zr]}')  # 静叶出口几何角
        self.data_window.lineEdit_omaga_16.setText(
            f'{data_list.Stator_Gamma[self.current_z][self.current_zr]}')  # 静叶安装角
        self.data_window.lineEdit_alph2z_24.setText(
            f'{data_list.Stator_Cmax[self.current_z][self.current_zr] * 1000}')  # 静叶最大厚度
        self.data_window.lineEdit_faiz_12.setText(
            f'{data_list.Stator_r1[self.current_z][self.current_zr] * 1000}')  # 静叶前缘半径
        self.data_window.lineEdit_taoz_12.setText(
            f'{data_list.Stator_r2[self.current_z][self.current_zr] * 1000}')  # 静叶尾缘半径
        self.data_window.lineEdit_Maz_25.setText(
            f'{data_list.Stator_t[self.current_z][self.current_zr] * 1000}')  # 静叶节距
        self.data_window.lineEdit_alph2z_25.setText(f'{data_list.Stator_z[self.current_z][self.current_zr]}')  # 静叶叶片数
        self.data_window.lineEdit_taoz_13.setText(
            f'{data_list.Stator_B[self.current_z][self.current_zr] * 1000}')  # 静叶叶宽

        tmp = '静叶' if self.turbine.current_opt == 0 else '动叶'
        tmp = f'当前参数为第{self.current_z + 1}级' + tmp + f'第{self.current_zr + 1}计算站'
        self.data_window.label.setText(tmp)

    def show_cascade_thickness(self):
        # blade_dis = 2 * math.pi * 190 / 90
        blade_dis = figure_operation.blade_dis
        re_s2 = copy.deepcopy(figure_operation.re_s)
        #     # 向上移动blade_dis距离
        for i in range(len(re_s2)):
            if self.turbine.current_opt == 1:
                re_s2[i, 1] = re_s2[i, 1] - blade_dis
            else:
                re_s2[i, 1] = re_s2[i, 1] + blade_dis

        re_p2 = copy.deepcopy(figure_operation.re_p)
        for i in range(len(re_p2)):
            if self.turbine.current_opt == 1:
                re_p2[i, 1] = re_p2[i, 1] - blade_dis
            else:
                re_p2[i, 1] = re_p2[i, 1] + blade_dis
        calcu.plot_cascade_thickness(blade_dis, figure_operation.re_p, figure_operation.re_s, re_p2, re_s2,
                                     self.turbine.current_z, self.turbine.current_zr, self.turbine.current_opt)

    def combo_init(self, z, zr):
        if z == zr == -1:
            self.comboBox_leixing.setEnabled(False)  # 下拉框禁用
            self.comboBox_jishu.setEnabled(False)
            self.comboBox_jisuanzhan.setEnabled(False)
        else:
            Z = []
            for i in range(2, z + 1):
                Z.append(str(i))

            Zr = []
            for i in range(2, zr + 1):
                Zr.append(str(i))

            self.comboBox_leixing.addItems(["动叶"])
            self.comboBox_jishu.addItems(Z)
            self.comboBox_jisuanzhan.addItems(Zr)

    def feed_back_to_figure_and_camber(self, z, zr, opt):
        camber_operation.control_point = copy.deepcopy(self.all_blade[z][zr][opt][0])
        figure_operation.TE_radius = self.all_blade[z][zr][opt][2][1]
        figure_operation.blade_dis = self.all_blade[z][zr][opt][3]
        figure_operation.lim = self.all_blade[z][zr][opt][0][2, 0] / 20  # 最后一个控制点的x轴就是叶片宽度
        camber_operation.lim = self.all_blade[z][zr][opt][0][2, 0] / 20
        # self.show_camber()
        # figure_operation.auto_plot(self.two_d_Figure, self.ax2d, self.all_pp_distance[z][zr][opt],
        #                            self.all_ps_distance[z][zr][opt])
        # 不能用上面这种方式重新调用auto_plot，因为多次调用函数会造成在同一个图窗上薛定谔的存在很多个图窗，当拖动的时候，可能会有瞬时出现当前点坐标显示错误问题
        camber_operation.camber = camber_operation.controlpoint2line()
        camber_operation.x_lim_max, camber_operation.y_lim_max = calcu.get_max_range(camber_operation.camber,
                                                                                     camber_operation.control_point)
        camber_operation.x_lim_all = camber_operation.x_lim_max
        camber_operation.y_lim_all = camber_operation.y_lim_max
        camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)

        figure_operation.pp, figure_operation.slope_p = figure_operation.get_origin_control_point(
            figure_operation.num_p, False, self.all_pp_distance[z][zr][opt])
        figure_operation.ps, figure_operation.slope_s = figure_operation.get_origin_control_point(
            figure_operation.num_s, True, self.all_ps_distance[z][zr][opt])

        figure_operation.re_p = calcu.bezier_curve(figure_operation.pp, figure_operation.npoint - 1)
        xp = np.concatenate(([figure_operation.pp[0, 0]], figure_operation.re_p[:, 0]))
        yp = np.concatenate(([figure_operation.pp[0, 1]], figure_operation.re_p[:, 1]))
        figure_operation.re_p = np.column_stack((xp, yp))

        figure_operation.re_s = calcu.bezier_curve(figure_operation.ps, figure_operation.npoint - 1)
        xs = np.concatenate(([figure_operation.ps[0, 0]], figure_operation.re_s[:, 0]))
        ys = np.concatenate(([figure_operation.ps[0, 1]], figure_operation.re_s[:, 1]))
        figure_operation.re_s = np.column_stack((xs, ys))

        figure_operation.c21, figure_operation.c22 = circle.circle(8, figure_operation.pp[-1],
                                                                   figure_operation.ps[-1], 20,
                                                                   figure_operation.re_p[-2])
        figure_operation.c21 = figure_operation.c21[::-1]
        figure_operation.c22 = figure_operation.c22[::-1]
        figure_operation.c21 = np.delete(figure_operation.c21, 0, 0)
        figure_operation.c22 = np.delete(figure_operation.c22, 0, 0)

        # 都是先加尾缘再算中弧线
        figure_operation.re_p = np.concatenate([figure_operation.re_p, figure_operation.c21], axis=0)
        figure_operation.re_s = np.concatenate([figure_operation.re_s, figure_operation.c22], axis=0)

        if self.ready_flag is True:  # 刚开始所有叶片过一遍不需要这些
            figure_operation.x_lim_max, figure_operation.y_lim_max = calcu.get_max_range(figure_operation.re_p,
                                                                                         figure_operation.re_s,
                                                                                         figure_operation.pp,
                                                                                         figure_operation.ps)
            figure_operation.x_lim_all = figure_operation.x_lim_max
            figure_operation.y_lim_all = figure_operation.y_lim_max

            figure_operation.meanline = calcu.binary_meanline(
                calcu.distance(figure_operation.pp[0, 0], figure_operation.pp[0, 1], figure_operation.pp[-1, 0],
                               figure_operation.pp[-1, 1]), figure_operation.re_p, figure_operation.re_s)
            figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)

            if z != self.last_z or opt != self.last_opt or self.type == 1:  # 改到其他叶片才需要重画3d
                self.show_3d()
                if data_list.blade_layout_method == 0:
                    if self.current_opt == 1:
                        ym = data_list.YM[self.current_z]
                    else:
                        ym = 0
                elif data_list.blade_layout_method == 1:
                    ym = data_list.YM[self.current_z]  # 通流部分扩张角

                x1, y1 = file_operation.intersection([(self.all_blade[z][zr][opt][0][2, 0] -
                                                       self.all_blade[z][zr][opt][0][0, 0]),
                                                      self.all_blade[z][zr][opt][1][0]],
                                                     -math.tan(ym / 180 * math.pi),
                                                     [[0, -100], [0, 100]])
                x2, y2 = file_operation.intersection([(self.all_blade[z][zr][opt][0][2, 0] -
                                                       self.all_blade[z][zr][opt][0][0, 0]),
                                                      self.all_blade[z][zr][opt][1][1]],
                                                     math.tan(ym / 180 * math.pi),
                                                     [[0, -100], [0, 100]])
                control_pp = np.array([[x1, y1],
                                       [(self.all_blade[z][zr][opt][0][2, 0] - self.all_blade[z][zr][opt][0][0, 0]),
                                        self.all_blade[z][zr][opt][1][0]]])
                control_ps = np.array([[x2, y2],
                                       [(self.all_blade[z][zr][opt][0][2, 0] - self.all_blade[z][zr][opt][0][0, 0]),
                                        self.all_blade[z][zr][opt][1][1]]])
                hub_shroud_operation.pp = control_pp
                hub_shroud_operation.ps = control_ps

                hub_shroud_operation.shroud = calcu.bezier_curve(hub_shroud_operation.pp,
                                                                 hub_shroud_operation.npoint - 1)
                xp = np.concatenate(([hub_shroud_operation.pp[0, 0]], hub_shroud_operation.shroud[:, 0]))
                yp = np.concatenate(([hub_shroud_operation.pp[0, 1]], hub_shroud_operation.shroud[:, 1]))
                hub_shroud_operation.shroud = np.column_stack((xp, yp))

                hub_shroud_operation.hub = calcu.bezier_curve(hub_shroud_operation.ps, hub_shroud_operation.npoint - 1)
                xs = np.concatenate(([hub_shroud_operation.ps[0, 0]], hub_shroud_operation.hub[:, 0]))
                ys = np.concatenate(([hub_shroud_operation.ps[0, 1]], hub_shroud_operation.hub[:, 1]))
                hub_shroud_operation.hub = np.column_stack((xs, ys))

                hub_shroud_operation.x_lim_max, hub_shroud_operation.y_lim_max = calcu.get_max_range(
                    hub_shroud_operation.shroud, hub_shroud_operation.hub, hub_shroud_operation.pp,
                    hub_shroud_operation.ps)
                hub_shroud_operation.x_lim_all = hub_shroud_operation.x_lim_max
                hub_shroud_operation.y_lim_all = hub_shroud_operation.y_lim_max
                hub_shroud_operation.opt_plot(self.cp_cnt, self.hubshroud_Figure, self.ax_hubshroud)

    def upload_change(self):
        # 保存当前叶片数据
        # 放到确定修改按钮中
        self.all_pp_distance[self.current_z][self.current_zr][
            self.turbine.current_opt if self.type == 2 else 0] = Slope.r_distance(
            camber_operation.camber, figure_operation.pp[1:], figure_operation.TE_radius)
        self.all_ps_distance[self.current_z][self.current_zr][
            self.turbine.current_opt if self.type == 2 else 0] = Slope.r_distance(
            camber_operation.camber, figure_operation.ps[1:], figure_operation.TE_radius)
        if self.turbine.current_opt == 0:
            if camber_operation.control_point[0, 0] != 0 or camber_operation.control_point[0, 1] != 0:
                base_point = copy.deepcopy(camber_operation.control_point[0])
                for i in range(3):
                    camber_operation.control_point[i][0] = camber_operation.control_point[i][0] - base_point[0]
                    camber_operation.control_point[i][1] = camber_operation.control_point[i][1] - base_point[1]

            data_list.Stator_Beta1_g[self.current_z][self.current_zr], data_list.Stator_Beta2_g[self.current_z][
                self.current_zr], data_list.Stator_Gamma[self.current_z][self.current_zr] = calcu.cp_to_angle(
                camber_operation.control_point)
            data_list.Stator_B[self.current_z][self.current_zr] = camber_operation.control_point[2, 0] - \
                                                                  camber_operation.control_point[0, 0]
        else:  # 动叶
            tmp = calcu.get_centerpoint(
                np.vstack((figure_operation.re_p, figure_operation.re_s[-2::-1, :])))
            central_point_x = tmp.x
            central_point_y = tmp.y
            for i in range(3):
                camber_operation.control_point[i][0] = camber_operation.control_point[i][0] - central_point_x
                camber_operation.control_point[i][1] = camber_operation.control_point[i][1] - central_point_y

            data_list.Rotor_Beta1_g[self.current_z][self.current_zr], data_list.Rotor_Beta2_g[self.current_z][
                self.current_zr], data_list.Rotor_Gamma[self.current_z][self.current_zr] = calcu.cp_to_angle(
                camber_operation.control_point)
            data_list.Rotor_B[self.current_z][self.current_zr] = camber_operation.control_point[2, 0] - \
                                                                 camber_operation.control_point[0, 0]
        for i in range(3):
            self.all_blade[self.turbine.current_z][self.turbine.current_zr][
                self.turbine.current_opt if self.type == 2 else 0][0][
                i] = copy.deepcopy(
                camber_operation.control_point[i])

    def on_combo_change(self, z=None, zr=None, opt=None):
        # if self.ready_flag is True: # 当时加这句的目的忘了 但加了这句，从工况开始的叶片无法初始化平移
        self.upload_change()
        if z is None or zr is None or opt is None:
            if self.comboBox_leixing.currentText() == '静叶':
                opt = 0
            else:
                opt = 1
            z = int(self.comboBox_jishu.currentText()) - 1
            zr = int(self.comboBox_jisuanzhan.currentText()) - 1
        if self.last_opt != opt and self.type == 1:  # 单个叶片只更换积叠规律
            if opt == 1:
                for j in range(data_list.Zr):
                    rep, res = self.get_rep_and_res_from_cp(self.current_z, j, 0)
                    tmp = calcu.get_centerpoint(np.vstack((rep, res[-2::-1, :])))
                    central_point_x = tmp.x
                    central_point_y = tmp.y
                    for i in range(3):
                        self.all_blade[0][j][0][0][i][0] = self.all_blade[0][j][0][0][i][0] - central_point_x
                        self.all_blade[0][j][0][0][i][1] = self.all_blade[0][j][0][0][i][1] - central_point_y
            else:
                for j in range(data_list.Zr):
                    base_point = copy.deepcopy(self.all_blade[0][j][0][0][0])
                    for i in range(3):
                        self.all_blade[0][j][0][0][i][0] = self.all_blade[0][j][0][0][i][0] - base_point[0]
                        self.all_blade[0][j][0][0][i][1] = self.all_blade[0][j][0][0][i][1] - base_point[1]

        self.current_z = z
        self.current_zr = zr
        self.current_opt = opt
        self.turbine.current_z = z
        self.turbine.current_zr = zr
        self.turbine.current_opt = opt
        self.feed_back_to_figure_and_camber(z, zr, opt if self.type == 2 else 0)
        self.last_opt = opt
        self.last_z = z

    def confirm_change(self):
        self.last_z = -1
        self.last_opt = -1  # 改变上个叶片数据才能改变3d图像
        self.on_combo_change(self.turbine.current_z, self.turbine.current_zr, self.turbine.current_opt)
        self.last_z = self.current_z
        self.last_opt = self.turbine.current_opt

    def show_about(self):
        QMessageBox.about(self, '关于', 'HTDO 1.0\n作者GitHub: tian1wang')

    def save_txt(self):
        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/", 'txt(*.txt)')
        if filepath != '':
            if self.type == 1:
                pp_init = Slope.r_distance(camber_operation.camber, figure_operation.pp[1:], figure_operation.TE_radius)
                ps_init = Slope.r_distance(camber_operation.camber, figure_operation.ps[1:], figure_operation.TE_radius)
                file_operation.txtoutput(filepath, camber_operation.control_point, pp_init, ps_init, False)
            else:
                file_operation.txtoutput(filepath, self.all_blade, self.all_pp_distance,
                                         self.all_ps_distance, True)
            self.info.setText('成功保存为txt格式')
        else:
            self.info.setText('文件名不能为空，请重新输入文件名')

    def show_meridional(self):
        self.output(mode='calcu')
        fig_name = f'透平子午线'
        fig = plt.figure(fig_name)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('轴向/m', fontdict={'fontfamily': 'SimSun'})
        ax.set_ylabel('径向/m', fontdict={'fontfamily': 'SimSun'})
        tmpx = []
        tmpy = []
        for i in range(len(self.turbine.meridional['hub'])):
            for j in range(len(self.turbine.meridional['hub'][i])):
                tmpx.append(self.turbine.meridional['hub'][i][j][0])
                tmpy.append(self.turbine.meridional['hub'][i][j][1])
        ax.plot(tmpx, tmpy)
        tmpx = []
        tmpy = []
        for i in range(len(self.turbine.meridional['shroud'])):
            for j in range(len(self.turbine.meridional['shroud'][i])):
                tmpx.append(self.turbine.meridional['shroud'][i][j][0])
                tmpy.append(self.turbine.meridional['shroud'][i][j][1])
        ax.plot(tmpx, tmpy)

        for i in range(len(self.turbine.blade_position)):
            tmpx = []
            tmpy = []
            # 叶片 前/尾 下/上 x/y
            tmpx.append(self.turbine.blade_position[i][0][0][0])
            tmpx.append(self.turbine.blade_position[i][1][0][0])
            tmpx.append(self.turbine.blade_position[i][1][1][0])
            tmpx.append(self.turbine.blade_position[i][0][1][0])
            tmpx.append(self.turbine.blade_position[i][0][0][0])
            tmpy.append(self.turbine.blade_position[i][0][0][1])
            tmpy.append(self.turbine.blade_position[i][1][0][1])
            tmpy.append(self.turbine.blade_position[i][1][1][1])
            tmpy.append(self.turbine.blade_position[i][0][1][1])
            tmpy.append(self.turbine.blade_position[i][0][0][1])
            label = ('N' if i % 2 == 0 else 'R') + f'{i // 2 + 1}'
            ax.plot(tmpx, tmpy)
            ax.fill(tmpx, tmpy, alpha=0.3, label=label)
        # 入口长度标记
        x1 = self.turbine.meridional['hub'][0][0][0]
        y1 = self.turbine.meridional['hub'][0][0][1]
        x2 = self.turbine.meridional['shroud'][0][0][0]
        y2 = self.turbine.meridional['shroud'][0][0][1]
        ax.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle="<->"))
        ax.annotate(f'{calcu.distance(x1, y1, x2, y2):.3g}m', xy=((x1 + x2) / 2, (y1 + y2) / 2), xytext=(2, -2),
                    textcoords="offset points", ha="left")
        # 通流长度标记
        x1 = self.turbine.blade_position[0][0][0][0]
        x2 = self.turbine.blade_position[-1][1][0][0]
        h = self.turbine.blade_position[-1][1][1][1] - self.turbine.blade_position[-1][1][0][1]
        y2 = self.turbine.blade_position[-1][1][0][1] - 0.17 * h
        y1 = y2
        ax.plot([x1, x1], [self.turbine.blade_position[0][0][0][1], y1], color='black')
        ax.plot([x2, x2], [self.turbine.blade_position[-1][1][0][1], y2], color='black')
        y2 = y2 + 0.04 * h
        y1 = y2
        ax.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle="<->"))
        ax.annotate(f'{calcu.distance(x1, y1, x2, y2):.3g}m', xy=((x1 + x2) / 2, (y1 + y2) / 2), xytext=(-10, 0),
                    textcoords="offset points", va="bottom")

        if data_list.blade_layout_method == 0:
            x2 = (self.turbine.meridional['hub'][0][0][0] + self.turbine.meridional['hub'][0][-1][0]) / 2
            y2 = data_list.Dm1M[0] / 2
            x1 = x2
            y1 = y2 - 0.7 * h
            phy = data_list.Dm1M[0]  # 中径
        elif data_list.blade_layout_method == 1:
            x2 = (self.turbine.meridional['hub'][0][0][0] + self.turbine.meridional['hub'][0][-1][0]) / 2
            y2 = self.turbine.meridional['hub'][0][0][1]
            x1 = x2
            y1 = y2 - 0.3 * h
            phy = data_list.Dh1M[0]  # 内径
            print(x1, y1, x2, y2, phy)
        ax.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle="<-"))
        ax.annotate(f'Φ{phy:.3g}m', xy=((x1 + x2) / 2, (y1 + y2) / 2), xytext=(0, 0),
                    textcoords="offset points", ha="right")
        ax.legend()
        ax.axis('square')
        plt.show()

    def output(self, mode):
        # mode等于calcu时，是单纯计算子午线，其他时候是输出
        if mode != 'calcu':
            filepath, type = QFileDialog.getSaveFileName(self, "文件导出", "/", 'geomTurbo(*.geomTurbo)')
        else:
            filepath = 'https://github.com/tian1wang'
            file_operation.output_ready_flag = False

        if filepath != '':
            if self.type == 1:
                if data_list.Zr == 1:
                    file_operation.geomturbo_output(figure_operation.re_p, figure_operation.re_s, [190, 211.83],
                                                    filepath)
                    self.info.setText('成功导出为geomTurbo格式')
                else:
                    re_p = []
                    re_s = []
                    for j in range(len(self.all_blade[0])):
                        tmp_re_p, tmp_re_s = self.get_rep_and_res_from_cp(0, j, 0)
                        re_p.append(copy.deepcopy(tmp_re_p))
                        re_s.append(copy.deepcopy(tmp_re_s))
                    file_operation.geomturbo_output(re_p, re_s, self.all_blade[0][0][0][1], filepath,
                                                    self.all_blade[0][0][0][0][2, 0], 0, 0)
                QMessageBox.information(self, '导出成功', f'导出成功，路径为{filepath}')
            else:
                offset = 0
                last_b = 0
                hub = []
                shroud = []
                last_TE = []
                self.turbine.blade_position = []
                for i in range(data_list.Z_num):  # 级数
                    if i > 0:
                        offset = offset + 1.5 * data_list.ACM[i - 1]
                    for k in range(2):  # 静叶 动叶
                        if k == 1:
                            offset = offset + data_list.ACM[i] - self.all_blade[i][0][k][0][0, 0]
                        offset = offset + last_b
                        re_p = []
                        re_s = []
                        for j in range(len(self.all_blade[i])):
                            tmp_re_p, tmp_re_s = self.get_rep_and_res_from_cp(i, j, k)
                            re_p.append(copy.deepcopy(tmp_re_p))
                            re_s.append(copy.deepcopy(tmp_re_s))

                        if data_list.blade_layout_method == 0:
                            if self.current_opt == 1:
                                ym = data_list.YM[self.current_z]
                            else:
                                ym = 0
                        elif data_list.blade_layout_method == 1:
                            ym = data_list.YM[self.current_z]  # 通流部分扩张角

                        tmp_hub, tmp_shroud = file_operation.geomturbo_output(re_p, re_s, self.all_blade[i][0][k][1],
                                                                              filepath[:-10] + (
                                                                                  f'_s{i + 1}' if k == 0 else f'_r{i + 1}') + '.geomTurbo',
                                                                              self.all_blade[i][0][k][0][2, 0],
                                                                              offset, ym, last_TE,
                                                                              data_list.Stator_z[i][0] if k == 0 else
                                                                              data_list.Rotor_z[i][0])
                        last_b = self.all_blade[i][round(len(self.all_blade[i]) / 2.0)][k][0][2, 0]
                        last_TE = [[self.all_blade[i][0][k][0][2, 0] + offset, self.all_blade[i][0][k][1][0]],
                                   [self.all_blade[i][-1][k][0][2, 0] + offset, self.all_blade[i][-1][k][1][1]]]
                        le = [[self.all_blade[i][0][k][0][0, 0] + offset, self.all_blade[i][0][k][1][0]],
                              [self.all_blade[i][-1][k][0][0, 0] + offset, self.all_blade[i][-1][k][1][1]]]
                        self.turbine.blade_position.append([le, last_TE])
                        tmp_hub[1].append(last_TE[0])  # 保证连续性
                        tmp_shroud[1].append(last_TE[1])
                        hub.append(tmp_hub[0])
                        hub.append(tmp_hub[1])
                        shroud.append(tmp_shroud[0])
                        shroud.append(tmp_shroud[1])
                end = last_TE[0][0] if last_TE[0][0] > last_TE[1][0] else last_TE[1][0]
                end = end + 2 * last_b
                end_interval = (end - last_TE[0][0]) / 20
                end_series = []
                for i in range(21):
                    end_series.append([last_TE[0][0] + i * end_interval, last_TE[0][1]])
                hub.append(end_series)
                end_interval = (end - last_TE[1][0]) / 20
                end_series = []
                for i in range(21):
                    end_series.append([last_TE[1][0] + i * end_interval, last_TE[1][1]])
                shroud.append(end_series)
                file_series = []
                for i in range(data_list.Z_num):
                    for k in range(2):
                        file = filepath[:-10] + (f'_s{i + 1}' if k == 0 else f'_r{i + 1}') + '.geomTurbo'
                        file_operation.print_all_meridional(hub, shroud, file)
                        file_series.append(file)
                if mode != 'calcu':
                    QMessageBox.information(self, '导出成功', f'导出成功，路径为{file_series}')
                self.turbine.meridional = {'hub': hub, 'shroud': shroud}
        else:
            self.info.setText('文件名不能为空，请重新输入文件名')
        if mode == 'calcu':
            file_operation.output_ready_flag = True

    def undo(self):
        if figure_operation.back_up_now_pos > 0:
            # 执行撤销操作之前需要保存当前点，这样才能实现重做
            figure_operation.back_up_now_pos = figure_operation.back_up_now_pos - 1
            tmp_opt = figure_operation.back_up_series[figure_operation.back_up_now_pos]
            length = len(tmp_opt)
            save_opt = []
            if length == 4:  # 是截面图 [flag, ind, x_back_up, y_back_up]
                if tmp_opt[0] == 0:  # 改pp
                    # 保存当前点
                    save_opt = [tmp_opt[0], tmp_opt[1], figure_operation.pp[tmp_opt[1], 0],
                                figure_operation.pp[tmp_opt[1], 1]]
                    figure_operation.pp[tmp_opt[1], 0] = tmp_opt[2]
                    figure_operation.pp[tmp_opt[1], 1] = tmp_opt[3]
                    figure_operation.controlpoint2line(False)
                else:  # 改ps
                    save_opt = [tmp_opt[0], tmp_opt[1], figure_operation.ps[tmp_opt[1], 0],
                                figure_operation.ps[tmp_opt[1], 1]]
                    figure_operation.ps[tmp_opt[1], 0] = tmp_opt[2]
                    figure_operation.ps[tmp_opt[1], 1] = tmp_opt[3]
                    figure_operation.controlpoint2line(True)
                figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
            else:  # 是中弧线图 [ind, x_back_up, y_back_up]
                save_opt = [tmp_opt[0], camber_operation.control_point[tmp_opt[0], 0],
                            camber_operation.control_point[tmp_opt[0], 1]]
                camber_operation.control_point[tmp_opt[0], 0] = tmp_opt[1]
                camber_operation.control_point[tmp_opt[0], 1] = tmp_opt[2]
                last_camber = copy.deepcopy(camber_operation.camber)
                camber_operation.camber = camber_operation.controlpoint2line()
                camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)
                camber_operation.sym_figure(last_camber)

            if len(figure_operation.back_up_series) <= figure_operation.back_up_now_pos + 1:
                figure_operation.back_up_series.append(save_opt)
            else:
                figure_operation.back_up_series[figure_operation.back_up_now_pos + 1] = save_opt

            self.info.setText('撤销成功')
        else:
            self.info.setText('无前置操作，无法撤销')

    def remake(self):
        if figure_operation.back_up_now_pos < len(figure_operation.back_up_series) - 1:
            figure_operation.back_up_now_pos = figure_operation.back_up_now_pos + 1
            tmp_opt = figure_operation.back_up_series[figure_operation.back_up_now_pos]
            length = len(tmp_opt)
            if length == 4:  # 是截面图 [flag, ind, x_back_up, y_back_up]
                if tmp_opt[0] == 0:  # 改pp
                    figure_operation.pp[tmp_opt[1], 0] = tmp_opt[2]
                    figure_operation.pp[tmp_opt[1], 1] = tmp_opt[3]
                    figure_operation.controlpoint2line(False)
                else:  # 改ps
                    figure_operation.ps[tmp_opt[1], 0] = tmp_opt[2]
                    figure_operation.ps[tmp_opt[1], 1] = tmp_opt[3]
                    figure_operation.controlpoint2line(True)
                figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
            else:  # 是中弧线图 [ind, x_back_up, y_back_up]
                camber_operation.control_point[tmp_opt[0], 0] = tmp_opt[1]
                camber_operation.control_point[tmp_opt[0], 1] = tmp_opt[2]
                last_camber = camber_operation.camber
                camber_operation.camber = camber_operation.controlpoint2line()
                camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)
                camber_operation.sym_figure(last_camber)
            self.info.setText('重做成功')
        else:
            self.info.setText('无后置操作，无法重做')

    def show_coordinate(self):
        if figure_operation.x_mouse is not None and figure_operation.y_mouse is not None:
            self.info.setText(f'截面图: {figure_operation.x_mouse:.3f},{figure_operation.y_mouse:.3f}')
        elif camber_operation.x_mouse is not None and camber_operation.y_mouse is not None:
            self.info.setText(f'弧度曲线: {camber_operation.x_mouse:.3f},{camber_operation.y_mouse:.3f}')
        elif hub_shroud_operation.x_mouse is not None and hub_shroud_operation.y_mouse is not None:
            self.info.setText(f'弧度曲线: {hub_shroud_operation.x_mouse:.3f},{hub_shroud_operation.y_mouse:.3f}')
        elif plot_3d.flag is True:
            self.info.setText('三维图像')
            # else:
            #     self.info.setText('')

    def show_hubshroud(self):
        if self.type == 1:
            hub_shroud_operation.auto_plot(self.hubshroud_Figure, self.ax_hubshroud)
        else:
            z = int(self.comboBox_jishu.currentText()) - 1
            zr = int(self.comboBox_jisuanzhan.currentText()) - 1
            if self.comboBox_leixing.currentText() == '静叶':
                opt = 0
            else:
                opt = 1

            if data_list.blade_layout_method == 0:
                if self.current_opt == 1:
                    ym = data_list.YM[self.current_z]
                else:
                    ym = 0
            elif data_list.blade_layout_method == 1:
                ym = data_list.YM[self.current_z]  # 通流部分扩张角

            x1, y1 = file_operation.intersection([(self.all_blade[z][zr][opt][0][2, 0] -
                                                   self.all_blade[z][zr][opt][0][0, 0]),
                                                  self.all_blade[z][zr][opt][1][0]],
                                                 -math.tan(ym / 180 * math.pi), [[0, -100], [0, 100]])
            x2, y2 = file_operation.intersection([(self.all_blade[z][zr][opt][0][2, 0] -
                                                   self.all_blade[z][zr][opt][0][0, 0]),
                                                  self.all_blade[z][zr][opt][1][1]],
                                                 math.tan(ym / 180 * math.pi), [[0, -100], [0, 100]])
            hub_shroud_operation.auto_plot(self.hubshroud_Figure, self.ax_hubshroud,
                                           np.array([[x1, y1],
                                                     [(self.all_blade[z][zr][opt][0][2, 0] -
                                                       self.all_blade[z][zr][opt][0][0, 0]),
                                                      self.all_blade[z][zr][opt][1][0]]]),
                                           np.array([[x2, y2],
                                                     [(self.all_blade[z][zr][opt][0][2, 0] -
                                                       self.all_blade[z][zr][opt][0][0, 0]),
                                                      self.all_blade[z][zr][opt][1][1]]])
                                           )

    def show_2d_plot(self, init_pp, init_ps):
        figure_operation.auto_plot(self.two_d_Figure, self.ax2d, init_pp, init_ps)
        # print(figure_operation.re_p, figure_operation.re_s)

    def show_3d(self):
        # 每次点击计算都重新计算，虽然时间慢一点，但不需要空间
        # 叶片数据只有这里用得到，为了这一个地方存一次不值得
        # 而且直接计算写代码更简单
        if self.type == 1 and data_list.Zr == 1:
            plot_3d.plot_3d(np.vstack((figure_operation.re_p, figure_operation.re_s[-2::-1, :])), 10,
                            self.three_d_Figure,
                            self.ax3d, np.array([[0, 0], [5, -2], [10, 0]]), False)
            # , np.array([[0, 0], [5, -2], [10, 0]])
        else:
            all_yexing = []
            for i in range(len(self.all_blade[self.current_z])):
                tmp_re_p, tmp_re_s = self.get_rep_and_res_from_cp(self.current_z, i,
                                                                  self.current_opt if self.type == 2 else 0)
                yexing = copy.deepcopy(np.vstack((tmp_re_p, tmp_re_s[-2::-1, :])))
                all_yexing.append(yexing)
            if self.current_opt == 0:
                plot_3d.plot_3d(all_yexing, 10, self.three_d_Figure, self.ax3d, data_list.stacking_line[self.current_z],
                                True)
            if self.current_opt == 1:
                plot_3d.plot_3d(all_yexing, 10, self.three_d_Figure, self.ax3d, np.array(
                    [[self.all_blade[self.current_z][0][1][1][0], 0],
                     [(self.all_blade[self.current_z][0][1][1][0] + self.all_blade[self.current_z][0][1][1][1]) / 2, 0],
                     [self.all_blade[self.current_z][0][1][1][1], 0]]),
                                True)
        '''
            np.append()
            np.concatenate()
            np.stack()
            np.hstack()
            np.vstack()
            np.dstack()
            记得要多加一个括号
        '''

    def get_rep_and_res_from_cp(self, z, zr, opt):
        tmp_pp, waste = figure_operation.get_origin_control_point(figure_operation.num_p, False,
                                                                  self.all_pp_distance[z][zr][opt],
                                                                  self.all_blade[z][zr][opt][2][1], None,
                                                                  self.all_blade[z][zr][opt][0])
        tmp_ps, waste = figure_operation.get_origin_control_point(figure_operation.num_s, True,
                                                                  self.all_ps_distance[z][zr][opt],
                                                                  self.all_blade[z][zr][opt][2][1], None,
                                                                  self.all_blade[z][zr][opt][0])
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

    def show_camber(self):
        camber_operation.auto_plot(self.camber_Figure, self.ax_camber)

    def plot_resize(self):
        figure_operation.x_lim_all = figure_operation.x_lim_max
        figure_operation.y_lim_all = figure_operation.y_lim_max
        figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
        camber_operation.x_lim_all = camber_operation.x_lim_max
        camber_operation.y_lim_all = camber_operation.y_lim_max
        camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)

    def plot_square(self):
        self.square_cnt = self.square_cnt + 1
        if self.square_cnt > 1:
            self.square_cnt = 0
        pic_list = ['lashen_on.png', 'lashen_off.png']  # 这个需要改
        self.pushButton_square.setStyleSheet(f"border-image: url(:/source/{pic_list[self.square_cnt]});\n")
        figure_operation.square_switch = self.square_cnt
        camber_operation.square_switch = self.square_cnt
        # 懒得传参了，直接修改了全局变量
        figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
        camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)

    def camber_opt(self):
        self.camber_cnt = self.camber_cnt + 1
        if self.camber_cnt > 1:
            self.camber_cnt = 0
        pic_list = ['zhonghu_on.png', 'zhonghu_off.png']
        self.pushButton_zhonghu.setStyleSheet(f"border-image: url(:/source/{pic_list[self.camber_cnt]});\n")
        figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)

    def drag_opt(self):
        self.drag_cnt = self.drag_cnt + 1
        if self.drag_cnt > 1:
            self.drag_cnt = 0
        pic_list = ['drag_on.png', 'drag_off.png']
        self.pushButton_drag.setStyleSheet(f"border-image: url(:/source/{pic_list[self.drag_cnt]});\n")
        # figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
        figure_operation.drag_switch = self.drag_cnt
        camber_operation.drag_switch = self.drag_cnt

    def ctrl_point_opt(self):
        self.cp_cnt = self.cp_cnt + 1
        if self.cp_cnt > 1:
            self.cp_cnt = 0
        pic_list = ['control_on.png', 'control_off.png']
        self.pushButton_control.setStyleSheet(f"border-image: url(:/source/{pic_list[self.cp_cnt]});\n")
        figure_operation.opt_plot(self.camber_cnt, self.cp_cnt, self.two_d_Figure, self.ax2d)
        camber_operation.opt_plot(self.cp_cnt, self.camber_Figure, self.ax_camber)
