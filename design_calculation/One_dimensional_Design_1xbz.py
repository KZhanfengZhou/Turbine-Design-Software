# One-dimensional Design 设计的第一步：一维设计程序，根据要求的进出口条件计算平均的气流参数
import math
import numpy as np

from design_calculation import data_list


# 删掉一个d表示已经改变

def get_blade_stage_num():
    h_ds = data_list.k / (data_list.k - 1) * data_list.R * data_list.Tt0 * (
            1 - (data_list.pz / data_list.pt0) ** ((data_list.k - 1) / data_list.k))  # 等熵焓降

    # 级数
    Z = 1  # 初始级数设定为1
    hs = h_ds / 1000  # 等熵焓降单位转换为kJ/kg
    while hs / Z > 220:  # 判断焓降是否过大
        Z = Z + 1
    # print('级数为%d级\n' % Z)
    return Z, hs


def One_dimensional_design(Z, hs):
    # 参数计算
    cp = data_list.k / (data_list.k - 1) * data_list.R  # 等压比热
    B = math.sqrt(
        data_list.k / data_list.R * (2 / (data_list.k + 1)) ** ((data_list.k + 1) / (data_list.k - 1)))  # 气动常数

    # 焓降分配
    piT = data_list.pt0 / data_list.pz  # 膨胀比
    grammar = (data_list.k - 1) / data_list.k
    m1 = data_list.Eff * grammar
    aa = 1 / data_list.Eff * (1 - 1 / piT ** m1) / (1 - 1 / piT ** grammar) - 1
    a = (Z - 1) / Z * aa  # 重热系数
    ha = (1 + a) * hs
    h = np.zeros((Z, 1))
    for i in range(Z):
        h[i] = ha / Z
    for j in range(1, Z):
        h[j] = h[j] + 0.1 * h[j - 1]

    # 末级尺寸确定
    qz = data_list.Maz * (1 + (data_list.k - 1) / 2 * data_list.Maz ** 2) ** (
            - (data_list.k + 1) / (2 * (data_list.k - 1))) * ((data_list.k + 1) / 2) ** (
                 (data_list.k + 1) / 2 / (data_list.k - 1))  # 气动函数，用来估算末级出口面积
    Ttz = data_list.Tt0 * (1 - data_list.Efft0 * (
            1 - (data_list.pz / data_list.pt0) ** ((data_list.k - 1) / data_list.k) * (
            1 + (data_list.k - 1) / 2 * data_list.Maz ** 2)))  # 末级出口总温
    ptz = data_list.pz * (1 + (data_list.k - 1) / 2 * data_list.Maz ** 2) ** (data_list.k / (data_list.k - 1))  # 末级出口总压
    caz = np.sqrt(2000 * h[Z - 1])  # 末级理想速度
    # data_list.omaga = 0.357  # 末级反动度，选取
    # data_list.xaz = 0.586  # 末级速度比，选取
    umz = caz * data_list.xaz  # 末级平均速度
    Dmz = 60 * umz / np.pi / data_list.n  # 末级平均直径
    data_list.alph2z = 90  # 末级出口角，轴向出气，为90度
    A2z = data_list.G * np.sqrt(Ttz) / (B * ptz * qz * np.sin(data_list.alph2z * np.pi / 180))  # 末级出口截面积
    l2z = A2z / (np.pi * Dmz)  # 末级平均叶高
    Ttz0 = Ttz + umz ** 2 / (2 * cp)  # 末级滞止温度

    # 强度校核
    Thz = 0.95 * Ttz0  # 末级叶根温度，(0.9~0.95)Ttz0
    # data_list.faiz = 0.5  # 叶片减扭系数，选定，一般为0.48~0.54
    # data_list.rouz = 8.4 * 10 ** 3  # 金属材料密度，由动叶材料定，kg/m3
    # data_list.taoz = 5000  # 叶片适用寿命，选取，h
    fRz = 1.745 * data_list.faiz * data_list.rouz * data_list.n ** 2 * A2z * 10 ** (- 8) / 1000000  # 末级动叶离心应力,MN/m2
    fREz = fRz * (1 + 0.32)  # 末级动叶总应力
    # data_list.fRz_z = 410  # 材料持久强度，查取
    Kz = data_list.fRz_z / fREz  # 叶片安全系数，大于2才可

    # 各级叶栅计算
    # 冷却空气参数，不一定需要考虑

    Ttc = np.full((Z, 1), data_list.Ttic)  # 冷却空气参数总温，给定
    ptc = np.full((Z, 1), data_list.ptic)  # 冷却空气总压，给定
    kc = np.full((Z, 1), data_list.kic)  # 绝热指数
    Rc = np.full((Z, 1), data_list.Ric)  # 气体常数
    cpc = kc / (kc - 1) * Rc  # 定压比热

    # data_list.Gc = np.zeros((Z, 1))  # 冷却空气流量，给定
    # data_list.Gc[0] = 1.65
    # data_list.crc = np.zeros((Z, 1))  # 相对流速比,选取
    # data_list.crc[0] = 0.5
    # for i in range(1, Z):
    #     data_list.Gc[i] = 1.132  # 与冷却空气流量相关的方程
    #     data_list.crc[i] = 0.1  # 与冷却空气流速比相关的方程
    Grc = data_list.Gc / data_list.G
    # 预留空间
    data_list.One_dimension_init(Z)
    if data_list.blade_layout_method == 0:
        # 下面的基本都在for大循环里，记得缩进
        for i in range(Z):
            if i == 0:
                data_list.Tt0M[i] = data_list.Tt0
                data_list.pt0M[i] = data_list.pt0
                data_list.hsM[i] = h[i]  # 级等熵焓降
            else:
                data_list.Tt0M[i] = data_list.Tt2M[i - 1]  # 级进口总温 asf
                data_list.pt0M[i] = data_list.pt2M[i - 1]  # 级进口总压 asf
                data_list.hsM[i] = h[i] + data_list.c2M[i - 1] ** 2 / 2000
            # 第一级静叶
            data_list.Dm1M[i] = Dmz  # 平均直径 asf asfg
            data_list.alph1M[i] = 27.5  # 静叶出口气流角
            data_list.ysM[i] = 0.975  # 静叶速度系数,查取
            data_list.um1M[i] = np.pi * data_list.Dm1M[i] * data_list.n / 60  # 静叶出口平均周向速度 asf
            data_list.c_soundM[i] = np.sqrt(
                2 * data_list.k * data_list.R * data_list.Tt0M[i] / (data_list.k + 1))  # 静叶出口声速
            data_list.p2M[i] = data_list.pt0M[i] * (
                    1 - data_list.hsM[i] * 1000 / (
                    data_list.k / (data_list.k - 1) * data_list.R * data_list.Tt0M[i])) ** (
                                       data_list.k / (data_list.k - 1))  # 级出口静压
            data_list.caM[i] = np.sqrt(2000 * data_list.hsM[i])  # 涡轮假想速度
            if i == Z - 1:
                data_list.omagaM[i] = data_list.omaga
            else:
                data_list.omagaM[i] = 0.32  # 反动度，选取
            data_list.hcM[i] = cpc[i] * Ttc[i] * (
                    1 - (data_list.p2M[i] / ptc[i]) ** ((kc[i] - 1) / kc[i])) / 1000  # 冷气焓降
            data_list.h1sM[i] = (1 - data_list.omagaM[i]) * data_list.hsM[i]  # 静叶焓降
            data_list.c1sM[i] = np.sqrt(2000 * data_list.h1sM[i])  # 静叶出口等熵速度
            data_list.c1M[i] = data_list.ysM[i] * data_list.c1sM[i] * (1 + Grc[i] * data_list.crc[i]) / (
                    1 + Grc[i])  # 静叶出口实际速度
            data_list.c1uM[i] = data_list.c1M[i] * np.cos(data_list.alph1M[i] * np.pi / 180)  # 静叶出口圆周分速度 asf
            data_list.c1zM[i] = data_list.c1M[i] * np.sin(data_list.alph1M[i] * np.pi / 180)  # 静叶出口轴向分速度 asf
            # 冷气影响
            data_list.Tt1_mixM[i] = (data_list.G * cp * data_list.Tt0M[i] + data_list.Gc[i] * cpc[i] * Ttc[i]) / (
                    data_list.G * cp + data_list.Gc[i] * cpc[i])  # 静叶出口混合滞止温度
            data_list.c_sound_mixM[i] = np.sqrt(
                2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt1_mixM[i])  # 静叶出口混合声速
            data_list.Lamda1M[i] = data_list.c1M[i] / data_list.c_sound_mixM[i]  # 静叶出口折合速度
            data_list.T1_mixM[i] = data_list.Tt1_mixM[i] * (
                    1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda1M[i] ** 2)  # 静叶出口静温
            data_list.p1M[i] = data_list.pt0M[i] * (
                    1 - data_list.h1sM[i] * 1000 / (
                    data_list.k / (data_list.k - 1) * data_list.R * data_list.Tt0M[i])) ** (
                                       data_list.k / (data_list.k - 1))  # 静叶出口静压
            data_list.Density1M[i] = data_list.p1M[i] / (data_list.R * data_list.T1_mixM[i])  # 静叶出口密度
            data_list.G1M[i] = data_list.G + data_list.Gc[i]  # 静叶出口流量
            data_list.A1M[i] = data_list.G1M[i] / (data_list.Density1M[i] * data_list.c1M[i])  # 静叶出口截面积
            data_list.l1M[i] = data_list.A1M[i] / (
                    np.pi * data_list.Dm1M[i] * np.sin(data_list.alph1M[i] * np.pi / 180))  # 静叶出口叶高 asfg

            # 第一级动叶
            data_list.w1uM[i] = data_list.c1uM[i] - data_list.um1M[i]  # 动叶进口相对圆周分速
            data_list.w1zM[i] = data_list.c1zM[i]  # 动叶进口轴向分速
            data_list.Beta1M[i] = np.arctan(data_list.w1zM[i] / data_list.w1uM[i]) * 180 / np.pi  # 动叶进口相对气流角
            # 动叶冷却空气参数
            data_list.Gc2M[i] = 0.626  # 动叶冷却空气流量
            data_list.Ttc2M[i] = 743.9  # 动叶冷却空气总温
            data_list.ptc2M[i] = 17.96 * 10 ** 5  # 动叶冷却空气总压
            data_list.kc2M[i] = 1.4  # 动叶冷却空气绝热指数
            data_list.Rc2M[i] = 286.96  # 动叶冷却空气气体常数
            data_list.cpc2M[i] = data_list.kc2M[i] / (data_list.kc2M[i] - 1) * data_list.Rc2M[i]  # 动叶冷却空气定压比热
            data_list.wrc2M[i] = 0.5  # 动叶冷却空气相对流速比
            data_list.Grc2M[i] = data_list.Gc2M[i] / data_list.G  # 动叶冷却空气相对流量比
            # 动叶参数
            data_list.w1M[i] = data_list.w1zM[i] / np.sin(data_list.Beta1M[i] * np.pi / 180)  # 动叶进口相对速度
            data_list.Tt11_mixM[i] = data_list.T1_mixM[i] + data_list.w1M[i] ** 2 / 2 / cp  # 动叶进口总温
            data_list.c1_sound_mixM[i] = np.sqrt(
                2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt11_mixM[i])  # 动叶进口声速
            data_list.Lamda11M[i] = data_list.w1M[i] / data_list.c1_sound_mixM[i]  # 动叶进口折合速度
            data_list.pt1M[i] = data_list.p1M[i] / (
                    1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda11M[i] ** 2) ** (
                                        data_list.k / (data_list.k - 1))  # 动叶进口总压
            data_list.Dm2M[i] = Dmz  # 动叶出口平均直径，根据通流部分形状定,此处认为是等中径
            data_list.um2M[i] = np.pi * data_list.Dm2M[i] * data_list.n / 60  # 动叶出口平均轮周速度 asf
            data_list.Beta2M[i] = 28  # 动叶出口气流角，选取，°
            data_list.yRM[i] = 0.957  # 动叶速度系数
            data_list.w2sM[i] = np.sqrt(
                2000 * data_list.omagaM[i] * data_list.hsM[i] + data_list.w1M[i] ** 2 - data_list.um1M[i] ** 2 +
                data_list.um2M[
                    i] ** 2)  # 动叶出口理想相对速度
            data_list.R_Tt2M[i] = data_list.Tt11_mixM[i] - (data_list.um1M[i] ** 2 - data_list.um2M[i] ** 2) / (
                    2 * cp)  # 动叶出口相对总温
            data_list.w2M[i] = data_list.yRM[i] * data_list.w2sM[i] * (1 + data_list.Grc2M[i] * data_list.wrc2M[i]) / (
                    1 + data_list.Grc2M[i])  # 动叶出口相对速度
            data_list.Tt2_mixM[i] = (data_list.G * cp * data_list.R_Tt2M[i] + data_list.Gc2M[i] * (
                    data_list.cpc2M[i] * data_list.Ttc2M[i] + data_list.um2M[i] ** 2 / 2)) / (
                                            data_list.G * cp + data_list.Gc2M[i] * data_list.cpc2M[i])  # 动叶出口混合总温
            data_list.c2_sound_mixM[i] = np.sqrt(
                2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt2_mixM[i])  # 动叶出口混合音速
            data_list.Lamda12M[i] = data_list.w2M[i] / data_list.c2_sound_mixM[i]  # 动叶出口折合速度
            data_list.T2_mixM[i] = data_list.Tt2_mixM[i] * (
                    1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda12M[i] ** 2)  # 动叶出口混合静温
            data_list.Density2M[i] = data_list.p2M[i] / (data_list.R * data_list.T2_mixM[i])  # 动叶出口密度
            data_list.G2M[i] = data_list.G + data_list.Gc[i] + data_list.Gc2M[i]  # 动叶出口流量
            if i == Z - 1:
                data_list.l2M[i] = l2z
                data_list.A2M[i] = A2z
            else:
                data_list.l2M[i] = data_list.G2M[i] / (
                        np.pi * data_list.Dm2M[i] * data_list.Density2M[i] * data_list.w2M[i] * np.sin(
                    data_list.Beta2M[i] * np.pi / 180))  # 动叶出口叶高 asf asfg
                data_list.A2M[i] = np.pi * data_list.Dm2M[i] * data_list.l2M[i]  # 动叶出口截面积
            data_list.ThM[i] = 0.95 * data_list.R_Tt2M[i]  # 动叶叶根温度，为0.9~0.95Tt2
            data_list.w2uM[i] = data_list.w2M[i] * np.cos(data_list.Beta2M[i] * np.pi / 180)  # 动叶出口相对圆周分速度
            data_list.w2zM[i] = data_list.w2M[i] * np.sin(data_list.Beta2M[i] * np.pi / 180)  # 动叶出口轴向分速度
            data_list.c2zM[i] = data_list.w2zM[i]  # 动叶出口绝对轴向分速度 asf
            data_list.c2uM[i] = data_list.w2uM[i] - data_list.um2M[i]  # 动叶出口圆周分速度 asf
            # 动叶出口气流角计算
            if i == Z - 1:
                data_list.alph12M[i] = data_list.alph2z
            elif np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi > 0:
                data_list.alph12M[i] = np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi
            else:
                data_list.alph12M[i] = 180 + np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi
            data_list.c2M[i] = data_list.c2zM[i] / np.sin(data_list.alph12M[i] * np.pi / 180)  # 动叶出口绝对速度
            if i == Z - 1:
                data_list.Tt2M[i] = Ttz
            else:
                data_list.Tt2M[i] = data_list.T2_mixM[i] + data_list.c2M[i] ** 2 / (2 * cp)  # 动叶出口总温 asf
            data_list.c2_soundM[i] = np.sqrt(
                2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt2M[i])  # 动叶出口声速
            data_list.Ma2M[i] = data_list.c2M[i] / data_list.c2_soundM[i]  # 动叶出口马赫数
            if i == Z - 1:
                data_list.pt2M[i] = ptz
            else:
                data_list.pt2M[i] = data_list.p2M[i] * (1 + (data_list.k - 1) / 2 * data_list.Ma2M[i] ** 2) ** (
                        data_list.k / (data_list.k - 1))  # 动叶出口总压 asf
            # 强度校核
            data_list.faiM[i] = 0.5  # 动叶减扭系数，为0.48~0.54
            data_list.rouM[i] = 8.4 * 10 ** 8  # 金属材料密度
            data_list.taoM[i] = 200  # 叶片使用寿命，h
            data_list.fRM[i] = 1.745 * data_list.faiM[i] * data_list.rouM[i] * data_list.n ** 2 * data_list.A2M[
                i] * 10 ** (
                                   - 8) / 1000000  # 动叶离心应力,MN/m2
            data_list.fREM[i] = data_list.fRM[i] * (1 + 0.32)  # 动叶总应力，MN/m2
            data_list.fR1M[i] = 500  # 材料持久强度，查取
            data_list.KM[i] = data_list.fR1M[i] / data_list.fREM[i]  # 叶片安全系数，大于2才可
            # 通流部分草图
            data_list.H_to_W1M[i] = 16.4 / (data_list.Dm1M[i] / data_list.l1M[i] - 0.25)  # 静叶叶高叶宽比
            data_list.H_to_W2M[i] = 24 / (data_list.Dm2M[i] / data_list.l2M[i])  # 动叶叶高叶宽比
            data_list.Bz1M[i] = data_list.l1M[i] / data_list.H_to_W1M[i]  # 静叶叶宽 asfg
            data_list.Bz2M[i] = data_list.l2M[i] / data_list.H_to_W2M[i]  # 动叶叶宽 asfg
            data_list.ACM[i] = 0.2 * (data_list.Bz1M[i] + data_list.Bz2M[i])  # 轴向间隙
            data_list.LM[i] = 1.2 * (data_list.Bz1M[i] + data_list.Bz2M[i])  # 通流部分长度,所有级通流部分长度的加和，记得带上级与级之间的轴向间隙
            # data_list.YM[i] = np.arctan(
            #     (data_list.l2M[i] - data_list.l1M[i]) / 2 / data_list.LM[i]) * 180 / np.pi  # 通流部分扩张角 # 公式错误
            # data_list.YM.append([0, 8])
            data_list.YM[i] = 8
    elif data_list.blade_layout_method == 1:
        for i in range(Z):
            if i == 0:
                data_list.Tt0M[i] = data_list.Tt0
                data_list.pt0M[i] = data_list.pt0
                data_list.hsM[i] = h[i]  # 级等熵焓降
            else:
                data_list.Tt0M[i] = data_list.Tt2M[i - 1]  # 级进口总温 asf
                data_list.pt0M[i] = data_list.pt2M[i - 1]  # 级进口总压 asf
                data_list.hsM[i] = h[i] + data_list.c2M[i - 1] ** 2 / 2000
            # 第一级静叶
            data_list.YM[i] = 10  # 改，初始通流部分扩张角
            data_list.Dh1M[i] = Dmz - l2z  # 改，等内径，叶根直径都一样
            Bz2 = Dmz / 24  # 改，末级动叶叶宽
            Bz1 = Bz2 / 0.7  # 改，末级静叶叶宽，初步估计值
            ACzM = 0.2 * (Bz1 + Bz2)  # 改，末级轴向间隙，初步估计值
            ACSM = 1.5 * ACzM  # 改，级间轴向间隙，初步估计值
            ls = (Z - i) * (Bz1 + Bz2 + ACzM + ACSM) + ACzM + Bz2  # 改，离末级轴向距离
            dls = ls * np.tan(data_list.YM[i] * np.pi / 180)  # 改，与末级叶高差
            data_list.l1M[i] = l2z - dls  # 改，初始估计的静叶高度
            l1M1 = 0.0  # 改，判断叶高是否合适用
            if i == Z - 1:
                data_list.omagaM[i] = data_list.omaga
            else:
                data_list.omagaM[i] = 0.370  # 反动度，选取
            m = 1.0  # 改，与径向气流参数有关的参数，1和cos^2(alph1m)之间，这里用等环量为例，为1.等alph1时，为cos^2(alph1m)
            while True:  # 改
                while np.abs(l1M1 - data_list.l1M[i]) > 0.00001:  # 改
                    l1M1 = data_list.l1M[i]  # 改
                    data_list.Dm1M[i] = data_list.Dh1M[i] + l1M1  # 改，平均直径 asf asfg
                    data_list.alph1M[i] = 20.0 + 2 * i  # 改，静叶出口气流角
                    data_list.ysM[i] = 0.973  # 改，静叶速度系数,查取
                    data_list.um1M[i] = np.pi * data_list.Dm1M[i] * data_list.n / 60  # 静叶出口平均周向速度 asf
                    data_list.c_soundM[i] = np.sqrt(
                        2 * data_list.k * data_list.R * data_list.Tt0M[i] / (data_list.k + 1))  # 静叶出口声速
                    data_list.p2M[i] = data_list.pt0M[i] * (
                            1 - data_list.hsM[i] * 1000 / (
                            data_list.k / (data_list.k - 1) * data_list.R * data_list.Tt0M[i])) ** (
                                               data_list.k / (data_list.k - 1))  # 级出口静压
                    data_list.caM[i] = np.sqrt(2000 * data_list.hsM[i])  # 涡轮假想速度
                    data_list.hcM[i] = cpc[i] * Ttc[i] * (
                            1 - (data_list.p2M[i] / ptc[i]) ** ((kc[i] - 1) / kc[i])) / 1000  # 冷气焓降
                    data_list.h1sM[i] = (1 - data_list.omagaM[i]) * data_list.hsM[i]  # 静叶焓降
                    data_list.c1sM[i] = np.sqrt(2000 * data_list.h1sM[i])  # 静叶出口等熵速度
                    data_list.c1M[i] = data_list.ysM[i] * data_list.c1sM[i] * (1 + Grc[i] * data_list.crc[i]) / (
                            1 + Grc[i])  # 静叶出口实际速度
                    data_list.c1uM[i] = data_list.c1M[i] * np.cos(data_list.alph1M[i] * np.pi / 180)  # 静叶出口圆周分速度 asf
                    data_list.c1zM[i] = data_list.c1M[i] * np.sin(data_list.alph1M[i] * np.pi / 180)  # 静叶出口轴向分速度 asf
                    # 冷气影响
                    data_list.Tt1_mixM[i] = (data_list.G * cp * data_list.Tt0M[i] + data_list.Gc[i] * cpc[i] * Ttc[
                        i]) / (
                                                    data_list.G * cp + data_list.Gc[i] * cpc[i])  # 静叶出口混合滞止温度
                    data_list.c_sound_mixM[i] = np.sqrt(
                        2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt1_mixM[i])  # 静叶出口混合声速
                    data_list.Lamda1M[i] = data_list.c1M[i] / data_list.c_sound_mixM[i]  # 静叶出口折合速度
                    data_list.T1_mixM[i] = data_list.Tt1_mixM[i] * (
                            1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda1M[i] ** 2)  # 静叶出口静温
                    data_list.p1M[i] = data_list.pt0M[i] * (
                            1 - data_list.h1sM[i] * 1000 / (data_list.k / (data_list.k - 1) * data_list.R *
                                                            data_list.Tt1_mixM[i])) ** (
                                               data_list.k / (data_list.k - 1))  # 静叶出口静压
                    data_list.Density1M[i] = data_list.p1M[i] / (data_list.R * data_list.T1_mixM[i])  # 静叶出口密度
                    data_list.G1M[i] = data_list.G + data_list.Gc[i]  # 静叶出口流量
                    data_list.A1M[i] = data_list.G1M[i] / (data_list.Density1M[i] * data_list.c1M[i])  # 静叶出口截面积
                    data_list.l1M[i] = data_list.A1M[i] / (
                            np.pi * data_list.Dm1M[i] * np.sin(data_list.alph1M[i] * np.pi / 180))  # 静叶出口叶高 asfg

                # 第一级动叶
                data_list.w1uM[i] = data_list.c1uM[i] - data_list.um1M[i]  # 动叶进口相对圆周分速
                data_list.w1zM[i] = data_list.c1zM[i]  # 动叶进口轴向分速
                data_list.Beta1M[i] = np.arctan(data_list.w1zM[i] / data_list.w1uM[i]) * 180 / np.pi  # 动叶进口相对气流角
                # 动叶冷却空气参数
                data_list.Gc2M[i] = 0  # 改，动叶冷却空气流量（动力涡轮为0）
                data_list.Ttc2M[i] = 743.9  # 动叶冷却空气总温
                data_list.ptc2M[i] = 17.96 * 10 ** 5  # 动叶冷却空气总压
                data_list.kc2M[i] = 1.4  # 动叶冷却空气绝热指数
                data_list.Rc2M[i] = 286.96  # 动叶冷却空气气体常数
                data_list.cpc2M[i] = data_list.kc2M[i] / (data_list.kc2M[i] - 1) * data_list.Rc2M[i]  # 动叶冷却空气定压比热
                data_list.wrc2M[i] = 0.5  # 动叶冷却空气相对流速比
                data_list.Grc2M[i] = data_list.Gc2M[i] / data_list.G  # 动叶冷却空气相对流量比
                # 动叶参数
                data_list.w1M[i] = data_list.w1zM[i] / np.sin(data_list.Beta1M[i] * np.pi / 180)  # 动叶进口相对速度
                data_list.Tt11_mixM[i] = data_list.T1_mixM[i] + data_list.w1M[i] ** 2 / 2 / cp  # 动叶进口总温
                data_list.c1_sound_mixM[i] = np.sqrt(
                    2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt11_mixM[i])  # 动叶进口声速
                data_list.Lamda11M[i] = data_list.w1M[i] / data_list.c1_sound_mixM[i]  # 动叶进口折合速度
                data_list.pt1M[i] = data_list.p1M[i] / (
                        1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda11M[i] ** 2) ** (
                                            data_list.k / (data_list.k - 1))  # 动叶进口总压
                data_list.Dh2M[i] = data_list.Dh1M[i]  # 改，等内径，叶根直径都一样
                lr = (Z - i) * (Bz1 + Bz2 + ACzM + ACSM)  # 改，离末级轴向距离
                dlr = lr * np.tan(data_list.YM[i] * np.pi / 180)  # 改，与末级叶高差
                data_list.l2M[i] = l2z - dlr  # 改，初始估计的动叶高度
                l2M1 = 0.0  # 改，判断叶高是否合适用
                while np.abs(l2M1 - data_list.l2M[i]) > 0.00001:
                    l2M1 = data_list.l2M[i]  # 改
                    data_list.Dm2M[i] = data_list.Dh2M[i] + l2M1  # 改，动叶出口平均直径，根据通流部分形状定
                    data_list.um2M[i] = np.pi * data_list.Dm2M[i] * data_list.n / 60  # 动叶出口平均轮周速度 asf
                    data_list.Beta2M[i] = 22.0 + 2 * i  # 动叶出口气流角，选取，°
                    data_list.yRM[i] = 0.955  # 动叶速度系数
                    data_list.w2sM[i] = np.sqrt(
                        2000 * data_list.omagaM[i] * data_list.hsM[i] + data_list.w1M[i] ** 2 - data_list.um1M[i] ** 2 +
                        data_list.um2M[i] ** 2)  # 动叶出口理想相对速度
                    data_list.R_Tt2M[i] = data_list.Tt11_mixM[i] - (data_list.um1M[i] ** 2 - data_list.um2M[i] ** 2) / (
                            2 * cp)  # 动叶出口相对总温
                    data_list.w2M[i] = data_list.yRM[i] * data_list.w2sM[i] * (
                            1 + data_list.Grc2M[i] * data_list.wrc2M[i]) / (
                                               1 + data_list.Grc2M[i])  # 动叶出口相对速度
                    data_list.Tt2_mixM[i] = (data_list.G * cp * data_list.R_Tt2M[i] + data_list.Gc2M[i] * (
                            data_list.cpc2M[i] * data_list.Ttc2M[i] + data_list.um2M[i] ** 2 / 2)) / (
                                                    data_list.G * cp + data_list.Gc2M[i] * data_list.cpc2M[
                                                i])  # 动叶出口混合总温
                    data_list.c2_sound_mixM[i] = np.sqrt(
                        2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt2_mixM[i])  # 动叶出口混合音速
                    data_list.Lamda12M[i] = data_list.w2M[i] / data_list.c2_sound_mixM[i]  # 动叶出口折合速度
                    data_list.T2_mixM[i] = data_list.Tt2_mixM[i] * (
                            1 - (data_list.k - 1) / (data_list.k + 1) * data_list.Lamda12M[i] ** 2)  # 动叶出口混合静温
                    data_list.Density2M[i] = data_list.p2M[i] / (data_list.R * data_list.T2_mixM[i])  # 动叶出口密度
                    data_list.G2M[i] = data_list.G + data_list.Gc[i] + data_list.Gc2M[i]  # 动叶出口流量
                    # 改，不再用之前末级的数据 if i == Z - 1:
                    # 改，data_list.l2M[i] = l2z
                    # 改，data_list.A2M[i] = A2z
                    # 改，else:
                    data_list.l2M[i] = data_list.G2M[i] / (
                            np.pi * data_list.Dm2M[i] * data_list.Density2M[i] * data_list.w2M[i]
                            * np.sin(data_list.Beta2M[i] * np.pi / 180))  # 动叶出口叶高 asf asfg
                    data_list.A2M[i] = np.pi * data_list.Dm2M[i] * data_list.l2M[i]  # 动叶出口截面积
                data_list.omagahM[i] = 1 - (1 - data_list.omagaM[i]) * (1 + data_list.ysM[i] ** 2 / m *
                                                                        np.cos(data_list.alph1M[i] * np.pi / 180) ** 2 *
                                                                        (1 / (data_list.Dh2M[i] /
                                                                              data_list.Dm2M[i]) ** (
                                                                                     2 * m) - 1))  # 改，叶根反动度
                if data_list.omagahM[i] < 0:  # 改，判断叶根反动度是否小于0，如果小于0，需提升平均反动度
                    data_list.omagaM[i] = data_list.omagaM[i] + 0.05  # 改
                else:
                    break  # 改

            data_list.ThM[i] = 0.95 * data_list.R_Tt2M[i]  # 动叶叶根温度，为0.9~0.95Tt2
            data_list.w2uM[i] = data_list.w2M[i] * np.cos(data_list.Beta2M[i] * np.pi / 180)  # 动叶出口相对圆周分速度
            data_list.w2zM[i] = data_list.w2M[i] * np.sin(data_list.Beta2M[i] * np.pi / 180)  # 动叶出口轴向分速度
            data_list.c2zM[i] = data_list.w2zM[i]  # 动叶出口绝对轴向分速度 asf
            data_list.c2uM[i] = data_list.w2uM[i] - data_list.um2M[i]  # 动叶出口圆周分速度 asf
            # 动叶出口气流角计算
            # 改，不再用之前末级的数据，if i == Z - 1:
            # 改，data_list.alph12M[i] = data_list.alph2z
            if np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi > 0:
                data_list.alph12M[i] = np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi
            else:
                data_list.alph12M[i] = 180 + np.arctan(data_list.c2zM[i] / data_list.c2uM[i]) * 180 / np.pi
            data_list.c2M[i] = data_list.c2zM[i] / np.sin(data_list.alph12M[i] * np.pi / 180)  # 动叶出口绝对速度
            # 改，不再用之前末级的数据，if i == Z - 1:
            # 改，data_list.Tt2M[i] = Ttz
            # 改，else:
            data_list.Tt2M[i] = data_list.T2_mixM[i] + data_list.c2M[i] ** 2 / (2 * cp)  # 动叶出口总温 asf
            data_list.c2_soundM[i] = np.sqrt(
                2 * data_list.k / (data_list.k + 1) * data_list.R * data_list.Tt2M[i])  # 动叶出口声速
            data_list.Ma2M[i] = data_list.c2M[i] / data_list.c2_soundM[i]  # 动叶出口马赫数
            # 改，不再用之前末级的数据，if i == Z - 1:
            # 改，data_list.pt2M[i] = ptz
            # 改，else:
            data_list.pt2M[i] = data_list.p2M[i] * (1 + (data_list.k - 1) / 2 * data_list.Ma2M[i] ** 2) ** (
                    data_list.k / (data_list.k - 1))  # 动叶出口总压 asf
            # 强度校核
            data_list.faiM[i] = 0.5  # 动叶减扭系数，为0.48~0.54
            data_list.rouM[i] = 8.4 * 10 ** 3  # 改，金属材料密度
            data_list.taoM[i] = 200  # 叶片使用寿命，h
            data_list.fRM[i] = 1.745 * data_list.faiM[i] * data_list.rouM[i] * data_list.n ** 2 * data_list.A2M[
                i] * 10 ** (
                                   - 3)  # 动叶离心应力,MN/m2
            data_list.fREM[i] = data_list.fRM[i] * (1 + 0.32)  # 动叶总应力，MN/m2
            data_list.fR1M[i] = 500  # 材料持久强度，查取
            data_list.KM[i] = data_list.fR1M[i] / data_list.fREM[i]  # 叶片安全系数，大于2才可
            # 通流部分草图
            data_list.H_to_W1M[i] = 16.4 / (data_list.Dm1M[i] / data_list.l1M[i] - 0.25)  # 静叶叶高叶宽比
            data_list.H_to_W2M[i] = 24 / (data_list.Dm2M[i] / data_list.l2M[i])  # 动叶叶高叶宽比
            data_list.Bz1M[i] = data_list.l1M[i] / data_list.H_to_W1M[i]  # 静叶叶宽 asfg
            data_list.Bz2M[i] = data_list.l2M[i] / data_list.H_to_W2M[i]  # 动叶叶宽 asfg
            data_list.ACM[i] = 0.2 * (data_list.Bz1M[i] + data_list.Bz2M[i])  # 轴向间隙
            data_list.LM[i] = 1.2 * (data_list.Bz1M[i] + data_list.Bz2M[i])  # 通流部分长度,所有级通流部分长度的加和，记得带上级与级之间的轴向间隙
            LMt = data_list.LM[i] - (data_list.Bz2M[i] * (
                        1 - 0.04 * (data_list.Zr - 1 - math.ceil(data_list.Zr / 2))))  # 改，叶顶通流部分长度，前缘积叠这么算的
            # LMt = data_list.LM[i] - (data_list.Bz2M[i] * (1 - 0.04 * (data_list.Zr-1 - math.ceil(data_list.Zr / 2)))) +
            # (data_list.Bz1M[i] * (1 + 0.04 * (data_list.Zr-1 - math.ceil(data_list.Zr / 2))))  # 最大厚度积叠这么算的
            data_list.YM[i] = np.arctan(
                (data_list.l2M[i] - data_list.l1M[i]) / LMt) * 180 / np.pi  # 改，现在可以直接用，通流部分扩张角
