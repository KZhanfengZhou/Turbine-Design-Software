import numpy as np
from blade_geometry import calcu
from blade_geometry import Slope
from blade_geometry import camber_operation
from blade_geometry import circle

x_lim_all = [-10, 16]
y_lim_all = [-10, 16]  # 这两个千万不要放到test6()这个函数里面 否则就失效了
x_lim_max = None
y_lim_max = None

re_s = None
re_p = None
pp = None
ps = None
c21 = None
c22 = None
meanline = None
# 这两东西也要自适应
npoint = 200  # 前缘到尾缘共100点 还要再加一个首控制点进去

num_p = 0
num_s = 0  # 可调整的控制点个数
slope_p = []
slope_s = []

TE_radius = 0.072  # 尾缘半径 预设值
blade_dis = 13.3  # 节距 预设值
TE_theta = 8  # 静叶尾缘扩张角 °

NN = 20  # 杨辉三角预处理阶数

lim = 1  # 这里设置一个阈值，如果距离很近，就把它添加到那个列表中去
# 加了距离对比判断之后就能把这个稍微设置大一点了，但也不能太大，太大容易误操作

ind = -1  # 这里生成一个列表存储一下要移动的那个点
flag = -1
x_mouse = None
y_mouse = None

lastx = 0  # 获取鼠标按下时的坐标X
lasty = 0  # 获取鼠标按下时的坐标Y
press = False

camber_switch = 0
drag_switch = 0
cp_switch = 0
square_switch = 0

back_up_series = []
x_back_up = None
y_back_up = None
back_up_now_pos = 0

default_2d_fig = None
default_2d_ax = None


# default_3d_fig = None
# default_3d_ax = None

def get_TE_theta_cp(ret, k, point, last_k_o):  # 用倒数第一个和尾缘角，和倒数第二斜率 计算倒数第二个控制点位置
    k1 = -last_k_o[0] / last_k_o[1]
    k2 = k[-2][1] / k[-2][0]
    # y-ret[-1][1]=k1(x-ret[-1][0])
    # y-point[-2][1]=k2(x-point[-2][0])
    tmpx = (k1 * ret[-1][0] - k2 * point[-2][0] + point[-2][1] - ret[-1][1]) / (k1 - k2)
    tmpy = k1 * (tmpx - ret[-1][0]) + ret[-1][1]
    ret[-2][0] = tmpx
    ret[-2][1] = tmpy
    return ret


def get_origin_control_point(num, opt, init_cp_dis=None, te_radius=None,
                             te_theta=None, camber_cp=None):  # n为控制点数量，flag=0为叶背pp，flag=1为叶盆ps
    global TE_theta, TE_radius
    if te_radius is None:
        te_radius = TE_radius
    if te_theta is None:
        te_theta = TE_theta
    if camber_cp is None:
        camber = camber_operation.camber
    else:
        camber = camber_operation.controlpoint2line(camber_cp)
    if opt is False:
        if init_cp_dis is None:
            init_cp_dis = np.array(
                [0.55265057, 1.45065745, 1.9049298, 1.4, 1.2, 0.90225495, 0.5696306, 0.12181866,
                 0.03256453384853942])
        ret, k, point, last_k_o = Slope.rd_point(camber, init_cp_dis, opt, te_radius, num, te_theta)
    else:
        if init_cp_dis is None:
            init_cp_dis = np.array(
                [0.48356924, 0.64079172, 0.17364286, 0.1846661, 0.09128979, 0.05147349, 0.06818834, 0.028493967117471992
                 ])
        ret, k, point, last_k_o = Slope.rd_point(camber, init_cp_dis, opt, te_radius, num, te_theta)
    ret = get_TE_theta_cp(ret, k, point, last_k_o)
    return ret, k


def opt_plot(camber, control_point, fig=None, ax=None):
    # fig=default_fig, ax=default_ax这样是错误的
    # 默认变量仅求值并设置一次。因此，Python会创建引用的副本，从那时起，它将始终将该引用作为默认值传递。无需重新评估。
    global pp, ps
    global cp_switch, camber_switch, square_switch
    global x_lim_all, y_lim_all
    global default_2d_fig, default_2d_ax
    if fig is None and ax is None:
        fig = default_2d_fig
        ax = default_2d_ax
    cp_switch = control_point
    camber_switch = camber
    ax.cla()
    if square_switch == 0:  # 0是开1是关
        ax.axis('square')
    else:
        ax.axis('auto')
    ax.set(xlim=x_lim_all, ylim=y_lim_all)
    if control_point == 0:
        ax.scatter(pp[:, 0], pp[:, 1], color='blueviolet')  # 画成散点图
        ax.scatter(ps[:, 0], ps[:, 1], color='orange')

    ax.plot(re_p[:, 0], re_p[:, 1], color='blueviolet')
    ax.plot(re_s[:, 0], re_s[:, 1], color='orange')

    if camber == 0:
        ax.plot(meanline[:, 0], meanline[:, 1], color='green')
        # ax.plot(meanline2[:, 0], meanline2[:, 1], color='blue')  # 偏置线法
        # ax.plot(meanline3[:, 0], meanline3[:, 1], color='red')  # 近似中弧线修正法

    ax.plot(camber_operation.camber[:, 0], camber_operation.camber[:, 1], color='black')
    fig.draw()


def controlpoint2line(opt: bool):  # False 改 pp ，True 改 ps
    global c21, c22
    global re_s, re_p
    global pp, ps
    global meanline
    global camber_switch
    # 只有改变末尾控制点或者改变弧度曲线的末尾控制点才会改变c21,c22,所以这里直接不变了
    if opt is False:
        re_p = calcu.bezier_curve(pp, npoint - 1)
        xp = np.concatenate(([pp[0, 0]], re_p[:, 0]))
        yp = np.concatenate(([pp[0, 1]], re_p[:, 1]))
        re_p = np.column_stack((xp, yp))
        re_p = np.concatenate([re_p, c21], axis=0)
    else:
        re_s = calcu.bezier_curve(ps, npoint - 1)
        xs = np.concatenate(([ps[0, 0]], re_s[:, 0]))
        ys = np.concatenate(([ps[0, 1]], re_s[:, 1]))
        re_s = np.column_stack((xs, ys))
        re_s = np.concatenate([re_s, c22], axis=0)

    # meanline3 = calcu.meanline(re_p[:, 0], re_s[:, 0], re_p[:, 1], re_s[:, 1], npoint)
    # meanline2 = calcu.offset_meanline(re_p, re_s)
    if camber_switch == 0:
        meanline = calcu.binary_meanline(calcu.distance(pp[0, 0], pp[0, 1], pp[-1, 0], pp[-1, 1]), re_p, re_s)


def auto_plot(fig, ax, init_pp=None, init_ps=None):  # , fig3d, ax3d
    global x_lim_all, y_lim_all
    global x_lim_max, y_lim_max
    global re_s, re_p
    global num_p, num_s
    global meanline
    global slope_p, slope_s
    global TE_radius
    global pp, ps
    global cp_switch, camber_switch
    global c21, c22
    calcu.yh_sanjiao(NN)  # warning: 杨辉三角预处理阶数最好写一个自适应！
    # 先读取一群点，把点画出来
    num_p = 6
    num_s = 5

    if init_pp is None:
        pp, slope_p = get_origin_control_point(num_p, False)  # 新建项目时用这个
        ps, slope_s = get_origin_control_point(num_s, True)
    else:
        pp, slope_p = get_origin_control_point(num_p, False, init_pp)
        ps, slope_s = get_origin_control_point(num_s, True, init_ps)

    # ps[1, 0] = pp[0, 0] - (pp[1, 0] - pp[0, 0])  # 锁定两个点
    # ps[1, 1] = pp[0, 1] - (pp[1, 1] - pp[0, 1])

    # ps[-2, 0] = pp[-1, 0] - (pp[-2, 0] - pp[-1, 0])
    # ps[-2, 1] = pp[-1, 1] - (pp[-2, 1] - pp[-1, 1])

    re_p = calcu.bezier_curve(pp, npoint - 1)
    xp = np.concatenate(([pp[0, 0]], re_p[:, 0]))
    yp = np.concatenate(([pp[0, 1]], re_p[:, 1]))
    re_p = np.column_stack((xp, yp))

    re_s = calcu.bezier_curve(ps, npoint - 1)
    xs = np.concatenate(([ps[0, 0]], re_s[:, 0]))
    ys = np.concatenate(([ps[0, 1]], re_s[:, 1]))
    re_s = np.column_stack((xs, ys))

    c21, c22 = circle.circle(8, pp[-1], ps[-1], 20, re_p[-2])
    c21 = c21[::-1]
    c22 = c22[::-1]
    c21 = np.delete(c21, 0, 0)
    c22 = np.delete(c22, 0, 0)

    # 都是先加尾缘再算中弧线
    re_p = np.concatenate([re_p, c21], axis=0)
    re_s = np.concatenate([re_s, c22], axis=0)

    x_lim_max, y_lim_max = calcu.get_max_range(re_p, re_s, pp, ps)
    x_lim_all = x_lim_max
    y_lim_all = y_lim_max

    # meanline3 = calcu.meanline(re_p[:, 0], re_s[:, 0], re_p[:, 1], re_s[:, 1], npoint)
    # meanline2 = calcu.offset_meanline(re_p, re_s)
    meanline = calcu.binary_meanline(calcu.distance(pp[0, 0], pp[0, 1], pp[-1, 0], pp[-1, 1]), re_p, re_s)

    np.seterr(divide='ignore', invalid='ignore')  # 忽略除以0的报错
    # fig.canvas.draw_idle()
    opt_plot(camber_switch, cp_switch, fig, ax)

    # 鼠标点击事件  函数里面又绑定了一个鼠标移动事件，所以生成的效果是鼠标按下并且移动的时候
    # 点一下选定一个点

    def on_button_press(event):
        global ind, flag
        global x_mouse, y_mouse
        global press, lastx, lasty
        global x_back_up, y_back_up
        min_dis = 100000
        if event.inaxes is not None:  # 判断鼠标是否在axes内
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
                ind = -1  # 这里生成一个列表存储一下要移动的那个点
                # 计算一下鼠标的位置和图上点的位置距离，如果距离很近就移动图上那个点
                for i in range(len(pp[:, 0])):
                    # 计算一下距离 图上每个点都和鼠标计算一下距离
                    # 这里有一个bug，当鼠标带着点移到最旁边时，应该是自动缩放，但这里没有处理，而是直接使用None去计算，结果就是报错！！！
                    d = calcu.distance(x_mouse, y_mouse, pp[i, 0], pp[i, 1])
                    if d < lim:  # 这里设置一个阈值，如果距离很近，就把它添加到那个列表中去
                        if d < min_dis:
                            ind = i
                            min_dis = d
                            flag = 0

                for i in range(len(ps[:, 0])):
                    # 计算一下距离 图上每个点都和鼠标计算一下距离
                    # 这里有一个bug，当鼠标带着点移到最旁边时，应该是自动缩放，但这里没有处理，而是直接使用None去计算，结果就是报错！！！
                    d = calcu.distance(x_mouse, y_mouse, ps[i, 0], ps[i, 1])
                    if d < lim:
                        if d < min_dis:
                            # ind.append(i)
                            ind = i
                            min_dis = d
                            flag = 1
                if flag == 0:
                    x_back_up = pp[ind, 0]
                    y_back_up = pp[ind, 1]
                else:
                    x_back_up = ps[ind, 0]
                    y_back_up = ps[ind, 1]

            elif event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                press = True
                lastx = event.xdata  # 获取鼠标按下时的坐标X
                lasty = event.ydata  # 获取鼠标按下时的坐标Y

    # on_button_move 鼠标移动事件
    def on_button_move(event):
        global flag, cp_switch
        global re_s, re_p, meanline
        global lim, ind
        global x_mouse, y_mouse
        global x_lim_all, y_lim_all
        global x_lim_max, y_lim_max
        current_ax = event.inaxes
        x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
        if event.inaxes:
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                if ind != -1 and ind != 0 and cp_switch != 1:  # 如果ind里面有元素,不是前缘
                    # 通过索引ind[0]去改变当前这个点的坐标，新坐标是当前鼠标的横纵坐标（这样给人的感觉就是这个点跟着鼠标动了）
                    if flag == 0:  # 是yp，且不是
                        if ind == len(pp) - 1 or ind == len(pp) - 2:  # 如果是尾缘控制点跳过
                            return
                        if slope_p[ind, 1] / slope_p[ind, 0] <= 1 and slope_p[ind, 1] / slope_p[
                            ind, 0] >= -1:  # 当斜率不大时，x跟随鼠标
                            pp[ind, 1] = pp[ind, 1] + (x_mouse - pp[ind, 0]) / slope_p[ind, 0] * slope_p[ind, 1]
                            pp[ind, 0] = x_mouse
                        else:
                            pp[ind, 0] = pp[ind, 0] + (y_mouse - pp[ind, 1]) / slope_p[ind, 1] * slope_p[ind, 0]
                            pp[ind, 1] = y_mouse
                        # wrong!:这里强制x锁会导致斜率为很大时瞬移

                        if ind == 1 or ind == len(pp) - 2:  # 这种情况后面会舍去，所以不用写备份操作
                            ps[1, 0] = pp[0, 0] - (pp[1, 0] - pp[0, 0])
                            ps[1, 1] = pp[0, 1] - (pp[1, 1] - pp[0, 1])
                            # ps[-2, 0] = pp[-1, 0] - (pp[-2, 0] - pp[-1, 0])
                            # ps[-2, 1] = pp[-1, 1] - (pp[-2, 1] - pp[-1, 1])
                            controlpoint2line(True)
                        # 然后根据所有点拟合出来一个b样条方程
                        controlpoint2line(False)

                    elif flag == 1:
                        if ind == len(ps) - 1 or ind == len(ps) - 2:  # 如果是尾缘控制点跳过
                            return
                        if slope_s[ind, 1] / slope_s[ind, 0] <= 1 and slope_s[ind, 1] / slope_s[
                            ind, 0] >= -1:  # 当斜率不大时，x跟随鼠标
                            ps[ind, 1] = ps[ind, 1] + (x_mouse - ps[ind, 0]) / slope_s[ind, 0] * slope_s[ind, 1]
                            ps[ind, 0] = x_mouse
                        else:
                            ps[ind, 0] = ps[ind, 0] + (y_mouse - ps[ind, 1]) / slope_s[ind, 1] * slope_s[ind, 0]
                            ps[ind, 1] = y_mouse

                        if ind == 1 or ind == len(ps) - 2:  # 这种情况后面会舍去，所以不用写备份操作
                            pp[1, 0] = ps[0, 0] - (ps[1, 0] - ps[0, 0])
                            pp[1, 1] = ps[0, 1] - (ps[1, 1] - ps[0, 1])
                            # pp[-2, 0] = ps[-1, 0] - (ps[-2, 0] - ps[-1, 0])
                            # pp[-2, 1] = ps[-1, 1] - (ps[-2, 1] - ps[-1, 1])
                            controlpoint2line(False)
                        # 然后根据所有点拟合出来一个b样条方程
                        controlpoint2line(True)

                    # 拟合好了以后把曲线画出来
                    x_lim_max, y_lim_max = calcu.get_max_range(re_p, re_s, pp, ps)
                    opt_plot(camber_switch, cp_switch, fig, ax)

                    # tmp = calcu.get_centerpoint(np.vstack((re_p, re_s[-2::-1, :])))
                    # central_point_x = tmp.x
                    # central_point_y = tmp.y
                    # ax.scatter(central_point_x, central_point_y)
                    fig.draw()

            elif event.button == 1:
                if press and drag_switch != 1:  # 按下状态
                    # 计算新的坐标原点并移动
                    # 获取当前最新鼠标坐标与按下时坐标的差值
                    x = event.xdata - lastx
                    y = event.ydata - lasty
                    # 获取当前原点和最大点的4个位置
                    x_min, x_max = event.inaxes.get_xlim()
                    y_min, y_max = event.inaxes.get_ylim()

                    x_min = x_min - x
                    x_max = x_max - x
                    y_min = y_min - y
                    y_max = y_max - y
                    x_lim_all = [x_min, x_max]
                    y_lim_all = [y_min, y_max]
                    opt_plot(camber_switch, cp_switch, fig, ax)

    def on_button_release(event):
        global ind, press, flag
        global back_up_series, x_back_up, y_back_up, back_up_now_pos
        global re_s, re_p
        if press is False:  # 不是拖动屏幕操作
            # 备份操作
            tmp_opt = [flag, ind, x_back_up, y_back_up]
            if len(back_up_series) <= back_up_now_pos:
                back_up_series.append(tmp_opt)
                back_up_now_pos = back_up_now_pos + 1
            else:
                back_up_series[back_up_now_pos] = tmp_opt
                back_up_now_pos = back_up_now_pos + 1
            # plot_3d.plot_3d(np.vstack((re_p, re_s[-2::-1, :])), 10, fig3d, ax3d)
        else:
            press = False  # 鼠标松开，结束移动
        ind = -1

    def enlarge(event):
        global x_lim_all, y_lim_all
        x, y = event.xdata, event.ydata  # 这个暂时没有用上
        current_ax = event.inaxes
        xmin, xmax = current_ax.get_xlim()
        ymin, ymax = current_ax.get_ylim()
        x_step1, x_step2 = (x - xmin) / 10, (xmax - x) / 10
        y_step1, y_step2 = (y - ymin) / 10, (ymax - y) / 10

        if event.button == "up":
            # 鼠标向上滚动，缩小坐标轴刻度范围，使得图形变大
            x_lim_all = [xmin + x_step1, xmax - x_step2]
            y_lim_all = [ymin + y_step1, ymax - y_step2]
            current_ax.set(xlim=x_lim_all,
                           ylim=y_lim_all)
        if event.button == "down":
            # 鼠标向下滚动，增加坐标轴刻度范围，使得图形变小
            x_lim_all = [xmin - x_step1, xmax + x_step2]
            y_lim_all = [ymin - y_step1, ymax + y_step2]
            current_ax.set(xlim=x_lim_all,
                           ylim=y_lim_all)

        # fig.canvas.draw_idle()
        fig.draw()

    fig.mpl_connect('button_press_event', on_button_press)  # 鼠标点击事件
    fig.mpl_connect('button_release_event', on_button_release)  # 鼠标松开
    fig.mpl_connect('motion_notify_event', on_button_move)
    fig.mpl_connect('scroll_event', enlarge)  # 鼠标滚轮滚动事件
