import numpy as np
from blade_geometry import calcu

x_lim_all = [-10, 16]
y_lim_all = [-10, 16]  # 这两个千万不要放到test6()这个函数里面 否则就失效了
x_lim_max = None
y_lim_max = None

hub = None
shroud = None
pp = None
ps = None
# 这两东西也要自适应
npoint = 200  # 前缘到尾缘共100点 还要再加一个首控制点进去

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

drag_switch = 0
cp_switch = 0
square_switch = 0


def opt_plot(control_point, fig=None, ax=None):
    # fig=default_fig, ax=default_ax这样是错误的
    # 默认变量仅求值并设置一次。因此，Python会创建引用的副本，从那时起，它将始终将该引用作为默认值传递。无需重新评估。
    global pp, ps
    global cp_switch, square_switch
    global x_lim_all, y_lim_all
    cp_switch = control_point
    ax.cla()
    # if square_switch == 0:  # 0是开1是关
    #     ax.axis('equal')
    # else:
    #     ax.axis('auto')
    ax.set(xlim=x_lim_all, ylim=y_lim_all)
    if control_point == 0:
        ax.scatter(pp[:, 0], pp[:, 1], color='blueviolet')  # 画成散点图
        ax.scatter(ps[:, 0], ps[:, 1], color='orange')

    ax.plot(shroud[:, 0], shroud[:, 1], color='blueviolet')
    ax.plot(hub[:, 0], hub[:, 1], color='orange')

    fig.draw()


def controlpoint2line(opt: bool):  # False 改 pp ，True 改 ps
    global hub, shroud
    global pp, ps
    # 只有改变末尾控制点或者改变弧度曲线的末尾控制点才会改变c21,c22,所以这里直接不变了
    if opt is False:
        shroud = calcu.bezier_curve(pp, npoint - 1)
        xp = np.concatenate(([pp[0, 0]], shroud[:, 0]))
        yp = np.concatenate(([pp[0, 1]], shroud[:, 1]))
        shroud = np.column_stack((xp, yp))
    else:
        hub = calcu.bezier_curve(ps, npoint - 1)
        xs = np.concatenate(([ps[0, 0]], hub[:, 0]))
        ys = np.concatenate(([ps[0, 1]], hub[:, 1]))
        hub = np.column_stack((xs, ys))


def auto_plot(fig, ax, control_pp=np.array([[0, 190], [20, 190]]), control_ps=np.array([[0, 211.83], [20, 211.83]])):
    global x_lim_all, y_lim_all
    global x_lim_max, y_lim_max
    global hub, shroud
    global pp, ps
    global cp_switch
    calcu.yh_sanjiao(NN)  # warning: 杨辉三角预处理阶数最好写一个自适应！
    # 先读取一群点，把点画出来

    pp = control_pp
    ps = control_ps

    shroud = calcu.bezier_curve(pp, npoint - 1)
    xp = np.concatenate(([pp[0, 0]], shroud[:, 0]))
    yp = np.concatenate(([pp[0, 1]], shroud[:, 1]))
    shroud = np.column_stack((xp, yp))

    hub = calcu.bezier_curve(ps, npoint - 1)
    xs = np.concatenate(([ps[0, 0]], hub[:, 0]))
    ys = np.concatenate(([ps[0, 1]], hub[:, 1]))
    hub = np.column_stack((xs, ys))

    x_lim_max, y_lim_max = calcu.get_max_range(shroud, hub, pp, ps)
    x_lim_all = x_lim_max
    y_lim_all = y_lim_max

    np.seterr(divide='ignore', invalid='ignore')  # 忽略除以0的报错

    opt_plot(cp_switch, fig, ax)

    # 鼠标点击事件  函数里面又绑定了一个鼠标移动事件，所以生成的效果是鼠标按下并且移动的时候
    # 点一下选定一个点

    def on_button_press(event):
        global ind, flag
        global x_mouse, y_mouse
        global press, lastx, lasty
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

            elif event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                press = True
                lastx = event.xdata  # 获取鼠标按下时的坐标X
                lasty = event.ydata  # 获取鼠标按下时的坐标Y

    # on_button_move 鼠标移动事件
    def on_button_move(event):
        global flag, cp_switch
        global hub, shroud
        global lim, ind
        global x_mouse, y_mouse
        global x_lim_all, y_lim_all
        global x_lim_max, y_lim_max
        current_ax = event.inaxes
        x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
        if event.inaxes:
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                if ind != -1 and cp_switch != 1:  # 如果ind里面有元素,不是前缘
                    # 通过索引ind[0]去改变当前这个点的坐标，新坐标是当前鼠标的横纵坐标（这样给人的感觉就是这个点跟着鼠标动了）
                    if flag == 0:  # 是yp，且不是
                        # if ind == len(pp) - 1 or ind == len(pp) - 2:  # 如果是尾缘控制点跳过
                        #     return

                        pp[ind, 1] = y_mouse
                        pp[ind, 0] = x_mouse
                        # 然后根据所有点拟合出来一个b样条方程
                        controlpoint2line(False)

                    elif flag == 1:
                        # if ind == len(ps) - 1 or ind == len(ps) - 2:  # 如果是尾缘控制点跳过
                        #     return
                        ps[ind, 1] = y_mouse
                        ps[ind, 0] = x_mouse
                        # 然后根据所有点拟合出来一个b样条方程
                        controlpoint2line(True)

                    # 拟合好了以后把曲线画出来

                    x_lim_max, y_lim_max = calcu.get_max_range(shroud, hub, pp, ps)
                    opt_plot(cp_switch, fig, ax)

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
                    opt_plot(cp_switch, fig, ax)

    def on_button_release(event):
        global ind, press, flag
        global hub, shroud
        if press is False:  # 不是拖动屏幕操作
            # # 备份操作
            # tmp_opt = [flag, ind, x_back_up, y_back_up]
            # if len(back_up_series) <= back_up_now_pos:
            #     back_up_series.append(tmp_opt)
            #     back_up_now_pos = back_up_now_pos + 1
            # else:
            #     back_up_series[back_up_now_pos] = tmp_opt
            #     back_up_now_pos = back_up_now_pos + 1
            ...
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

        fig.draw()

    fig.mpl_connect('button_press_event', on_button_press)  # 鼠标点击事件
    fig.mpl_connect('button_release_event', on_button_release)  # 鼠标松开
    fig.mpl_connect('motion_notify_event', on_button_move)
    fig.mpl_connect('scroll_event', enlarge)  # 鼠标滚轮滚动事件
