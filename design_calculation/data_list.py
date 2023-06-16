import numpy as np

# 压力单位 Pa
# 温度单位 K
# 焓单位 kJ/kg
# 流量单位 kg
# 转速单位 rpm

# 数据准备
G = 53.691  # 进口流量，给定，需外部输入 asdf
pt0 = 17.2 * 10 ** 5  # 进口总压，给定，需外部输入
Tt0 = 1330  # 进口总温，给定，需外部输入
pz = 4.54 * 10 ** 5  # 出口静压，给定，需外部输入
Efft0 = 0.865  # 滞止效率，预先设定，后面要用到
Eff = 0.88  # 效率同样需要外部输入
Maz = 0.366  # 末级出口马赫数，选定
n = 12637  # 转速，给定或选定 asdf
k = 1.33  # 绝热指数，给定
R = 287.25  # 气体常数，给定

omaga = 0.357  # 末级反动度，选取
xaz = 0.586  # 末级速度比，选取

alph2z = 90  # 末级出口角，轴向出气，为90度
faiz = 0.5  # 叶片减扭系数，选定，一般为0.48~0.54
rouz = 8.4 * 10 ** 8  # 金属材料密度，由动叶材料定，kg/m3
taoz = 200  # 叶片适用寿命，选取，h
fRz_z = 500  # 材料持久强度，查取

Ttic = 743.9  # 冷却空气参数总温，给定
ptic = 17.96 * 10 ** 5  # 冷却空气总压，给定
kic = 1.4
Ric = 286.96

Gc = None
crc = None

# One_dimensional_Design_1xbz中的数据
Tt0M = None
pt0M = None
hsM = None  # 级等熵焓降
Dm1M = None
alph1M = None
ysM = None
um1M = None
c_soundM = None
p2M = None
caM = None
omagaM = None
hcM = None
h1sM = None
c1sM = None
c1M = None
c1uM = None
c1zM = None
Tt1_mixM = None
c_sound_mixM = None
Lamda1M = None
T1_mixM = None
p1M = None
Density1M = None
G1M = None
A1M = None
l1M = None
w1uM = None
w1zM = None
Beta1M = None
Gc2M = None
Ttc2M = None
ptc2M = None
kc2M = None
Rc2M = None
cpc2M = None
wrc2M = None
Grc2M = None
w1M = None
Tt11_mixM = None
c1_sound_mixM = None
Lamda11M = None
pt1M = None
Dm2M = None
um2M = None
Beta2M = None
yRM = None
w2sM = None
R_Tt2M = None
w2M = None
Tt2_mixM = None
c2_sound_mixM = None
Lamda12M = None
T2_mixM = None
Density2M = None
G2M = None
l2M = None
A2M = None
ThM = None
w2uM = None
w2zM = None
c2zM = None
c2uM = None
alph12M = None
c2M = None
Tt2M = None
c2_soundM = None
Ma2M = None
pt2M = None
faiM = None
rouM = None
taoM = None
fRM = None
fREM = None
fR1M = None
KM = None
H_to_W1M = None
H_to_W2M = None
Bz1M = None
Bz2M = None
ACM = None
LM = None
YM = []
Dh1M = None  # 等内径参数
Dh2M = None
omagahM = None

Z_num = 1  # 叶片级数


def One_dimension_init(blade_stage):
    global Tt0M
    global pt0M
    global hsM  # 级等熵焓降
    global Dm1M
    global alph1M
    global ysM
    global um1M
    global c_soundM
    global p2M
    global caM
    global omagaM
    global hcM
    global h1sM
    global c1sM
    global c1M
    global c1uM
    global c1zM
    global Tt1_mixM
    global c_sound_mixM
    global Lamda1M
    global T1_mixM
    global p1M
    global Density1M
    global G1M
    global A1M
    global l1M
    global w1uM
    global w1zM
    global Beta1M
    global Gc2M
    global Ttc2M
    global ptc2M
    global kc2M
    global Rc2M
    global cpc2M
    global wrc2M
    global Grc2M
    global w1M
    global Tt11_mixM
    global c1_sound_mixM
    global Lamda11M
    global pt1M
    global Dm2M
    global um2M
    global Beta2M
    global yRM
    global w2sM
    global R_Tt2M
    global w2M
    global Tt2_mixM
    global c2_sound_mixM
    global Lamda12M
    global T2_mixM
    global Density2M
    global G2M
    global l2M
    global A2M
    global ThM
    global w2uM
    global w2zM
    global c2zM
    global c2uM
    global alph12M
    global c2M
    global Tt2M
    global c2_soundM
    global Ma2M
    global pt2M
    global faiM
    global rouM
    global taoM
    global fRM
    global fREM
    global fR1M
    global KM
    global H_to_W1M
    global H_to_W2M
    global Bz1M
    global Bz2M
    global ACM
    global LM
    global YM
    global Dh1M
    global Dh2M
    global omagahM


    Tt0M = np.zeros(blade_stage)
    pt0M = np.zeros(blade_stage)
    hsM = np.zeros(blade_stage)  # 级等熵焓降
    Dm1M = np.zeros(blade_stage)
    alph1M = np.zeros(blade_stage)
    ysM = np.zeros(blade_stage)
    um1M = np.zeros(blade_stage)
    c_soundM = np.zeros(blade_stage)
    p2M = np.zeros(blade_stage)
    caM = np.zeros(blade_stage)
    omagaM = np.zeros(blade_stage)
    hcM = np.zeros(blade_stage)
    h1sM = np.zeros(blade_stage)
    c1sM = np.zeros(blade_stage)
    c1M = np.zeros(blade_stage)
    c1uM = np.zeros(blade_stage)
    c1zM = np.zeros(blade_stage)
    Tt1_mixM = np.zeros(blade_stage)
    c_sound_mixM = np.zeros(blade_stage)
    Lamda1M = np.zeros(blade_stage)
    T1_mixM = np.zeros(blade_stage)
    p1M = np.zeros(blade_stage)
    Density1M = np.zeros(blade_stage)
    G1M = np.zeros(blade_stage)
    A1M = np.zeros(blade_stage)
    l1M = np.zeros(blade_stage)
    w1uM = np.zeros(blade_stage)
    w1zM = np.zeros(blade_stage)
    Beta1M = np.zeros(blade_stage)
    Gc2M = np.zeros(blade_stage)
    Ttc2M = np.zeros(blade_stage)
    ptc2M = np.zeros(blade_stage)
    kc2M = np.zeros(blade_stage)
    Rc2M = np.zeros(blade_stage)
    cpc2M = np.zeros(blade_stage)
    wrc2M = np.zeros(blade_stage)
    Grc2M = np.zeros(blade_stage)
    w1M = np.zeros(blade_stage)
    Tt11_mixM = np.zeros(blade_stage)
    c1_sound_mixM = np.zeros(blade_stage)
    Lamda11M = np.zeros(blade_stage)
    pt1M = np.zeros(blade_stage)
    Dm2M = np.zeros(blade_stage)
    um2M = np.zeros(blade_stage)
    Beta2M = np.zeros(blade_stage)
    yRM = np.zeros(blade_stage)
    w2sM = np.zeros(blade_stage)
    R_Tt2M = np.zeros(blade_stage)
    w2M = np.zeros(blade_stage)
    Tt2_mixM = np.zeros(blade_stage)
    c2_sound_mixM = np.zeros(blade_stage)
    Lamda12M = np.zeros(blade_stage)
    T2_mixM = np.zeros(blade_stage)
    Density2M = np.zeros(blade_stage)
    G2M = np.zeros(blade_stage)
    l2M = np.zeros(blade_stage)
    A2M = np.zeros(blade_stage)
    ThM = np.zeros(blade_stage)
    w2uM = np.zeros(blade_stage)
    w2zM = np.zeros(blade_stage)
    c2zM = np.zeros(blade_stage)
    c2uM = np.zeros(blade_stage)
    alph12M = np.zeros(blade_stage)
    c2M = np.zeros(blade_stage)
    Tt2M = np.zeros(blade_stage)
    c2_soundM = np.zeros(blade_stage)
    Ma2M = np.zeros(blade_stage)
    pt2M = np.zeros(blade_stage)
    faiM = np.zeros(blade_stage)
    rouM = np.zeros(blade_stage)
    taoM = np.zeros(blade_stage)
    fRM = np.zeros(blade_stage)
    fREM = np.zeros(blade_stage)
    fR1M = np.zeros(blade_stage)
    KM = np.zeros(blade_stage)
    H_to_W1M = np.zeros(blade_stage)
    H_to_W2M = np.zeros(blade_stage)
    Bz1M = np.zeros(blade_stage)
    Bz2M = np.zeros(blade_stage)
    ACM = np.zeros(blade_stage)
    LM = np.zeros(blade_stage)
    YM = np.zeros(blade_stage)
    Dh1M = np.zeros(blade_stage)
    Dh2M = np.zeros(blade_stage)
    omagahM = np.zeros(blade_stage)


# Radial_gas_parameter_distribution中的数据
# 只保存了需要向Profile_2D_parameters中传的数据
Zr = -1

alpha1i = []  # 绝对速度方向角，静叶出口气流角 asdfg
Beta1i = []  # 相对速度方向角，动叶进口气流角 asdfg
Beta2i = []  # 相对速度方向角，动叶出口气流角，asdfg
c1i = []
c2i = []
w1i = []
w2i = []
T1i = []
p1i = []
G1i = []
alpha2i = []
Tt2 = []
T2i = []
Ma_c2i = []
p2i = []
pt2i = []
Radial_omega = []

stacking_line = []

Stator_Beta1_g_tmp = []
Rotor_Beta1_g_tmp = []
Stator_Beta2_g_tmp = []
Rotor_Beta2_g_tmp = []
Stator_Gamma_tmp = []
Rotor_Gamma_tmp = []
Stator_Cmax_tmp = []
Rotor_Cmax_tmp = []
Stator_r1_tmp = []
Rotor_r1_tmp = []
Stator_r2_tmp = []
Rotor_r2_tmp = []
Stator_t_tmp = []
Rotor_t_tmp = []
Stator_z_tmp = []
Rotor_z_tmp = []
Stator_B_tmp = []
Rotor_B_tmp = []

Stator_Beta1_g = []
Rotor_Beta1_g = []
Stator_Beta2_g = []
Rotor_Beta2_g = []
Stator_Gamma = []
Rotor_Gamma = []
Stator_Cmax = []
Rotor_Cmax = []
Stator_r1 = []
Rotor_r1 = []
Stator_r2 = []
Rotor_r2 = []
Stator_t = []
Rotor_t = []
Stator_z = []
Rotor_z = []
Stator_B = []
Rotor_B = []

init_fitness = []

optimize_flag = -1
optimize_result = []
optimize_fitness = []

blade_layout_method = 1  # 0等中径 1等内径
