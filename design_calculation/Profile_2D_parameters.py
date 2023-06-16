import math
import numpy as np
from blade_geometry import calcu

from design_calculation import data_list


def Profile_2d_parameters(blade_stage, radial_stage):
    # 设计的第三步：主要是根据第二步的计算结果，前面计算的仅仅是气流参数，需要转换成几何参数，如气流角转换成几何角。（也不够完善，这里也仅仅是以某一个截面为例的）
    # 平面叶栅设计参数
    # 角度单位，°
    # 长度单位，m
    #  数据准备
    Stator_i = -2  # 静角，-2~-6之间叶攻
    Rotor_i = -2  # 动叶攻角，反动式-2~-6之间，冲动式可增大至+12
    Stator_Beta1 = 90  # 静叶进口气流角，一般为0,即90
    Stator_Beta2 = data_list.alpha1i[blade_stage, radial_stage]  # 静叶出口气流角，由一维设计确定，需要外部输入 ddd
    Rotor_Beta1 = data_list.Beta1i[blade_stage, radial_stage]  # 动叶进口气流角，由一维设计确定，需要外部输入 ddd
    Rotor_Beta2 = data_list.Beta2i[blade_stage, radial_stage]  # 动叶出口气流角，由一维设计确定，需要外部输入 ddd
    Stator_B = data_list.Bz1M[blade_stage] * (
            1 + 0.04 * (radial_stage - math.ceil(data_list.Zr / 2)))  # 静叶宽度，由一维设计确定，需要外部输入 ddd # 叶宽微调
    Rotor_B = data_list.Bz2M[blade_stage] * (
            1 - 0.04 * (radial_stage - math.ceil(data_list.Zr / 2)))  # 动叶宽度，由一维设计确定，需要外部输入 ddd# 叶宽微调
    Stator_l2 = data_list.l1M[blade_stage]  # 静叶出口叶高，由一维设计确定，需要外部输入 ddd
    Rotor_l2 = data_list.l2M[blade_stage]  # 动叶出口叶高，由一维设计确定，需要外部输入 ddd
    Co_Beta2 = np.zeros(2)  # 余角，arccos(o/t)
    Co_Beta2[0] = 90 - Stator_Beta2
    Co_Beta2[1] = 90 - Rotor_Beta2
    Ba_Beta = np.zeros(2)  # 落后角
    Stator_Dm = data_list.Dm1M[blade_stage]  # 静叶平均直径，由一维设计确定，需要外部输入 ddd
    Rotor_Dm = data_list.Dm2M[blade_stage]  # 动叶平均直径，由一维设计确定，需要外部输入 ddd
    Stator_w1 = 10  # 静叶前缘扩张角，8~10度（圆弧两边切线的夹角）
    Stator_w2 = 8  # 静叶尾缘扩张角， 8~10度
    Rotor_w1 = 10  # 动叶前缘扩张角， 8~10度
    Rotor_w2 = 8  # 动叶尾缘扩张角，8~10度
    # 参数计算，中部为例，其余的后面加上
    # 角度
    Stator_Beta1_g = Stator_i + Stator_Beta1  # 静叶进口几何角
    Rotor_Beta1_g = Rotor_i + Rotor_Beta1  # 动叶进口几何角
    for i in range(2):  # 需要查表，这里把马赫数定为0.5，一般来说都是合理的
        Ba_Beta[i] = -0.2 * Co_Beta2[i] + 14
    Stator_Beta2_g = Stator_Beta2 - Ba_Beta[0]  # 静叶出口几何角
    Rotor_Beta2_g = Rotor_Beta2 - Ba_Beta[1]  # 动叶出口几何角
    Stator_Gamma = 57.84 - 0.3929 * Stator_Beta1_g + 0.8221 * Stator_Beta2_g  # 静叶安装角
    Rotor_Gamma = 57.84 - 0.3929 * Rotor_Beta1_g + 0.8221 * Rotor_Beta2_g  # 动叶安装角

    # 厚度,长度
    Stator_b = Stator_B / math.sin(Stator_Gamma * math.pi / 180)
    Rotor_b = Stator_B / math.sin(Rotor_Gamma * math.pi / 180)
    # 前缘、尾缘、最大厚度
    Stator_Cmax = Stator_B * 0.1  # 静叶最大厚度，取10%。值得注意的是，这里的叶片厚度并不大
    # Rotor_Cmax = Rotor_B * 0.13  # 动叶最大厚度，叶根取15~20%，叶顶4~6%，这里为中部的，后续可以把叶根和叶顶也加上
    Rotor_Cmax = Rotor_B * (0.2 - (0.2 - 0.04) / data_list.Zr * radial_stage)  # 改，动叶最大厚度，叶根取15~20%，叶顶4~6%。
    Stator_r1 = Stator_Cmax * 0.4  # 静叶前缘半径，12~40%最大厚度
    Rotor_r1 = Rotor_Cmax * 0.4  # 动叶前缘半径，12~40%最大厚度
    Stator_r2 = Stator_Cmax * 0.06  # 静叶尾缘半径，12~40%最大厚度
    Rotor_r2 = Rotor_Cmax * 0.06  # 动叶尾缘半径，12~40%最大厚度
    if Stator_r2 < 0.7e-3:  # 考虑到加工要求，尾缘半径不能低于0.7 mm
        Stator_r2 = 0.7e-3
    if Rotor_r2 < 0.7e-3:
        Rotor_r2 = 0.7e-3
    Stator_cons = 1.2  # 静叶稠度，1.0~1.4
    Stator_t = Stator_b / Stator_cons  # 静叶节距
    Stator_o = Stator_t * math.sin(Stator_Beta2 * math.pi / 180)  # 静叶喉宽
    Rotor_cons = 1.5  # 动叶稠度，中部1.35~1.65
    Rotor_t = Rotor_b / Rotor_cons  # 动叶节距
    Rotor_o = Rotor_t * math.sin(Rotor_Beta2 * math.pi / 180)  # 动叶喉宽

    # 叶片数
    Stator_z = math.ceil(math.pi * Stator_Dm / Stator_t)  # 静叶叶片数
    Rotor_z = math.ceil(math.pi * Rotor_Dm / Rotor_t)  # 动叶叶片数

    data_list.Stator_Beta1_g_tmp.append(Stator_Beta1_g)
    data_list.Rotor_Beta1_g_tmp.append(Rotor_Beta1_g)
    data_list.Stator_Beta2_g_tmp.append(Stator_Beta2_g)
    data_list.Rotor_Beta2_g_tmp.append(Rotor_Beta2_g)
    data_list.Stator_Gamma_tmp.append(Stator_Gamma)
    data_list.Rotor_Gamma_tmp.append(Rotor_Gamma)
    data_list.Stator_Cmax_tmp.append(Stator_Cmax)
    data_list.Rotor_Cmax_tmp.append(Rotor_Cmax)
    data_list.Stator_r1_tmp.append(Stator_r1)
    data_list.Rotor_r1_tmp.append(Rotor_r1)
    data_list.Stator_r2_tmp.append(Stator_r2)
    data_list.Rotor_r2_tmp.append(Rotor_r2)
    data_list.Stator_t_tmp.append(Stator_t)
    data_list.Rotor_t_tmp.append(Rotor_t)
    data_list.Stator_z_tmp.append(Stator_z)
    data_list.Rotor_z_tmp.append(Rotor_z)
    data_list.Stator_B_tmp.append(Stator_B)
    data_list.Rotor_B_tmp.append(Rotor_B)

    return [
        geom_parameter2blade(Stator_Beta1_g, Stator_Beta2_g, Stator_Gamma, Stator_r1, Stator_r2, Stator_B, Stator_l2,
                             Stator_Dm, Stator_t, False),
        geom_parameter2blade(Rotor_Beta1_g, Rotor_Beta2_g, Rotor_Gamma, Rotor_r1, Rotor_r2, Rotor_B, Rotor_l2,
                             Rotor_Dm, Rotor_t, True)]


def geom_parameter2blade(beta1, beta2, gamma, r1, r2, b, l2, dm, t, opt):
    # beta1：进口几何角 beta2：出口几何角 gamma：安装角 r1：前缘半径 r2：尾缘半径 b：叶片宽度 l2：叶高 dm:平均直径 t：节距 opt：False静叶 True动叶

    control_point = calcu.angle_to_cp(beta1, beta2, gamma, b, opt)
    hub = dm / 2 - l2 / 2
    shroud = dm / 2 + l2 / 2
    return [control_point, [hub, shroud], [r1, r2], t]
    # 返回 弧度曲线，[hub,shroud]，[前缘,尾缘]，截距
