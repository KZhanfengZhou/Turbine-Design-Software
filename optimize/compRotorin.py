# coding=gbk
# ���㶯Ҷ���ڵĲ��ֲ��������������ǡ����������������ѹ���������¶ȡ��������Ϊ��Ҷ��
from optimize.KO_loss import KO_loss
import math
from design_calculation import data_list


def compRotorin(alpha1=None, alpha2=None, k=None, Re=None, ia=None, cons=None, tD=None, Bz=None, t_MAX=None, P_in=None,
                P_out=None, T_in=None, Ma_in=None, Ma_out=None, r_hub=None, r_tip=None, n=None):  # �ĸģ�ɾ��o=None,����βԵֱ��
    # alpha1: ����������(��Ҷ)
    # Stator_alpha2: ����������(��Ҷ)
    # k: �������ָ��
    # Re:��ŵ��
    # cons ҶƬ��ȣ�1.0~1.4�� Ĭ��1.2
    # ia ���ǣ�-2~-6��Ĭ��-2
    # o: ����� mm, ������Ҷ����϶��ʧ����oΪ�������
    # Bz: �����ҳ� mm (Ҷ��)
    # t_MAX: ���Ҷ�ͺ�� mm
    # P_in, P_out: ������ѹ�� Pa (��Ҷ)
    # T_in�������¶�
    # Ma_in, Ma_out: ����������� (��Ҷ)
    # r_hub, r_tip: ��챺Ͷ˸ǵİ뾶 mm (��Ҷ)
    # l: Ҷ�� mm
    # n: ת�� rpm
    # ���㶼�ǻ����������壬ʵ���������ʱ��Ҫ���
    # R = 286.96  # ���峣��
    cp = k / (k - 1) * data_list.R  # ��ѹ����
    h1_ds = k / (k - 1) * data_list.R * T_in * (1 - (P_out / P_in) ** ((k - 1) / k))  # ��Ҷ�����ʽ�
    h1 = h1_ds * (1 - KO_loss(alpha1, alpha2, k, Re, ia, cons, tD, Bz, t_MAX, P_in, P_out, T_in, Ma_in, Ma_out, r_hub,
                              r_tip))  # ��Ҷʵ���ʽ�
    c1 = math.sqrt(2 * h1)  # ��Ҷ����ʵ���ٶ�
    rs = (r_hub + r_tip) / 2  # ��Ҷ�뾶
    u1 = math.pi * 2 * rs * n / 60000  # ��Ҷ����Բ���ٶ�
    alpha2 = math.radians(alpha2)
    w1 = math.sqrt(c1 ** 2 + u1 ** 2 - 2 * u1 * c1 * math.cos(alpha2))  # ��Ҷ��������ٶ�
    alpha1r = math.atan(c1 * math.sin(alpha2) / (c1 * math.cos(alpha2) - u1))
    T1s = T_in * (P_out / P_in) ** ((k - 1) / k)  # ��Ҷ���ڵ��ؾ���
    T1 = T1s + (h1_ds - h1) / cp  # ��Ҷ����ʵ�ʾ���
    alpha1r = math.degrees(alpha1r)
    Mar_in = w1 / math.sqrt(k * data_list.R * T1)  # ��Ҷ������������
    Pr_in = P_out  # ��Ҷ����ѹ��
    Tr_in = T1  # ��Ҷ�����¶�
    return alpha1r, Mar_in, Pr_in, Tr_in
