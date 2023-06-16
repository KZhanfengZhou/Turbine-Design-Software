# coding=gbk
# 计算动叶进口的部分参数，进口气流角、进口马赫数、进口压力、进口温度。输入参数为静叶的
from optimize.KO_loss import KO_loss
import math
from design_calculation import data_list


def compRotorin(alpha1=None, alpha2=None, k=None, Re=None, ia=None, cons=None, tD=None, Bz=None, t_MAX=None, P_in=None,
                P_out=None, T_in=None, Ma_in=None, Ma_out=None, r_hub=None, r_tip=None, n=None):  # 改改，删除o=None,换成尾缘直径
    # alpha1: 进口气流角(静叶)
    # Stator_alpha2: 出口气流角(静叶)
    # k: 气体绝热指数
    # Re:雷诺数
    # cons 叶片稠度，1.0~1.4， 默认1.2
    # ia 攻角，-2~-6，默认-2
    # o: 喉部宽度 mm, 若忽略叶顶间隙损失，则o为多余变量
    # Bz: 轴向弦长 mm (叶宽)
    # t_MAX: 最大叶型厚度 mm
    # P_in, P_out: 进出口压力 Pa (静叶)
    # T_in：进口温度
    # Ma_in, Ma_out: 进出口马赫数 (静叶)
    # r_hub, r_tip: 轮毂和端盖的半径 mm (静叶)
    # l: 叶高 mm
    # n: 转速 rpm
    # 计算都是基于理想气体，实际气体计算时需要查表
    # R = 286.96  # 气体常数
    cp = k / (k - 1) * data_list.R  # 等压比热
    h1_ds = k / (k - 1) * data_list.R * T_in * (1 - (P_out / P_in) ** ((k - 1) / k))  # 静叶等熵焓降
    h1 = h1_ds * (1 - KO_loss(alpha1, alpha2, k, Re, ia, cons, tD, Bz, t_MAX, P_in, P_out, T_in, Ma_in, Ma_out, r_hub,
                              r_tip))  # 静叶实际焓降
    c1 = math.sqrt(2 * h1)  # 静叶出口实际速度
    rs = (r_hub + r_tip) / 2  # 静叶半径
    u1 = math.pi * 2 * rs * n / 60000  # 静叶出口圆周速度
    alpha2 = math.radians(alpha2)
    w1 = math.sqrt(c1 ** 2 + u1 ** 2 - 2 * u1 * c1 * math.cos(alpha2))  # 静叶出口相对速度
    alpha1r = math.atan(c1 * math.sin(alpha2) / (c1 * math.cos(alpha2) - u1))
    T1s = T_in * (P_out / P_in) ** ((k - 1) / k)  # 静叶出口等熵静温
    T1 = T1s + (h1_ds - h1) / cp  # 静叶出口实际静温
    alpha1r = math.degrees(alpha1r)
    Mar_in = w1 / math.sqrt(k * data_list.R * T1)  # 动叶进口相对马赫数
    Pr_in = P_out  # 动叶进口压力
    Tr_in = T1  # 动叶进口温度
    return alpha1r, Mar_in, Pr_in, Tr_in
