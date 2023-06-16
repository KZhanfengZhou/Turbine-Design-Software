import math
import numpy as np
from design_calculation import data_list

# 注意！！！python中的下标0开始，matlab中1开始
# ddd 标记改变


# 设计的第二步：径向气流参数计算，根据第一步的计算结果，来确定径向方向上气流参数的分布。（程序未完全完善，只是拿了某一级为例，实际上应该加一个大循环，把每一级都放进去）

KG = 0.999  # 端壁附面层阻塞系数,默认值，不用管
Zr = 5  # 对于短叶片，5~7，过长的叶片要超过11


# 径向气流参数分布计算
# 长度单位，m
# 速度单位，m/s
# 角度单位，°
# 压力单位，Pa
# 温度单位，K
# 转速单位，rpm
# 密度单位，kg/m3
# 给定数据及计算准备
# 通流部分结构尺寸

def radial_gas_parameter_distribution(blade_stage):  # blade_stage 叶片级数
    global KG
    global Zr
    D1m = data_list.Dm1M[blade_stage]  # ddd # 改，动叶进口平均直径，和静叶出口平均直径一致，通流方案计算得出
    D2m = data_list.Dm2M[blade_stage]  # 改，动叶出口平均直径，通流方案计算得出
    l1 = data_list.l1M[blade_stage]  # 改，动叶进口叶高，和静叶出口叶高一致，通流方案计算得出
    l2 = data_list.l2M[blade_stage]  # ddd # 动叶出口叶高，计算时先假定进出口叶高一致
    r1T = D1m / 2 + l1 / 2  # 各级动叶进口叶顶尺寸，通流方案计算得出
    r1H = D1m / 2 - l1 / 2  # 各级动叶进口轮毂尺寸，通流方案计算得出
    r2T = D2m / 2 + l2 / 2  # 各级动叶出口叶顶尺寸，通流方案计算得出
    r2H = D2m / 2 - l2 / 2  # 各级动叶出口轮毂尺寸，通流方案计算得出
    # KG = 0.999  # 端壁附面层阻塞系数,默认值，不用管
    Dertah = 0.5 * (1 + KG)  # 轮毂阻塞因子,默认值，不用管
    DertaT = 0.5 * (1 + KG)  # 外壁阻塞因子,默认值，不用管
    r1hq = math.sqrt(Dertah * r1H ** 2 + (1 - Dertah) * r1T ** 2)  # 进口轮毂气动计算半径
    r1tq = math.sqrt(DertaT * r1T ** 2 + (1 - DertaT) * r1H ** 2)  # 进口外壁气动计算半径
    r1m = 0.5 * (r1tq + r1hq)  # 进口平均半径，按气动计算半径平均
    r2hq = math.sqrt(Dertah * r2H ** 2 + (1 - Dertah) * r2T ** 2)  # 出口轮毂气动计算半径
    r2tq = math.sqrt(DertaT * r2T ** 2 + (1 - DertaT) * r2H ** 2)  # 出口外壁气动计算半径
    r2m = 0.5 * (r2tq + r2hq)  # 出口平均半径，按气动计算半径平均

    # 平均直径上的速度三角形
    c1zm = data_list.c1zM[blade_stage]  # ddd # 动叶进口轴向分速度，通流方案计算得出
    c1um = data_list.c1uM[blade_stage]  # ddd # 动叶进口圆周分速度，通流方案计算得出
    u1m = data_list.um1M[blade_stage]  # ddd# 动叶进口轮周分速度，通流方案计算得出
    c2zm = data_list.c2zM[blade_stage]  # ddd# 动叶出口轴向分速度，通流方案计算得出
    c2um = data_list.c2uM[blade_stage]  # ddd # 动叶出口圆周分速度，通流方案计算得出
    u2m = data_list.um2M[blade_stage]  # ddd 等于406.494 # 动叶出口轮周分速度，通流方案计算得出

    # 通流部分进出口气体参数
    pt0 = data_list.pt0M[blade_stage]  # ddd # 进口总压，通流方案计算得出
    Tt0 = data_list.Tt0M[blade_stage]  # ddd# 进口总温，通流方案计算得出
    Tt1 = Tt0  # 静叶出口总温，计算得来
    pt1 = pt0  # 静叶出口总压，计算得来
    # G = 87.5975  # 流量，给定
    # n = 5300  # 转速
    # ptz = 210567  # 出口总压，通流方案计算得出或给定
    ptz = data_list.pt2M[blade_stage]  # ddd 1中的备注是动叶出口总压。
    # Ttz = 360.293  # 出口总温，通流部分计算得出或给定
    Ttz = data_list.Tt2M[blade_stage]  # ddd 1中的备注是动叶出口总温。
    data_list.k = 1.33  # 绝热指数，给定,默认值，不用管
    data_list.R = 287.25  # 气体常数，给定，默认值，不用管
    # 数据准备截止

    # 确定径向计算站的数目及其位置
    # Zr = 5  # 对于短叶片，5~7，过长的叶片要超过11
    data_list.Zr = Zr
    r1i = np.zeros(Zr)
    r1i[0] = r1hq  # 进口第一个计算站位置
    r2i = np.zeros(Zr)
    r2i[0] = r2hq  # 出口第一个计算站位置
    for i in range(1, Zr):
        r1i[i] = r1i[i - 1] + (r1tq - r1hq) / (Zr - 1)
        r2i[i] = r2i[i - 1] + (r2tq - r2hq) / (Zr - 1)
    # 动叶进口截面，扭曲都为等功条件扭曲
    # 沿径向分布规律确定速度三角形
    u1i = np.zeros(Zr)
    for i in range(Zr):
        u1i[i] = 2 * math.pi * r1i[i] * data_list.n / 60
    # 用幂指数方法计算
    m = 1  # 1和cos^2(alph1m)之间，这里用等环量为例，为1.等alph1时，为cos^2(alph1m)
    B = c1um * r1m ** m  # 常数
    # 定义矩阵，预留存储空间
    c1zi = np.zeros(Zr)  # 绝对速度轴向分速
    c1ui = np.zeros(Zr)  # 绝对速度周向分速
    c1i = np.zeros(Zr)  # 绝对速度
    w1ui = np.zeros(Zr)  # 相对速度圆周分速
    w1i = np.zeros(Zr)  # 相对速度
    alpha1i = np.zeros(Zr)  # 绝对速度方向角，静叶出口气流角 asfg
    Beta1i = np.zeros(Zr)  # 相对速度方向角，动叶进口气流角 asfg
    a1i = math.sqrt(2 * data_list.k / (data_list.k + 1) * data_list.R * Tt1)  # 临界音速
    Lambda1i = np.zeros(Zr)  # 无因次速度
    Ma_w1i = np.zeros(Zr)
    T1i = np.zeros(Zr)  # 动叶进口静温
    p1i = np.zeros(Zr)  # 动叶进口静压
    Density1i = np.zeros(Zr)  # 动叶进口静密度
    q1i = np.zeros(Zr)  # 单位面积流量
    # 参数计算
    for i in range(Zr):
        c1ui[i] = B / r1i[i] ** m
        c1zi[i] = c1zm * math.sqrt(1 + 1 / (c1zm / c1um) ** 2 * (1 - m) / m * ((r1m / r1i[i]) ** 2 * m - 1))
        c1i[i] = math.sqrt(c1zi[i] ** 2 + c1ui[i] ** 2)
        w1ui[i] = abs(c1ui[i] - u1i[i])
        w1i[i] = math.sqrt(c1zi[i] ** 2 + w1ui[i] ** 2)
        alpha1i[i] = math.atan(c1zi[i] / c1ui[i]) * 180 / math.pi
        if c1ui[i] - u1i[i] > 0:
            Beta1i[i] = math.atan(c1zi[i] / w1ui[i]) * 180 / math.pi
        else:
            Beta1i[i] = math.atan(-c1zi[i] / w1ui[i]) * 180 / math.pi + 180
        Lambda1i[i] = c1i[i] / a1i  # 无因次速度
        T1i[i] = Tt1 * (1 - (data_list.k - 1) / (data_list.k + 1) * Lambda1i[i] ** 2)
        Ma_w1i[i] = w1i[i] / math.sqrt(data_list.k * data_list.R * T1i[i])
        p1i[i] = pt1 * (1 - (data_list.k - 1) / (data_list.k + 1) * Lambda1i[i] ** 2) ** (
                data_list.k / (data_list.k - 1))
        Density1i[i] = pt1 / (data_list.R * Tt1) * (1 - (data_list.k - 1) / (data_list.k + 1) * Lambda1i[i] ** 2) ** (
                1 / (data_list.k - 1))
        q1i[i] = Density1i[i] * c1zi[i]
    # 流量校核
    DAi = np.zeros(Zr - 1)  # 计算站之间的面积
    DGi = np.zeros(Zr - 1)  # 计算站之间的流量
    G1i = 0  # 流量
    for i in range(Zr - 1):
        DAi[i] = math.pi * (r1i[i + 1] ** 2 - r1i[i] ** 2)
        DGi[i] = DAi[i] * (q1i[i + 1] + q1i[i]) / 2
        G1i = G1i + DGi[i]
    eG = (G1i - data_list.G) / data_list.G * 100  # 流量误差 如果不满足要求，必须要改变c1zm的值或者改变通道尺寸

    # 动叶出口截面
    # 速度三角形
    E = (1 - (r1hq / r1tq) ** 2) / (1 - (r2hq / r2tq) ** 2) * (r1tq / r2tq) ** 2  # 截面比例系数
    u2i = np.zeros(Zr)  # 轮周速度
    c2ui = np.zeros(Zr)  # 绝对速度圆周分速
    c2zi = np.zeros(Zr)  # 绝对速度轴向分速
    c2i = np.zeros(Zr)  # 绝对速度
    w2ui = np.zeros(Zr)  # 相对速度周向分速
    w2i = np.zeros(Zr)  # 相对速度
    alpha2i = np.zeros(Zr)  # 绝对速度方向角 动叶出口绝对方向角
    Beta2i = np.zeros(Zr)  # 相对速度方向角，动叶出口气流角，asdfg
    h = u2m * c2um + u1m * c1um  # 输出功，J/kg
    # 解方程
    Ym = 2 * E / (r1m ** 2 * r2m) * ((1 - m) * c1um ** 2 * r1m ** 2 - (1 - m) * c1um * r1m * r2m * h / u2m)  # 常数，下同
    Yh = 2 * E / (r1m ** 2 * r2hq) * (
            (1 - m) * (1 + E * (r2m / r1m) ** 2 * ((r2hq / r2m) ** 2 - 1)) ** (-m) * c1um ** 2 * r1m ** 2 - (1 - m) * (
            1 + E * (r2m / r1m) ** 2 * ((r2hq / r2m) ** 2 - 1)) ** (-(m + 1) / 2))
    Yt = 2 * E / (r1m ** 2 * r2tq) * (
            (1 - m) * (1 + E * (r2m / r1m) ** 2 * ((r2tq / r2m) ** 2 - 1)) ** (-m) * c1um ** 2 * r1m ** 2 - (1 - m) * (
            1 + E * (r2m / r1m) ** 2 * ((r2tq / r2m) ** 2 - 1)) ** (-(m + 1) / 2))
    AA = r2m * r2hq * (r2m - r2hq)
    BB = r2m ** 2 - r2hq ** 2
    CC = Yh * r2m ** 2 - Ym * r2hq ** 2
    DD = r2m * r2tq * (r2m - r2tq)
    EE = r2m ** 2 - r2tq ** 2
    FF = Yt * r2m ** 2 - Ym * r2tq ** 2
    aa0 = (AA * FF - CC * DD) / (AA * EE - BB * DD)
    aa1 = (CC * EE - BB * FF) / (AA * EE - BB * DD)
    aa2 = (Ym - aa1 * r2m - aa0) / (r2m ** 2)
    for j in range(Zr):
        u2i[j] = 2 * math.pi * r2i[j] * data_list.n / 60
        c2ui[j] = -r1i[j] / r2i[j] * c1um / (r1i[j] / r1m) ** m + h / u2m / (r2i[j] / r2m)
        c2zi[j] = math.sqrt(
            c2zm ** 2 + 1 / 3 * aa2 * (r2m ** 3 - r2i[j] ** 2) + 0.5 * aa1 * (r2m ** 2 - r2i[j] ** 2) + aa0 * (
                    r2m - r2i[j]))
        c2i[j] = math.sqrt(c2ui[j] ** 2 + c2zi[j] ** 2)
        w2ui[j] = u2i[j] + c2ui[j]
        w2i[j] = math.sqrt(c2zi[j] ** 2 + w2ui[j] ** 2)
        if c2ui[j] < 0:  # 用来确定出口角是否大于90度
            alpha2i[j] = math.atan(c2zi[j] / c2ui[j]) * 180 / math.pi + 180
        else:
            alpha2i[j] = math.atan(c2zi[j] / c2ui[j]) * 180 / math.pi
        Beta2i[j] = math.atan(c2zi[j] / w2ui[j]) * 180 / math.pi

    # 气体状态计算
    cp = data_list.R * data_list.k / (data_list.k - 1)  # 气体定压比热
    DT2i = h / cp  # 动叶中的总温差
    Tt2 = Tt1 - DT2i  # 气体总温
    T2i = np.zeros(Zr)  # 气体静温
    Ma_c2i = np.zeros(Zr)  # 绝对速度马赫数
    RTt1i = np.zeros(Zr)  # 进口相对总温
    RLambda1i = np.zeros(Zr)  # 进口相对无因次速度
    a2i = math.sqrt(2 * data_list.k / (data_list.k + 1) * data_list.R * Tt2)  # 临界音速
    Lambda2i = np.zeros(Zr)  # 无因次速度
    Rpt1i = np.zeros(Zr)  # 进口相对总压
    RTt2i = np.zeros(Zr)  # 出口相对总温
    RLambda2i = np.zeros(Zr)  # 出口相对无因次速度
    Ideal_Rpt2i = np.zeros(Zr)  # 理论出口相对总压
    Co2i = np.zeros(Zr)  # 总压恢复系数
    Rpt2i = np.zeros(Zr)  # 出口相对总压
    p2i = np.zeros(Zr)  # 出口绝对静压
    pt2i = np.zeros(Zr)  # 出口绝对总压
    Density2i = np.zeros(Zr)  # 出口绝对静密度
    q2i = np.zeros(Zr)  # 单位面积流量
    for i in range(Zr):
        Lambda2i[i] = c2i[i] / a2i
        T2i[i] = Tt2 * (1 - (data_list.k - 1) / (data_list.k + 1) * Lambda2i[i] ** 2)
        Ma_c2i[i] = c2i[i] / math.sqrt(data_list.k * data_list.R * T2i[i])
        RTt1i[i] = T1i[i] + w1i[i] ** 2 / (2 * cp)
        RLambda1i[i] = w1i[i] / math.sqrt(2 * data_list.k / (data_list.k + 1) * data_list.R * RTt1i[i])
        Rpt1i[i] = p1i[i] / (1 - (data_list.k - 1) / (data_list.k + 1) * RLambda1i[i] ** 2) ** (
                data_list.k / (data_list.k - 1))
        RTt2i[i] = T2i[i] + w2i[i] ** 2 / (2 * cp)
        RLambda2i[i] = w2i[i] / math.sqrt(2 * data_list.k / (data_list.k + 1) * data_list.R * RTt2i[i])
        Ideal_Rpt2i[i] = Rpt1i[i] * (RTt2i[i] / RTt1i[i]) ** (data_list.k / (data_list.k - 1))
        Co2i[i] = 0.996  # 估取的
        Rpt2i[i] = Co2i[i] * Ideal_Rpt2i[i]
        p2i[i] = Rpt2i[i] * (1 - (data_list.k - 1) / (data_list.k + 1) * RLambda2i[i] ** 2) ** (
                data_list.k / (data_list.k - 1))
        pt2i[i] = p2i[i] / (1 - (data_list.k - 1) / (data_list.k + 1) * Lambda2i[i] ** 2) ** (
                data_list.k / (data_list.k - 1))
        Density2i[i] = pt2i[i] / (data_list.R * Tt2) * (
                1 - (data_list.k - 1) / (data_list.k + 1) * Lambda2i[i] ** 2) ** (1 / (data_list.k - 1))
        q2i[i] = Density2i[i] * c2zi[i]
    # 流量校核
    DA2i = np.zeros((Zr - 1, 1))  # 计算站之间的面积
    DG2i = np.zeros((Zr - 1, 1))  # 计算站之间的流量
    G2i = 0  # 流量
    for i in range(Zr - 1):
        DA2i[i] = math.pi * (r2i[i + 1] ** 2 - r2i[i] ** 2)
        DG2i[i] = DA2i[i] * (q2i[i + 1] + q2i[i]) / 2
        G2i = G2i + DG2i[i]
    eG2 = (G2i - data_list.G) / data_list.G * 100  # 流量误差 如果不满足要求，必须要改变c2zm的值或者改变通道尺寸
    omaga = np.zeros(Zr)  # 反动度
    for i in range(Zr):
        omaga[i] = T1i[i] * (1 - (p2i[i] / p1i[i]) ** ((data_list.k - 1) / data_list.k)) / Tt0 / (
                1 - (p2i[i] / pt0) ** ((data_list.k - 1) / data_list.k))
    data_list.alpha1i.append(alpha1i)
    data_list.Beta1i.append(Beta1i)
    data_list.Beta2i.append(Beta2i)
    data_list.c1i.append(c1i)
    data_list.c2i.append(c2i)
    data_list.w1i.append(w1i)
    data_list.w2i.append(w2i)
    data_list.T1i.append(T1i)
    data_list.p1i.append(p1i)
    data_list.G1i.append(G1i)  # 流量是一维量
    data_list.w1i.append(w1i)
    data_list.alpha2i.append(alpha2i)
    data_list.Tt2.append(Tt2)  # 气体总温是一维量
    data_list.T2i.append(T2i)
    data_list.Ma_c2i.append(Ma_c2i)
    data_list.p2i.append(p2i)
    data_list.pt2i.append(pt2i)
    data_list.Radial_omega.append(omaga)
