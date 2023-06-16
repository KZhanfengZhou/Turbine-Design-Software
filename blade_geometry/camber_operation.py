import numpy as np

from blade_geometry import figure_operation
from blade_geometry import calcu
from blade_geometry import Slope
from blade_geometry import circle

x_lim_all = [-10, 16]
y_lim_all = [-10, 16]  # 这两个千万不要放到test6()这个函数里面 否则就失效了
x_lim_max = None
y_lim_max = None
camber = None
control_point = []
npoint = 200  # 前缘到尾缘共100点 还要再加一个首控制点进去

NN = 20  # 杨辉三角预处理阶数
lim = 1  # 这里设置一个阈值，如果距离很近，就把它添加到那个列表中去

ind = -1
x_mouse = None
y_mouse = None

press = False
lastx = 0  # 获取鼠标按下时的坐标X
lasty = 0  # 获取鼠标按下时的坐标Y

drag_switch = 0
cp_switch = 0
square_switch = 0

x_back_up = None
y_back_up = None
camber_back_up = None


def opt_plot(control_point_switch, fig, ax):
    global cp_switch, square_switch
    global x_lim_all, y_lim_all
    global control_point
    cp_switch = control_point_switch
    ax.cla()
    if square_switch == 0:  # 0是开1是关
        ax.axis('square')
    else:
        ax.axis('auto')
    ax.set(xlim=x_lim_all, ylim=y_lim_all)
    if control_point_switch == 0:
        ax.scatter(control_point[:, 0], control_point[:, 1])
    ax.plot(camber[:, 0], camber[:, 1])
    fig.draw()


def controlpoint2line(cp=None):
    global control_point
    if cp is None:
        cp = control_point
    camber = calcu.bezier_curve(cp, npoint - 1)
    xp = np.concatenate(([cp[0, 0]], camber[:, 0]))
    yp = np.concatenate(([cp[0, 1]], camber[:, 1]))
    camber = np.column_stack((xp, yp))
    return camber


def sym_figure(camber_back_up):
    pp_init = Slope.r_distance(camber_back_up, figure_operation.pp[1:], figure_operation.TE_radius)
    ps_init = Slope.r_distance(camber_back_up, figure_operation.ps[1:], figure_operation.TE_radius)
    figure_operation.pp, figure_operation.slope_p = figure_operation.get_origin_control_point(
        figure_operation.num_p, False, pp_init)  # 新建项目时用这个
    figure_operation.ps, figure_operation.slope_s = figure_operation.get_origin_control_point(
        figure_operation.num_s, True, ps_init)

    figure_operation.re_p = calcu.bezier_curve(figure_operation.pp, figure_operation.npoint - 1)
    xp = np.concatenate(([figure_operation.pp[0, 0]], figure_operation.re_p[:, 0]))
    yp = np.concatenate(([figure_operation.pp[0, 1]], figure_operation.re_p[:, 1]))
    figure_operation.re_p = np.column_stack((xp, yp))

    figure_operation.re_s = calcu.bezier_curve(figure_operation.ps, figure_operation.npoint - 1)
    xs = np.concatenate(([figure_operation.ps[0, 0]], figure_operation.re_s[:, 0]))
    ys = np.concatenate(([figure_operation.ps[0, 1]], figure_operation.re_s[:, 1]))
    figure_operation.re_s = np.column_stack((xs, ys))

    c21, c22 = circle.circle(8, figure_operation.pp[-1], figure_operation.ps[-1], 20,
                             figure_operation.re_p[-2])
    c21 = c21[::-1]
    c22 = c22[::-1]
    c21 = np.delete(c21, 0, 0)
    c22 = np.delete(c22, 0, 0)
    figure_operation.c21 = c21
    figure_operation.c22 = c22

    # 都是先加尾缘再算中弧线
    figure_operation.re_p = np.concatenate([figure_operation.re_p, c21], axis=0)
    figure_operation.re_s = np.concatenate([figure_operation.re_s, c22], axis=0)

    figure_operation.x_lim_max, figure_operation.y_lim_max = calcu.get_max_range(figure_operation.re_p,
                                                                                 figure_operation.re_s,
                                                                                 figure_operation.pp,
                                                                                 figure_operation.ps)
    figure_operation.x_lim_all = figure_operation.x_lim_max
    figure_operation.y_lim_all = figure_operation.y_lim_max
    figure_operation.meanline = calcu.meanline(figure_operation.re_p[:, 0], figure_operation.re_s[:, 0],
                                               figure_operation.re_p[:, 1], figure_operation.re_s[:, 1],
                                               figure_operation.npoint)
    figure_operation.opt_plot(figure_operation.camber_switch, figure_operation.cp_switch)


def auto_plot(fig, ax):
    global x_lim_all, y_lim_all
    global x_lim_max, y_lim_max
    global camber
    global control_point
    global cp_switch
    calcu.yh_sanjiao(NN)  # warning: 杨辉三角预处理阶数最好写一个自适应！
    # 先读取一群点，把点画出来
    ax.set_xlim(x_lim_all)  # 坐标系x轴范围
    ax.set_ylim(y_lim_all)  # 坐标系y轴范围
    camber = controlpoint2line()
    x_lim_max, y_lim_max = calcu.get_max_range(camber, control_point)
    x_lim_all = x_lim_max
    y_lim_all = y_lim_max
    opt_plot(cp_switch, fig, ax)
    # 忽略除以0的报错
    np.seterr(divide='ignore', invalid='ignore')

    # 鼠标点击事件  函数里面又绑定了一个鼠标移动事件，所以生成的效果是鼠标按下并且移动的时候
    # 点一下选定一个点
    def on_button_press(event):
        global ind
        global x_mouse, y_mouse
        global control_point
        global press, lastx, lasty
        global x_back_up, y_back_up, camber_back_up
        global camber
        min_dis = 100000
        if event.inaxes is not None:  # 判断鼠标是否在axes内
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
                ind = -1
                # 计算一下鼠标的位置和图上点的位置距离，如果距离很近就移动图上那个点
                for i in range(len(control_point[:, 0])):
                    # 计算一下距离 图上每个点都和鼠标计算一下距离
                    # 这里有一个bug，当鼠标带着点移到最旁边时，应该是自动缩放，但这里没有处理，而是直接使用None去计算，结果就是报错！！！
                    d = calcu.distance(x_mouse, y_mouse, control_point[i, 0], control_point[i, 1])
                    if d < lim:  # 这里设置一个阈值，如果距离很近，就把它添加到那个列表中去
                        # warning: 这个阈值很重要，不能大不能小，最好写一个自适应程序
                        # 太大确定不了选的是哪个点，太小会让鼠标一动就跟丢。最好就是点下去之后那个点就锁定！
                        if d < min_dis:
                            ind = i
                            min_dis = d
                x_back_up = control_point[ind, 0]
                y_back_up = control_point[ind, 1]
                camber_back_up = camber
            elif event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                press = True
                lastx = event.xdata  # 获取鼠标按下时的坐标X
                lasty = event.ydata  # 获取鼠标按下时的坐标Y

    # on_button_move 鼠标移动事件
    def on_button_move(event):
        global camber
        global control_point
        global cp_switch
        global lim, ind
        global x_mouse, y_mouse
        global x_lim_all, y_lim_all
        global x_lim_max, y_lim_max
        current_ax = event.inaxes
        x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
        if current_ax is not None:
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                if ind != -1 and cp_switch != 1:  # 如果ind里面有元素，说明当前鼠标的位置距离图上的一个点很近
                    # 通过索引ind[0]去改变当前这个点的坐标，新坐标是当前鼠标的横纵坐标（这样给人的感觉就是这个点跟着鼠标动了）
                    control_point[ind, 1] = y_mouse
                    control_point[ind, 0] = x_mouse
                    # 然后根据所有点拟合出来一个b样条方程
                    camber = controlpoint2line()
                    current_ax.set(xlim=x_lim_all, ylim=y_lim_all)
                    x_lim_max, y_lim_max = calcu.get_max_range(camber, control_point)
                    opt_plot(cp_switch, fig, ax)
            elif event.button == 1:
                if press and drag_switch != 1:  # 按下状态
                    # 计算新的坐标原点并移动
                    # 获取当前最新鼠标坐标与按下时坐标的差值
                    x = x_mouse - lastx
                    y = y_mouse - lasty
                    # 获取当前原点和最大点的4个位置
                    x_min, x_max = event.inaxes.get_xlim()
                    y_min, y_max = event.inaxes.get_ylim()

                    x_min = x_min - x
                    x_max = x_max - x
                    y_min = y_min - y
                    y_max = y_max - y
                    x_lim_all = [x_min, x_max]
                    y_lim_all = [y_min, y_max]
                    opt_plot(cp_switch, fig, ax)

    def on_button_release(event):
        global ind
        global x_back_up, y_back_up
        global camber_back_up
        global press
        if press is False:  # 不是拖动操作,对弧度曲线进行了更改
            # 备份操作
            tmp_opt = [ind, x_back_up, y_back_up]
            if len(figure_operation.back_up_series) <= figure_operation.back_up_now_pos:
                figure_operation.back_up_series.append(tmp_opt)
                figure_operation.back_up_now_pos = figure_operation.back_up_now_pos + 1
            else:
                figure_operation.back_up_series[figure_operation.back_up_now_pos] = tmp_opt
                figure_operation.back_up_now_pos = figure_operation.back_up_now_pos + 1
            sym_figure(camber_back_up)
        else:
            press = False
        ind = -1

    def enlarge(event):
        global x_lim_all
        global y_lim_all
        x, y = event.xdata, event.ydata
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

        fig.draw()

    fig.mpl_connect('button_press_event', on_button_press)  # 鼠标点击事件
    fig.mpl_connect('button_release_event', on_button_release)  # 鼠标松开
    fig.mpl_connect('motion_notify_event', on_button_move)
    fig.mpl_connect('scroll_event', enlarge)  # 鼠标滚轮滚动事件
