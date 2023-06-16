import copy

import numpy as np
import math

# 这是一个给定曲线，返回n等分点及其对应法向量的函数
# 曲线按照从头到尾散点给出
# 头尾部控制点也需要法向分布
from blade_geometry import calcu


def curve_distance(array, dis):
    array = array[::-1]  # 反向，从尾缘开始算
    m = len(array[:, 0])
    point = np.zeros((1, 2), float)
    k = np.zeros((1, 2), float)
    s = 0
    e = np.zeros((m - 1, 1), float)
    j = 0
    for i in range(0, m - 1):
        e[i] = calcu.distance(array[i, 0], array[i, 1], array[i + 1, 0], array[i + 1, 1])
        s = s + e[i]
        dis = dis - e[i]
        if dis < 0:
            dis = dis + e[i]
            ratio = dis / e[i]
            point[0, 0] = array[i, 0] + ratio * (array[i + 1, 0] - array[i, 0])
            point[0, 1] = array[i, 1] + ratio * (array[i + 1, 1] - array[i, 1])
            point_k = np.zeros((2, 2), float)
            point_k[0] = array[i]
            point_k[1] = array[i + 1]
            k = slope(point_k)
            return point, k
    return None


def poin(Array, n):
    m = len(Array[:, 0])
    point = np.zeros((n + 1, 2), float)
    k = np.zeros((n + 1, 2), float)
    point[0] = Array[0]
    point[n] = Array[m - 1]
    point_k0 = np.zeros((2, 2), float)
    point_k0[0] = Array[0]
    point_k0[1] = Array[1]
    k[0] = slope(point_k0)
    point_k1 = np.zeros((2, 2), float)
    point_k1[0] = Array[m - 2]
    point_k1[1] = Array[m - 1]
    k[n] = slope(point_k1)
    js = np.zeros((n + 1, 1), int)
    js[0] = 0
    js[n] = m - 1
    s = 0
    e = np.zeros((m - 1, 1), float)
    j = 0
    for i in range(0, m - 1):
        e[i] = calcu.distance(Array[i, 0], Array[i, 1], Array[i + 1, 0], Array[i + 1, 1])
        s = s + e[i]
    s_n = 0
    for i in range(0, n - 1):
        s_n = s_n + s / n
        while s_n > e[j]:
            s_n = s_n - e[j]
            j = j + 1
        ratio = s_n / e[j]
        js[i + 1] = j
        point[i + 1, 0] = Array[j, 0] + ratio * (Array[j + 1, 0] - Array[j, 0])
        point[i + 1, 1] = Array[j, 1] + ratio * (Array[j + 1, 1] - Array[j, 1])
        point_k = np.zeros((2, 2), float)
        point_k[0] = Array[j]
        point_k[1] = Array[j + 1]
        k[i + 1] = slope(point_k)
    return point, k, js


def slope(array):  # 求法向向量
    m = len(array[:, 0])
    if array[0, 0] - array[m - 1, 0] == 0:
        k = [1, 0]
    else:
        if array[0, 1] - array[m - 1, 1] == 0:
            k = [0, 1]
        else:
            k = [1, -1 / ((array[0, 1] - array[m - 1, 1]) / (array[0, 0] - array[m - 1, 0]))]
    return np.array(k) / calcu.distance(0, 0, k[0], k[1])


def d_distance(array, n):
    m = len(array[:, 0])
    s = 0
    for i in range(0, m - 1):
        s = s + calcu.distance(array[i, 0], array[i, 1], array[i + 1, 0], array[i + 1, 1])
    s_n = s / n
    return s_n


def r_distance(array, point1, TE_radius):  # 求比距离，point1是一组点
    m = len(point1[:, 0])
    r2 = d_distance(array, m - 1)
    point2, k, js = poin(array, m - 1)
    e1 = np.zeros((2, 2), float)
    r_d = np.zeros(m, float)
    for i in range(0, m - 1):
        e1[0] = point1[i]
        e1[1] = point2[i]
        r1 = calcu.distance(e1[0][0], e1[0][1], e1[1][0], e1[1][1])
        r_d[i] = r1 / r2
    tp, tk = curve_distance(array, TE_radius)
    r_d[m - 1] = calcu.distance(tp[0][0], tp[0][1], point1[-1][0], point1[-1][1]) / r2
    return r_d


# 快速排斥实验，判断线段ab和线段cd是否不相交,不相交返回False，不能判断不相交返回True
def quick_judge(a, b, c, d):
    if (max(a[0], b[0]) < min(c[0], d[0]) or
            max(c[0], d[0]) < min(a[0], b[0]) or
            max(a[1], b[1]) < min(c[1], d[1]) or
            max(c[1], d[1]) < min(a[1], b[1])):
        return False
    else:
        return True


# 求向量ab和向量cd的叉乘
def xmult(a, b, c, d):
    vectorAx = b[0] - a[0]
    vectorAy = b[1] - a[1]
    vectorBx = d[0] - c[0]
    vectorBy = d[1] - c[1]
    return (vectorAx * vectorBy - vectorAy * vectorBx)


# 判断线段ab和线段cd是否相交,相交返回True，不相交返回False
def cross(a, b, c, d):
    # 先进行快速排斥，以减小计算量
    if not quick_judge(a, b, c, d):
        return False
    # 若快速排斥无法判断，使用叉乘判断是否相交
    # 以c为公共点，分别判断向量cd到向量ca与到向量cb的方向，记为xmult1和xmult2。
    # 若ab分布于cd两侧，xmult1 * xmult2应小于0。
    # 同理若cd分布于ab两侧，xmult3 * xmult4应小于0。
    xmult1 = xmult(c, d, c, a)
    xmult2 = xmult(c, d, c, b)
    xmult3 = xmult(a, b, a, c)
    xmult4 = xmult(a, b, a, d)
    if xmult1 * xmult2 < 0 and xmult3 * xmult4 < 0:
        return True
    else:
        return False


def rd_point(array, r_d, flag, TE_radius, num, TE_theta):  # 给定比距离求点，r_d是比距离，False为凸侧
    # n = len(r_d) - 1
    n = num + 2
    point1, k, js = poin(array, n)
    point = np.zeros((n + 1, 2), float)
    d = d_distance(array, n)
    # r0 = np.sqrt(k[0][0] * k[0][0] + k[0][1] * k[0][1])
    for i in range(0, n + 1):
        k[i] = calcu.get_side_vector(array, js[i], flag)
        r = np.sqrt(k[i][0] * k[i][0] + k[i][1] * k[i][1])
        point[i] = point1[i] + k[i] / r * r_d[i] * d
    # 尾缘控制点不在最后+补开头
    tp, tk = curve_distance(array, TE_radius)
    v1 = np.zeros(2, float)
    v2 = np.zeros(2, float)
    v1[0] = array[1, 0] - array[0, 0]
    v1[1] = array[1, 1] - array[0, 1]
    v2[0] = array[2, 0] - array[1, 0]
    v2[1] = array[2, 1] - array[1, 1]
    # t_tao = np.array([-tk[1], tk[0]])
    # t_tao不能用tk算，不然方向会有问题
    # 因为尾缘半径很小，切线不会发生突变，t_tao近似等于camber的最后一段切线
    t_tao = np.array([array[-1, 0] - tp[0, 0], array[-1, 1] - tp[0, 1]])
    last_k = calcu.to_right_orientation(tk, t_tao, v1, v2, flag)
    theta2 = (TE_theta / 2) / 180 * math.pi
    # 顺时针旋转
    last_k_o = copy.deepcopy(last_k)
    last_k_o[0] = last_k[0] * math.cos(theta2) - last_k[1] * math.sin(theta2)
    last_k_o[1] = last_k[1] * math.cos(theta2) + last_k[0] * math.sin(theta2)
    d1 = calcu.distance(0, 0, last_k_o[0], last_k_o[1])
    d2 = calcu.distance(0, 0, array[-1, 0] - array[-2, 0], array[-1, 1] - array[-2, 1])
    dot_multi = (last_k_o[0] * (array[-1, 0] - array[-2, 0]) + last_k_o[1] * (
            array[-1, 1] - array[-2, 1])) / d1 / d2
    if dot_multi < 0:  # 大于90度
        theta2 = -theta2
        last_k_o[0] = last_k[0] * math.cos(theta2) - last_k[1] * math.sin(theta2)
        last_k_o[1] = last_k[1] * math.cos(theta2) + last_k[0] * math.sin(theta2)
    point[-1] = tp + TE_radius * last_k_o
    # ret补个头就好了
    point = np.vstack((point1[0], point))
    # ret = np.vstack((ret, tp))
    k = k[:len(k) - 1]
    k = np.vstack((k, tk))
    k = np.vstack((np.array([0, 0]), k))
    return point, k, point1, last_k_o  # 返回一组点
