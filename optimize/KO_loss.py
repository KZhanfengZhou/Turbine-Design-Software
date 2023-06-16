# coding=gbk
# ��ʧģ�ͣ�����������ʧ
import math


def KO_loss(alpha1=None, alpha2=None, k=None, Re=None, ia=None, cons=None, tD=None, Bz=None, t_MAX=None, P_in=None,
            P_out=None, T_in=None, Ma_in=None, Ma_out=None, r_hub=None, r_tip=None):  # �ĸģ�ɾ��o=None,����βԵֱ��
    # alpha1: ����������
    # Stator_alpha2: ����������
    # k: �������ָ��
    # Re:��ŵ��
    # cons ҶƬ��ȣ�1.0~1.4�� Ĭ��1.2
    # ia ���ǣ�-2~-6��Ĭ��-2
    # o: ����� mm, ������Ҷ����϶��ʧ����oΪ�������
    # Bz: �����ҳ� mm (Ҷ��)
    # t_MAX: ���Ҷ�ͺ�� mm
    # P_in, P_out: ������ѹ�� Pa
    # T_in: �����¶ȣ�K
    # Ma_in, Ma_out: �����������
    # r_hub, r_tip: ��챺Ͷ˸ǵİ뾶 mm
    # l: Ҷ�� mm
    Ba_beta = -0.2 * (90 - alpha2) + 14  # ����
    alpha2g = math.radians(alpha2 - Ba_beta)  # �ĸģ����ڼ��ν�
    E1 = 0.1078 + 0.00025441 * (90 - alpha2)  # �ĸĸ�
    E2 = - 0.1968 - 0.00060714 * (90 - alpha2)  # �ĸĸ�
    E3 = 0.0543 + 0.00153 * (90 - alpha2)  # �ĸĸ�
    E4 = 0.3125 - 0.0012646 * (90 - alpha2)  # �ĸĸ�
    E5 = - 0.7932 + 0.006766 * (90 - alpha2)  # �ĸĸ�
    E6 = 0.3901 - 0.001692 * (90 - alpha2)  # �ĸĸ�
    gammarr = math.radians(57.84 - 0.3929 * (alpha1 + ia) + 0.8221 * (alpha2 - Ba_beta))
    Beta_in = math.radians(90 - alpha1 - ia)  # �ĸģ����ν�
    alpha1 = math.radians(90 - alpha1)  # �ĸģ�����ת��������math.radians(180) ���ΪPI
    b = Bz / math.sin(gammarr)  # b: �ҳ� mm
    t = b / cons  # t: �ھ� mm
    o = t * math.sin(alpha2g)  # �ĸģ����Ӻ�����
    alpha2 = math.radians(90 - alpha2)
    l = r_tip - r_hub  # Ҷ��

    alpha_in = alpha1
    alpha_out = alpha2
    # Ҷ����ʧ
    if Re <= 200000.0:
        X_Re = (Re / 200000.0) ** (- 0.4)
    elif 200000.0 < Re <= 1000000.0:
        X_Re = 1
    else:
        X_Re = (Re / 1000000.0) ** (- 0.2)

    Y_P1 = E1 + E2 * (t / b) + E3 * (t / b) ** 2
    Y_P2 = E4 + E5 * (t / b) + E6 * (t / b) ** 2
    Y_PAMDC = (Y_P1 + abs(Beta_in / alpha_out) * (Beta_in / alpha_out) * (Y_P2 - Y_P1)) * (t_MAX / b / 0.2) ** (
            Beta_in / alpha_out)
    K_p = 1 - 1.25 * (Ma_out - 0.2) * (Ma_in / Ma_out) ** 2
    T0 = T_in * (1 + (k - 1) * Ma_in * Ma_in / 2) ** (k / (k - 1))  # �ĸĸ�
    T_out = T0 / (1 + (k - 1) * Ma_out * Ma_out / 2) ** (k / (k - 1))  # �ĸĸ�
    if Ma_in > 0.4:  # �ĸĸ�
        Y_shock = 0.75 * ((Ma_in - 0.4) ** 1.75) * (r_hub / r_tip) * (P_in / P_out) * (
                T_in / T_out)  # �ĸĸģ�������ʧ
    else:  # �ĸĸģ�������ʧ
        Y_shock = 0  # �ĸĸģ�������ʧ

    Y_p = 0.914 * (2 * Y_PAMDC * K_p / 3 + Y_shock)  # �ĸĸ�
    # ��������ʧ
    if l / b <= 2:  # չ�ұ�
        X_AR = (1 - 0.25 * math.sqrt(2 - l / b)) / (l / b)
    else:
        X_AR = b / l

    alpha_m = math.atan((math.tan(alpha1) - math.tan(alpha2)) / 2)
    x1 = tD / o  # �ĸģ��ı����x1��ʽ
    x2 = 2 * (math.tan(alpha1) + math.tan(alpha2)) * math.cos(alpha_m)
    Y_SAMDC = 0.0334 * X_AR * (math.cos(alpha_out) / math.cos(Beta_in)) * x2 ** 2 * (math.cos(alpha_out)) ** 2 / (
        math.cos(alpha_m)) ** 3
    K_S = 1 - (Bz / l) ** 2 * (1 - K_p)
    Y_S = 1.2 * Y_SAMDC * K_S
    # β����ʧ
    # x2 = t_MAX/o;
    delta_fai1 = -1.1462 * x1 ** 3 + 1.2728 * x1 ** 2 + 0.0268 * x1 - 0.0003  # �ĸ�
    delta_fai2 = -0.5107 * x1 ** 3 + 0.6161 * x1 ** 2 + 0.0238 * x1 - 0.0007  # �ĸ�
    delta_fai3 = delta_fai1 + abs(Beta_in / alpha_out) * (Beta_in / alpha_out) * (delta_fai2 - delta_fai1)  # �ĸ�

    # print(k, Ma_out, delta_fai3)
    # print(Y_TE1)
    # print(1 - (k - 1) * Ma_out ** 2 * (1 / (1 - delta_fai3 * delta_fai3) - 1) / 2)
    Y_TE1 = (1 - (k - 1) * Ma_out ** 2 * (1 / (1 - delta_fai3) - 1) / 2) ** (-k / (k - 1)) - 1  # �ĸ�
    Y_TE2 = 1 - (1 + (k - 1) * Ma_out ** 2 / 2) ** (- k / (k - 1))
    Y_TE = abs(Y_TE1 / Y_TE2)  # �ĸĸ�
    # Ҷ����϶��ʧ
    # Y_TC = 0.3*0.47*c/H*(TC/c)^0.78*x1^2*(cos(alpha_out))^2/(cos(alpha_m))^3;
    # clear x1 x2

    # ����ʧ
    Loss = abs(X_Re * Y_p + Y_S + Y_TE)
    return Loss
