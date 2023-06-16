import numpy as np
import math
from scipy.interpolate import interp1d
from shapely.geometry import LineString
from shapely.geometry import Polygon

import matplotlib.pyplot as plt

t = np.zeros((1, 1))


def yh_sanjiao(N):  # 直接预处理20阶 其实只要N就可以了
    # warning! : 阶数超过20需要重新写！

    global t
    t = np.zeros((N, N))
    for i in range(N):
        t[i, 0] = 1
        t[i, i] = 1
    if N >= 3:
        for i in range(2, N):
            for j in range(1, i):
                t[i, j] = t[i - 1, j - 1] + t[i - 1, j]


def bezier_curve(ctrl_point, M):  # 有没有办法用b样条求出给定一个x的y值？？？
    # 用de casteljau算法改进
    global t

    # NN = 20  # 杨辉三角预处理阶数
    # yh_sanjiao(NN)

    N = len(ctrl_point)  # 确定贝塞尔阶数（控制点个数 - 1）

    # 根据公式计算贝塞尔曲线
    re = np.zeros((M, 2))
    for i in range(1, M + 1):
        step = i / M
        for k in range(0, N):
            # print(ctrl_point.shape)
            re[i - 1, 0] = re[i - 1, 0] + (1 - step) ** (N - k - 1) * ctrl_point[k, 0] * step ** k * t[
                N - 1, k]  # t替换为nchoosek(N - 1,k)，不用计算杨辉三角了;
            re[i - 1, 1] = re[i - 1, 1] + (1 - step) ** (N - k - 1) * ctrl_point[k, 1] * step ** k * t[
                N - 1, k]  # t替换为nchoosek(N - 1,k)，不用计算杨辉三角了;

    return re


def get_max_range(re_p, re_s, pp=None, ps=None):
    if pp is None:
        maxx = [min(min(re_p[:, 0]), min(re_s[:, 0])),
                max(max(re_p[:, 0]), max(re_s[:, 0]))]
        maxy = [min(min(re_p[:, 1]), min(re_s[:, 1])),
                max(max(re_p[:, 1]), max(re_s[:, 1]))]
    else:
        maxx = [min(min(re_p[:, 0]), min(re_s[:, 0]), min(pp[:, 0]), min(ps[:, 0])),
                max(max(re_p[:, 0]), max(re_s[:, 0]), max(pp[:, 0]), max(ps[:, 0]))]
        maxy = [min(min(re_p[:, 1]), min(re_s[:, 1]), min(pp[:, 1]), min(ps[:, 1])),
                max(max(re_p[:, 1]), max(re_s[:, 1]), max(pp[:, 1]), max(ps[:, 1]))]
    # 调成正方形：
    max_range = max(maxx[1] - maxx[0], maxy[1] - maxy[0])
    x_lim_max = (maxx[0] - 0.2 * max_range, maxx[0] + max_range + 0.2 * max_range)
    y_lim_max = (maxy[0] - 0.2 * max_range, maxy[0] + max_range + 0.2 * max_range)
    return x_lim_max, y_lim_max


def linear_interp(x0_line, y0_line, x_point, opt, start_no=0):
    # opt=0 左插；opt=1 右插
    y_point = -1
    if opt == 0:
        for i in range(start_no, len(x0_line) - 1):
            if (x0_line[i] - x_point) * (x0_line[i + 1] - x_point) <= 0:  # 有交点
                k = (x_point - x0_line[i]) / (x0_line[i + 1] - x0_line[i])
                y_point = (1 - k) * y0_line[i] + k * y0_line[i + 1]
                start_no = i + 1
                break
    else:
        for i in range(len(x0_line) - 2, -1, -1):
            if (x0_line[i] - x_point) * (x0_line[i + 1] - x_point) <= 0:  # 有交点
                k = (x_point - x0_line[i]) / (x0_line[i + 1] - x0_line[i])
                y_point = (1 - k) * y0_line[i] + k * y0_line[i + 1]
                start_no = i + 1
                break
    return [start_no, y_point]


# def diff(X):
#     return [X[i + 1] - X[i] for i in range(len(X) - 1)]
def offset_meanline(re_p, re_s):
    offset_line_p = re_p
    offset_line_s = re_s
    ret = []
    x = []
    y = []
    for i in range(200):
        offset_line_p = offset(offset_line_p, 0.1)
        offset_line_s = offset(offset_line_s, -0.1)
        first_line = LineString(offset_line_s)
        second_line = LineString(offset_line_p)
        intersection = first_line.intersection(second_line)

        if intersection.geom_type == 'MultiPoint':
            # plt.plot(*LineString(intersection).xy, 'o')
            x, y = LineString(intersection).xy
        elif intersection.geom_type == 'Point':
            # plt.plot(*intersection.xy, 'o')
            x, y = intersection.xy

        for j in range(len(x)):
            ret.append([x[j], y[j]])

    ret = np.array(ret)
    ret = ret[np.lexsort(ret[:, ::-1].T)]  # 按照x排序
    return ret


def offset(Line, delta):  # 求解曲线的偏置线，输入Line，和delta,分别代表曲线和偏置距离，Line输入格式为两列数据，代表x值和y值
    # flag = -1
    # 凸面必须是-到+ 凹面
    xLine = Line[:, 0]  # 偏置曲线x值
    yLine = Line[:, 1]  # 偏置曲线y值
    k = []
    for i in range(len(xLine) - 1):
        if xLine[i + 1] - xLine[i] != 0:
            k.append((yLine[i + 1] - yLine[i]) / (xLine[i + 1] - xLine[i]))
        else:
            k.append(None)
    # k = [diff(yLine)[i] / diff(xLine)[i] for i in range(len(xLine) - 1)]  # 一阶导数 length=len-1
    # kk = [diff(k)[i] / diff(xLine)[i] for i in range(len(k) - 1)]  # 二阶导数 length=len-2
    # del (kk[-1])  # 二阶导数最后一个值删除 （不需要了）
    # r = []
    # for i in range(len(k)-1): # lenth=len-1
    #     r.append(((1 + k[i] ** 2) ** (3 / 2)) / abs(kk[i]))  # 曲线曲率半径
    # rmin = min(r)  # 最小曲线曲率半径
    knormal = []
    for i in range(len(k)):
        if k[i] != None:
            knormal.append(math.atan(-1 / k[i]))
        else:
            knormal.append(None)
    # knormal = [-1 / num for num in k]  # 法线方向 length=len-1
    # knormal = [math.atan(num) for num in knormal]  # 转化为弧度 length=len-1
    for i in range(len(knormal)):  # 由于atan函数转化为弧度，范围在-2pi~2pi，为了把范围转化到0~2pi,把所有的负值加上pi
        # print(i)
        # print(knormal[i])
        if knormal == None:
            continue
        if knormal[i] < 0:
            knormal[i] = knormal[i] + math.pi
            # if delta < 0:
            #     flag = i
        # else:
        #     if delta > 0:
        #         flag = i
    # 取两个离散点的中点向外偏置
    xLinemid = []
    yLinemid = []
    xnewLine = []
    ynewLine = []

    # print(flag)
    for i in range(len(xLine) - 1):
        xLinemid.append((xLine[i + 1] + xLine[i]) / 2)
        yLinemid.append((yLine[i + 1] + yLine[i]) / 2)
        if knormal[i] != None:
            # if i <= flag:
            xnewLine.append(xLinemid[i] - delta * math.cos(knormal[i]))
            ynewLine.append(yLinemid[i] - delta * math.sin(knormal[i]))
        # else:
        #     # print('asdf')
        #     xnewLine.append(xLinemid[i] + delta * math.cos(knormal[i]))
        #     ynewLine.append(yLinemid[i] + delta * math.sin(knormal[i]))
        # plt.cla()
        # plt.plot(xLine, yLine)
        # plt.scatter(xnewLine[i], ynewLine[i])
        # plt.scatter(xLinemid[i], yLinemid[i])
        # plt.show()
        else:
            # if i <= flag:
            xnewLine.append(xLine[i] - delta)
            ynewLine.append(yLine[i])
        # else:
        #     xnewLine.append(xLine[i] + delta)
        #     ynewLine.append(yLine[i])
    # print(len(xLinemid))
    # xLinemid = [diff(xLine)[i] / 2 + xLine[i] for i in range(len(xLine) - 1)]
    # yLinemid = [diff(yLine)[i] / 2 + yLine[i] for i in range(len(yLine) - 1)]  # length=len-1
    # xnewLine = [xLinemid[i] - delta * math.cos(knormal[i]) for i in range(len(xLinemid))]
    # ynewLine = [yLinemid[i] - delta * math.sin(knormal[i]) for i in range(len(yLinemid))]
    newLine = [[xnewLine[i], ynewLine[i]] for i in range(len(xnewLine))]
    return np.array(newLine)


def meanline(xp, xs, yp, ys, npoint):
    # 为什么会飘? 因为进来的数据，给的前缘点根本不是前缘点 通过改变控制点让上下相对于前缘点对称就能解决
    # 这里直接首尾删掉几个点
    xc0 = [(xp[i] + xs[i]) / 2 for i in range(len(xp))]  # 这只是近似的中弧线
    yc0 = [(yp[i] + ys[i]) / 2 for i in range(len(yp))]
    # plt.scatter(xc0,yc0)
    # print(xp,yp,xs,ys)

    theta0 = []
    xc = []
    yc = []
    for i in range(npoint):  # 从0到npoint-1
        if i == 0:
            theta0.append(math.atan((yc0[i + 1] - yc0[i]) / (xc0[i + 1] - xc0[i])))
        elif i == npoint - 1:
            theta0.append(math.atan((yc0[i] - yc0[i - 1]) / (xc0[i] - xc0[i - 1])))
        else:
            theta0.append(math.atan((yc0[i + 1] - yc0[i - 1]) / (xc0[i + 1] - xc0[i - 1])))

        # if theta0[i] < 0:
        #     theta0[i] = theta0[i] + math.pi

        xp1 = []
        yp1 = []
        xs1 = []
        ys1 = []
        for j in range(npoint):
            xp1.append(xp[j] * math.cos(theta0[i]) + yp[j] * math.sin(theta0[i]))  # 中弧线旋转到水平
            yp1.append(-xp[j] * math.sin(theta0[i]) + yp[j] * math.cos(theta0[i]))
            xs1.append(xs[j] * math.cos(theta0[i]) + ys[j] * math.sin(theta0[i]))
            ys1.append(-xs[j] * math.sin(theta0[i]) + ys[j] * math.cos(theta0[i]))

        xc1 = [(xp1[i] + xs1[i]) / 2 for i in range(len(xp1))]  # bug:这里要写一个在b样条中找值的函数
        # yp1i=interp1(xp1,yp1,xc1,'pchip')    # 插值到同样x座标
        # ys1i=interp1(xs1,ys1,xc1,'pchip')
        # 按顺序第一次经过的自然就是那个值啊。。。。sb！管他是不是函数
        # sb++... python有提供插值函数
        # 测试一下 线性插值 和 pchip插值的效率和准确性
        # 这里先写一个线性插值

        # 自己写差值方法，先判断两遍是否越界，先处理越界点！！！
        # try:
        #     interpolate = interp1d(xp1, yp1, kind='linear')
        #     yp1i = interpolate(xc1[i])
        # except:
        #     yp1i=yp1i
        # try:
        #     interpolate = interp1d(xs1, ys1, kind='linear')
        #     ys1i = interpolate(xc1[i])
        # except:
        #     ys1i=ys1i
        interpolate = interp1d(xp1, yp1, kind='linear', fill_value="extrapolate")
        yp1i = interpolate(xc1[i])
        interpolate = interp1d(xs1, ys1, kind='linear', fill_value="extrapolate")
        ys1i = interpolate(xc1[i])

        # if xc1[i] < xs1[0]:  # 下方左不够
        #     ys1i = calcu.linear_interp(xp1, yp1, xc1[i], 0, p_start_no)
        #     p_start_no = ys1i[0]
        #     ys1i = ys1i[1]
        #     yp1i = calcu.linear_interp(xp1, yp1, xc1[i], 0, p_start_no)[1]
        #     # print("1")
        # elif xc1[i] > xs1[-1]:  # 下方右不够
        #     ys1i = calcu.linear_interp(xp1, yp1, xc1[i], 1, p_start_no)[1]
        #     yp1i = calcu.linear_interp(xp1, yp1, xc1[i], 0, p_start_no)[1]
        #     # print("2")
        # elif xc1[i] < xp1[0]:  # 上方左不够
        #     yp1i = calcu.linear_interp(xs1, ys1, xc1[i], 0, s_start_no)
        #     s_start_no = yp1i[0]
        #     yp1i = yp1i[1]
        #     ys1i = calcu.linear_interp(xs1, ys1, xc1[i], 0, s_start_no)[1]
        #     # print("3")
        # elif xc1[i] > xp1[-1]:  # 上方右不够
        #     yp1i = calcu.linear_interp(xs1, ys1, xc1[i], 1, s_start_no)[1]
        #     ys1i = calcu.linear_interp(xs1, ys1, xc1[i], 0, s_start_no)[1]
        # else:
        #     ys1i = calcu.linear_interp(xs1, ys1, xc1[i], 0, s_start_no)[1]
        #     yp1i = calcu.linear_interp(xp1, yp1, xc1[i], 0, p_start_no)[1]
        #     # print("4")

        # 用b样条代替拟合？？是否可行？ 不可行，直接把pp当做控制点，结果虽然没问题，但是点数为100，杨辉三角需要处理100阶！
        # 这里直接用线性插值会左右溢出，因为翼型有一段往回跑的段
        # 考虑到他只关心xp1[i] yp1[i] xs1[i] ys1[i] xc1[i] 可以只计算那一个点的值

        # print(p_start_no)
        # print(s_start_no)
        # plt.cla()
        # plt.plot(xs1, ys1)
        # plt.plot(xp1, yp1)
        # plt.xlim(-1, 2)
        # plt.ylim(-1, 2)
        # plt.scatter(xc1[i], yp1i)
        # plt.scatter(xc1[i], ys1i)
        # # plt.scatter(xc1,ys1,color='blue')
        # plt.scatter(xc1[i], yc1)
        # plt.show()

        # thick0=ys1i-yp1i    # 厚度
        # thick(i)=thick0(i)
        yc1 = (ys1i + yp1i) / 2
        # if i >= 4 and i <= npoint - 2:
        xc.append(xc1[i] * math.cos(-theta0[i]) + yc1 * math.sin(-theta0[i]))  # 旋转回去得到中弧线
        yc.append(-xc1[i] * math.sin(-theta0[i]) + yc1 * math.cos(-theta0[i]))

        # plt.plot(xp, yp, color='red')
        # plt.plot(xs, ys, color='red')
        # tmpx = xc1[i] * math.cos(-theta0[i]) + yp1i * math.sin(-theta0[i])
        # tmpy = -xc1[i] * math.sin(-theta0[i]) + yp1i * math.cos(-theta0[i])
        # plt.scatter(tmpx, tmpy)
        # tmpx = xc1[i] * math.cos(-theta0[i]) + ys1i * math.sin(-theta0[i])
        # tmpy = -xc1[i] * math.sin(-theta0[i]) + ys1i * math.cos(-theta0[i])
        # plt.scatter(tmpx, tmpy)
        # plt.scatter(xc[i], yc[i])
        # plt.show()
    # x都没存所以用下面这个会错！可以把删掉的那几个x存下来。这再说
    yc[0] = (yc[2] - yc[1]) / (xc[2] - xc[1]) * (xc[0] - xc[1]) + yc[1]  # 中弧线起点
    yc[-1] = (yc[-3] - yc[-2]) / (xc[-3] - xc[-2]) * (xc[-1] - xc[-2]) + yc[-2]  # 中弧线终点
    # thick=abs(thick)       # 把厚度变为正值
    ret = []
    # ret.append([xc[0], yc[0]])
    for i in range(int(npoint / 200) + 5, len(xc)):  # 前后端异常的治标不治本的处理方法
        ret.append([xc[i], yc[i]])
    # ret.append([xc[-1], yc[-1]])
    return np.array(ret)


def distance(p1x, p1y, p2x, p2y):
    return math.sqrt((p1x - p2x) ** 2 + (p1y - p2y) ** 2)


def get_centerpoint(yexing):
    P = Polygon(yexing)
    return P.centroid


# def get_centerpoint(yexing):
#     area = 0.0
#     x, y = 0.0, 0.0
#
#     for i in range(len(yexing)):
#         lat = yexing[i, 0]  # weidu
#         lng = yexing[i, 1]  # jingdu
#
#         if i == 0:
#             lat1 = yexing[-1, 0]
#             lng1 = yexing[-1, 1]
#
#         else:
#             lat1 = yexing[i - 1, 0]
#             lng1 = yexing[i - 1, 1]
#
#         fg = (lat * lng1 - lng * lat1) / 2.0
#
#         area += fg
#         x += fg * (lat + lat1) / 3.0
#         y += fg * (lng + lng1) / 3.0
#
#     x = x / area
#     y = y / area
#
#     return x, y


def cross(v1, v2):
    return v1[0] * v2[1] - v2[0] * v1[1]


def get_vec_n(array, i):  # 单位法向量 方向还不确定
    # if i == 0:
    #     k = (array[i + 1, 1] - array[i, 1]) / (array[i + 1, 0] - array[i, 0])
    # elif i == len(array) - 1:
    #     k = (array[i, 1] - array[i - 1, 1]) / (array[i, 0] - array[i - 1, 0])
    # else:
    #     k = (array[i + 1, 1] - array[i - 1, 1]) / (array[i + 1, 0] - array[i - 1, 0])
    k = get_vec_tao(array, i)
    # k = -1 / k
    ret = np.zeros(2, float)
    ret[0] = k[1] / distance(0, 0, k[0], k[1])
    ret[1] = -k[0] / distance(0, 0, k[0], k[1])
    return ret


def get_vec_tao(array, i):  # 单位切向量
    ret = np.zeros(2, float)
    if i == len(array) - 1:
        ret[0] = array[i, 0] - array[i - 1, 0]
        ret[1] = array[i, 1] - array[i - 1, 1]
        r = distance(array[i - 1, 0], array[i - 1, 1], array[i, 0], array[i, 1])
    else:
        ret[0] = array[i + 1, 0] - array[i, 0]
        ret[1] = array[i + 1, 1] - array[i, 1]
        r = distance(array[i + 1, 0], array[i + 1, 1], array[i, 0], array[i, 1])
    ret[0] = ret[0] / r
    ret[1] = ret[1] / r
    return ret


def to_right_orientation(vec_n, vec_tao, v1, v2, opt):
    orientation = cross(vec_tao, vec_n)
    # v1->v2逆时针为正，顺时针为负
    if cross(v1, v2) < 0:  # 上凸曲线 凹点在切线顺时针方向
        if opt is False:  # 求凸点 在逆时针
            if orientation < 0:
                vec_n = -vec_n
        else:  # 求凹点 在顺时针
            if orientation > 0:
                vec_n = -vec_n
    else:
        if opt is False:  # 求凸点 在顺时针
            if orientation > 0:
                vec_n = -vec_n
        else:  # 求凹点 在逆时针
            if orientation < 0:
                vec_n = -vec_n
    return vec_n


def get_side_vector(array, i, opt):
    # 求方向正确的单位法向量
    # array是一条凸曲线 计算第i个点的法向量位置 opt为False时，返回凸侧，opt为True时返回凹侧
    # 判断曲线是上凸还是下凹 上凸曲线切线顺时针转 下凹曲线切线逆时针转
    v1 = np.zeros(2, float)
    v2 = np.zeros(2, float)
    v1[0] = array[1, 0] - array[0, 0]
    v1[1] = array[1, 1] - array[0, 1]
    v2[0] = array[2, 0] - array[1, 0]
    v2[1] = array[2, 1] - array[1, 1]

    vec_n = get_vec_n(array, i)
    vec_tao = get_vec_tao(array, i)

    vec_n = to_right_orientation(vec_n, vec_tao, v1, v2, opt)

    return vec_n


intersect_in_TE = False


def check_intersection(center_circle, radius, re_s):
    # eps=1e-3 # 距离小于这个就可以认为他们相交
    # 不能这样判断，这个eps不好确定，万一两个点刚好都大于他，但这两个点之间有一个交点，就漏了
    global intersect_in_TE
    cnt = 0
    size_enough_flag = True
    dis0 = distance(re_s[0, 0], re_s[0, 1], center_circle[0], center_circle[1])
    for i in range(1, len(re_s)):
        dis1 = distance(re_s[i, 0], re_s[i, 1], center_circle[0], center_circle[1])
        if (dis0 - radius) * (dis1 - radius) <= 0:  # 相交线定理，这两个点中有一个和圆的交点
            cnt = cnt + 1
            if i == len(re_s) - 1 and cnt == 1:  # 相交于尾缘,且只有这一个交点，如果求叶栅通道厚度，此时即可停止
                intersect_in_TE = True
        if dis0 > radius:  # 圆不够大
            size_enough_flag = False
        dis0 = dis1
    if cnt == 0:
        # 圈太大不也会没交点
        # 必须有大于半径距离的re_s上的点，且没有交点，才能说明是太小
        if size_enough_flag is False:  # 圆太小而没有交点
            return False
        else:  # 圆太大而没有交点
            return True
    else:
        return True


def check_self_intersection(center_circle, radius, re_p):
    cnt = 0
    dis0 = distance(re_p[0, 0], re_p[0, 1], center_circle[0], center_circle[1])
    for i in range(1, len(re_p)):
        dis1 = distance(re_p[i, 0], re_p[i, 1], center_circle[0], center_circle[1])
        if (dis0 - radius) * (dis1 - radius) <= 0:  # 相交线定理，这两个点中有一个和圆的交点
            cnt = cnt + 1
        dis0 = dis1
    if cnt > 1:
        return True
    else:
        return False


def Thickness_distribution(blade_dis, re_p, re_s, opt=False):  # 叶栅通道的厚度分布
    # blade_dis 节距(计算中弧线时：叶片弦长） re_p 压力面 re_s 吸力面 opt为False计算叶栅通道厚度 opt为True计算中弧线
    # re_p是一条凸曲线
    eps = blade_dis / 1000
    diameter = []
    valid_data_flag = False
    start = -1
    end = -1
    cc = []
    global intersect_in_TE
    intersect_in_TE = False
    for i in range(len(re_p)):
        left = 0
        right = blade_dis / 2 * 1.1  # 比半节距大一点
        vec_n = get_side_vector(re_p, i, opt)  # 如果求叶片的中弧线就改成True
        ans = -1
        while math.fabs(left - right) > eps:
            mid = (left + right) / 2
            center_circle = re_p[i] + vec_n * mid
            # 调试代码：
            # if i == 90:
            #     tmp.append(center_circle)
            if check_intersection(center_circle, mid, re_s):  # or check_self_intersection(center_circle, mid, re_p):
                # 如果自交，就缩小，但有可能缩的非常小才没有交点，所以，如果因为自交缩小到与s没有交点，则舍去这个点
                ans = mid
                right = mid
            else:
                left = mid
        # 排除不合理点 推测应该两头会有一串-1数据
        if ans != -1:
            if valid_data_flag is False:
                start = i
                valid_data_flag = True
            diameter.append(2 * ans)
            cc.append(re_p[i] + vec_n * ans)
            if intersect_in_TE is True and opt is False:  # 如果求的是叶栅厚度，相交且仅相交于尾缘时，即可退出
                end = i - 1
                break
            # print(i)
        elif valid_data_flag is True:
            end = i - 1
            break

    return np.array(diameter), start, end, np.array(cc)


def plot_cascade_thickness(blade_dis, re_p, re_s, re_p2, re_s2, z, zr, opt):
    fig_name = f'第{z + 1}级' + ('静叶' if opt == 0 else '动叶') + f'第{zr + 1}计算站'
    fig = plt.figure(fig_name)
    ax = fig.add_subplot(2, 1, 1)
    ax.set_title('厚度分布曲线', fontdict={'fontfamily': 'SimSun'})
    ax.set_xlabel('叶片离散点编号', fontdict={'fontfamily': 'SimSun'})
    ax.set_ylabel('厚度（内切圆直径）', fontdict={'fontfamily': 'SimSun'})
    tmp, st, end, cc = Thickness_distribution(blade_dis, re_p[:200], re_s2[:200], False)
    ax.plot(range(len(tmp)), tmp)
    ax = fig.add_subplot(2, 1, 2)
    ax.set_title('叶栅通道示意图', fontdict={'fontfamily': 'SimSun'})
    ax.plot(re_p[:, 0], re_p[:, 1], color='blue')
    ax.plot(re_p2[:, 0], re_p2[:, 1], color='red')
    ax.plot(re_s[:, 0], re_s[:, 1], color='blue')
    ax.plot(re_s2[:, 0], re_s2[:, 1], color='red')
    ax.scatter(cc[:, 0], cc[:, 1])
    ax.scatter(re_p[st:end, 0], re_p[st:end, 1])
    ax.axis('square')
    fig.subplots_adjust(hspace=0.8)
    plt.show()


def binary_meanline(blade_dis, re_p, re_s):
    waste1, waste2, waste3, ret = Thickness_distribution(
        blade_dis, re_p, re_s, True)
    # if meanline[-1]!=re_p[-1]:
    #     ...
    # 加尾缘点
    return ret


def cp_to_angle(control_point):
    beta1 = 90 - math.atan(
        (control_point[1, 1] - control_point[0, 1]) / (
                control_point[1, 0] - control_point[0, 0])) / math.pi * 180
    beta2 = 90 + math.atan(
        (control_point[2, 1] - control_point[1, 1]) / (
                control_point[2, 0] - control_point[1, 0])) / math.pi * 180
    gamma = 90 + math.atan(
        (control_point[2, 1] - control_point[0, 1]) / (
                control_point[2, 0] - control_point[0, 0])) / math.pi * 180
    return beta1, beta2, gamma


def angle_to_cp(beta1, beta2, gamma, b, opt):
    # 生成弧度曲线控制点
    # 统一角度成 弧度制 的 NUMECA形式
    beta1 = (90 - beta1) / 180 * math.pi
    beta2 = (90 - beta2) / 180 * math.pi
    # beta2 = (90 - beta2)
    gamma = (90 - gamma) / 180 * math.pi
    control_point = []
    control_point.append([0, b * math.tan(gamma)])
    tmpx = b * (math.tan(beta2) - math.tan(gamma)) / (math.tan(beta1) + math.tan(beta2))
    tmpy = -math.tan(beta2) * (tmpx - b)
    control_point.append([tmpx, tmpy])
    control_point.append([b, 0])
    control_point = np.array(control_point)
    if opt is True:
        for i in range(len(control_point)):
            control_point[i, 1] = -control_point[i, 1]

    # (0,b*tan(gamma))
    # y=tan(beta1)x+b*tan(gamma)
    # y=-tan(beta2)(x-b)
    # (b,0)
    return control_point
