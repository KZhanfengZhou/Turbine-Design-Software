import numpy as np

from blade_geometry import calcu

x_lim_all = [-10, 16]
y_lim_all = [-10, 16]  # 这两个千万不要放到test6()这个函数里面 否则就失效了
x_lim_max = None
y_lim_max = None
camber = None
control_point = []
cnt = 0
npoint = 200  # 前缘到尾缘共100点 还要再加一个首控制点进去

NN = 4  # 杨辉三角预处理阶数
x_mouse = None
y_mouse = None

press = False
lastx = 0  # 获取鼠标按下时的坐标X
lasty = 0  # 获取鼠标按下时的坐标Y
flag = 0  # 标记点击了图像，需要更新文本框内容


def opt_plot(fig, ax):
    global x_lim_all, y_lim_all
    global control_point
    ax.cla()
    ax.axis('square')
    ax.set(xlim=x_lim_all, ylim=y_lim_all)
    np_control_point = np.array(control_point)
    ax.scatter(np_control_point[:, 0], np_control_point[:, 1])
    if len(control_point) == 3:
        controlpoint2line()
        ax.plot(camber[:, 0], camber[:, 1])
    fig.draw()


def controlpoint2line():
    global camber
    global control_point
    np_control_point = np.array(control_point)
    camber = calcu.bezier_curve(np_control_point, npoint - 1)
    xp = np.concatenate(([np_control_point[0, 0]], camber[:, 0]))
    yp = np.concatenate(([np_control_point[0, 1]], camber[:, 1]))
    camber = np.column_stack((xp, yp))


def confirm_opt(final_x, final_y, fig, ax):
    global cnt
    global control_point
    if len(control_point) > cnt:
        control_point.pop()
    control_point.append([final_x, final_y])
    cnt = cnt + 1
    opt_plot(fig, ax)


def cancel_opt(fig, ax):
    global cnt
    global control_point
    control_point.pop()
    cnt = cnt - 1
    opt_plot(fig, ax)


def auto_plot(file_name, fig, ax):
    global x_lim_all, y_lim_all
    global camber
    global control_point
    calcu.yh_sanjiao(NN)  # warning: 杨辉三角预处理阶数最好写一个自适应！
    # 先读取一群点，把点画出来
    ax.set_xlim(x_lim_all)  # 坐标系x轴范围
    ax.set_ylim(y_lim_all)  # 坐标系y轴范围
    ax.axis('square')
    # 忽略除以0的报错
    np.seterr(divide='ignore', invalid='ignore')

    # 鼠标点击事件  函数里面又绑定了一个鼠标移动事件，所以生成的效果是鼠标按下并且移动的时候
    # 点一下选定一个点
    def on_button_press(event):
        global x_mouse, y_mouse
        global control_point
        global cnt
        global press, lastx, lasty
        global flag
        if event.inaxes is not None:  # 判断鼠标是否在axes内
            if event.button == 3:  # 1、2、3分别代表鼠标的左键、中键、右键，我这里用的是鼠标中键，根据自己的喜好选择吧
                x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
                flag = 1
                if len(control_point) > cnt:
                    control_point.pop()
                    control_point.append([x_mouse, y_mouse])
                else:
                    control_point.append([x_mouse, y_mouse])
                opt_plot(fig, ax)

            elif event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                press = True
                lastx = event.xdata  # 获取鼠标按下时的坐标X
                lasty = event.ydata  # 获取鼠标按下时的坐标Y

    # on_button_move 鼠标移动事件
    def on_button_move(event):
        global camber
        global control_point
        global x_mouse, y_mouse
        global x_lim_all, y_lim_all
        current_ax = event.inaxes
        x_mouse, y_mouse = event.xdata, event.ydata  # 拿到鼠标当前的横纵坐标
        if current_ax is not None:
            if event.button == 1:
                if press:  # 按下状态
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
                    ax.set_xlim(x_lim_all)  # 坐标系x轴范围
                    ax.set_ylim(y_lim_all)  # 坐标系y轴范围
                    fig.draw()

    def on_button_release(event):
        global press
        press = False

    def enlarge(event):
        global x_lim_all
        global y_lim_all
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
