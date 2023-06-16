import copy

import numpy as np


class Section:

    def __init__(self, pcp, scp, ccp, le, te, t):
        self.p_control_point = copy.deepcopy(pcp)  # p控制点
        self.s_control_point = copy.deepcopy(scp)  # s控制点
        self.c_control_point = copy.deepcopy(ccp)  # 弧度曲线控制点
        self.le = le  # 前缘半径
        self.te = te  # 尾缘半径
        self.t = t  # 节距


class Blade:

    def __init__(self, zr, hub, shroud, theta, this_blade, this_pp_distance, this_ps_distance):
        self.zr = zr
        self.hub = hub  # 叶顶
        self.shroud = shroud  # 叶根
        self.theta = theta  # 扩张角
        self.sections = []  # 计算站
        self.stacking_line = []  # 积叠规律
        for i in range(self.zr):
            self.sections.append(
                Section(this_pp_distance[i], this_ps_distance[i], this_blade[i][0], this_blade[i][2][0],
                        this_blade[i][2][1], this_blade[i][3]))

    def add_section(self):
        self.zr = self.zr + 1


class Turbine:

    def __init__(self, z, zr, all_blade, all_pp_distance, all_ps_distance):
        self.z = 0
        self.meridional = None
        self.blade_position = []  # 两个前缘两个尾缘确定一个叶片
        self.blade = []
        self.current_z = 0
        self.current_zr = 0
        self.current_opt = 0
        for i in range(z):
            for k in range(len(all_pp_distance[i][0])):
                if k == 0:
                    theta = 0
                else:
                    theta = 8
                this_blade = []
                this_pp_distance = []
                this_ps_distance = []
                for j in range(zr):
                    this_blade.append(all_blade[i][j][k])
                    this_pp_distance.append(all_pp_distance[i][j][k])
                    this_ps_distance.append(all_ps_distance[i][j][k])
                self.blade.append(
                    Blade(zr, all_blade[i][0][k][1][0], all_blade[i][0][k][1][1], theta, this_blade, this_pp_distance,
                          this_ps_distance))
