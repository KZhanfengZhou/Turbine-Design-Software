from design_calculation import One_dimensional_Design_1xbz, Profile_2D_parameters, Radial_gas_parameter_distribution, \
    data_list
import matplotlib

matplotlib.use('Qt5Agg')

from ui import main_leaf
from ui.gongkuang_designed import Ui_gongkuang
from PyQt5 import QtWidgets
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')

from blade_geometry import figure_operation, camber_operation

import copy


class gongkuang(QtWidgets.QMainWindow, Ui_gongkuang):
    main = None

    Z = 0
    hs = 0
    all_blade = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.confirm)

    def confirm(self):
        self.working_condition_init()
        self.geom_blade_calcu()
        # 显示一级静叶的第一计算站 从前往后分别是：级数 计算站数 静叶/动叶 参数编号
        camber_operation.control_point = self.all_blade[0][0][0][0]
        figure_operation.TE_radius = self.all_blade[0][0][0][2][1]
        figure_operation.blade_dis = self.all_blade[0][0][0][3]
        figure_operation.lim = self.all_blade[0][0][0][0][2, 0] / 20
        camber_operation.lim = self.all_blade[0][0][0][0][2, 0] / 20
        for i in range(data_list.Z_num):
            for j in range(data_list.Zr):
                if self.all_blade[i][j][0][0][0, 0] != 0 or self.all_blade[i][j][0][0][0, 1] != 0:
                    base_point = copy.deepcopy(self.all_blade[i][j][0][0][0])
                    for k in range(3):
                        self.all_blade[i][j][0][0][k][0] = self.all_blade[i][j][0][0][k][0] - base_point[0]
                        self.all_blade[i][j][0][0][k][1] = self.all_blade[i][j][0][0][k][1] - base_point[1]
        self.main = main_leaf.blade_designer(2, self.all_blade)  # 从参数开始用1表示
        self.setVisible(False)  # 隐藏主界面
        self.main.setVisible(True)

    def geom_blade_calcu(self):
        One_dimensional_Design_1xbz.One_dimensional_design(self.Z, self.hs)
        for i in range(data_list.Z_num):
            Radial_gas_parameter_distribution.radial_gas_parameter_distribution(i)
        data_list.Beta2i = np.array(data_list.Beta2i)
        data_list.alpha1i = np.array(data_list.alpha1i)
        data_list.Beta1i = np.array(data_list.Beta1i)
        data_list.c1i = np.array(data_list.c1i)
        data_list.c2i = np.array(data_list.c2i)
        data_list.w1i = np.array(data_list.w1i)
        data_list.w2i = np.array(data_list.w2i)
        data_list.T1i = np.array(data_list.T1i)
        data_list.p1i = np.array(data_list.p1i)
        data_list.G1i = np.array(data_list.G1i)
        data_list.alpha2i = np.array(data_list.alpha2i)
        data_list.Tt2 = np.array(data_list.Tt2)
        data_list.T2i = np.array(data_list.T2i)
        data_list.Ma_c2i = np.array(data_list.Ma_c2i)
        data_list.p2i = np.array(data_list.p2i)
        data_list.pt2i = np.array(data_list.pt2i)
        data_list.Radial_omega = np.array(data_list.Radial_omega)

        for i in range(data_list.Z_num):
            i_stage = []
            for j in range(data_list.Zr):
                i_stage.append(Profile_2D_parameters.Profile_2d_parameters(i, j))
            self.all_blade.append(i_stage)

            data_list.Stator_Beta1_g.append(data_list.Stator_Beta1_g_tmp)
            data_list.Rotor_Beta1_g.append(data_list.Rotor_Beta1_g_tmp)
            data_list.Stator_Beta2_g.append(data_list.Stator_Beta2_g_tmp)
            data_list.Rotor_Beta2_g.append(data_list.Rotor_Beta2_g_tmp)
            data_list.Stator_Gamma.append(data_list.Stator_Gamma_tmp)
            data_list.Rotor_Gamma.append(data_list.Rotor_Gamma_tmp)
            data_list.Stator_Cmax.append(data_list.Stator_Cmax_tmp)
            data_list.Rotor_Cmax.append(data_list.Rotor_Cmax_tmp)
            data_list.Stator_r1.append(data_list.Stator_r1_tmp)
            data_list.Rotor_r1.append(data_list.Rotor_r1_tmp)
            data_list.Stator_r2.append(data_list.Stator_r2_tmp)
            data_list.Rotor_r2.append(data_list.Rotor_r2_tmp)
            data_list.Stator_t.append(data_list.Stator_t_tmp)
            data_list.Rotor_t.append(data_list.Rotor_t_tmp)
            data_list.Stator_z.append(data_list.Stator_z_tmp)
            data_list.Rotor_z.append(data_list.Rotor_z_tmp)
            data_list.Stator_B.append(data_list.Stator_B_tmp)
            data_list.Rotor_B.append(data_list.Rotor_B_tmp)

            data_list.Stator_Beta1_g_tmp = []
            data_list.Rotor_Beta1_g_tmp = []
            data_list.Stator_Beta2_g_tmp = []
            data_list.Rotor_Beta2_g_tmp = []
            data_list.Stator_Gamma_tmp = []
            data_list.Rotor_Gamma_tmp = []
            data_list.Stator_Cmax_tmp = []
            data_list.Rotor_Cmax_tmp = []
            data_list.Stator_r1_tmp = []
            data_list.Rotor_r1_tmp = []
            data_list.Stator_r2_tmp = []
            data_list.Rotor_r2_tmp = []
            data_list.Stator_t_tmp = []
            data_list.Rotor_t_tmp = []
            data_list.Stator_z_tmp = []
            data_list.Rotor_z_tmp = []
            data_list.Stator_B_tmp = []
            data_list.Rotor_B_tmp = []

        # data_list.Stator_Beta1_g = np.array(data_list.Stator_Beta1_g)
        # data_list.Rotor_Beta1_g = np.array(data_list.Rotor_Beta1_g)
        # data_list.Stator_Beta2_g = np.array(data_list.Stator_Beta2_g)
        # data_list.Rotor_Beta2_g = np.array(data_list.Rotor_Beta2_g)
        # data_list.Stator_Gamma = np.array(data_list.Stator_Gamma)
        # data_list.Rotor_Gamma = np.array(data_list.Rotor_Gamma)
        # data_list.Stator_Cmax = np.array(data_list.Stator_Cmax)
        # data_list.Rotor_Cmax = np.array(data_list.Rotor_Cmax)
        # data_list.Stator_r1 = np.array(data_list.Stator_r1)
        # data_list.Rotor_r1 = np.array(data_list.Rotor_r1)
        # data_list.Stator_r2 = np.array(data_list.Stator_r2)
        # data_list.Rotor_r2 = np.array(data_list.Rotor_r2)
        # data_list.Stator_t = np.array(data_list.Stator_t)
        # data_list.Rotor_t = np.array(data_list.Rotor_t)
        # data_list.Stator_z = np.array(data_list.Stator_z)
        # data_list.Rotor_z = np.array(data_list.Rotor_z)
        # data_list.Stator_B = np.array(data_list.Stator_B)
        # data_list.Rotor_B = np.array(data_list.Rotor_B)

    def working_condition_init(self):
        data_list.G = float(self.lineEdit_G.text())
        data_list.pt0 = float(self.lineEdit_pt0.text())
        data_list.Tt0 = float(self.lineEdit_Tt0.text())
        data_list.pz = float(self.lineEdit_pz.text())
        # data_list.Efft0 = float(self.lineEdit_Efft0.text())
        # data_list.Eff = float(self.lineEdit_Eff.text())
        data_list.Maz = float(self.lineEdit_Maz.text())
        data_list.n = float(self.lineEdit_n.text())
        data_list.k = float(self.lineEdit_k.text())
        data_list.R = float(self.lineEdit_R.text())
        data_list.omaga = float(self.lineEdit_omaga.text())
        data_list.xaz = float(self.lineEdit_xaz.text())
        # data_list.alph2z = float(self.lineEdit_alph2z.text())

        data_list.faiz = float(self.lineEdit_faiz.text())
        data_list.rouz = float(self.lineEdit_rouz.text())
        data_list.taoz = float(self.lineEdit_taoz.text())
        data_list.fRz_z = float(self.lineEdit_fRz_z.text())

        data_list.Ttic = float(self.lineEdit_Ttic.text())
        data_list.ptic = float(self.lineEdit_ptic.text())
        data_list.kic = float(self.lineEdit_kic.text())
        data_list.Ric = float(self.lineEdit_Ric.text())

        self.Z, self.hs = One_dimensional_Design_1xbz.get_blade_stage_num()
        data_list.Z_num = int(self.Z)
        # a = self.lineEdit_Gc.text()
        # data_list.Gc = np.array([float(tmp) for tmp in a.split(',')])
        a = self.lineEdit_Gc.text().split(',')
        tmp = []
        tmp.append(float(a[0]))
        for i in range(1, self.Z):
            tmp.append(float(a[1]))
        data_list.Gc = np.array(tmp)

        # a = self.lineEdit_crc.text()
        # data_list.crc = np.array([float(tmp) for tmp in a.split(',')])
        a = self.lineEdit_crc.text().split(',')
        tmp = []
        tmp.append(float(a[0]))
        for i in range(1, self.Z):
            tmp.append(float(a[1]))
        data_list.crc = np.array(tmp)

        Radial_gas_parameter_distribution.KG = float(self.lineEdit_KG.text())
        # Radial_gas_parameter_distribution.G = float(self.lineEdit_G_2.text())
        # Radial_gas_parameter_distribution.n = float(self.lineEdit_n_2.text())
        Radial_gas_parameter_distribution.Zr = int(self.lineEdit_Zr.text())
