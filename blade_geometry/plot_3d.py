import numpy as np
from blade_geometry import calcu
from scipy.interpolate import interp1d

from blade_geometry import figure_operation

flag = False


def on_figure_enter(event):
    global flag
    flag = True


def on_figure_leave(event):
    global flag
    flag = False


npoint = 100


def plot_3d(yexing, length, fig, ax, stacking_cp=None, opt=False):  # stacking_cp 0对应高度，1对应凸起度（通常为负数 凹陷）即自己坐标中的y减少
    # 写等间距坐标轴
    global npoint
    ax.cla()
    ax.grid(False)
    # ax.axis('equal')
    # ax.set(xlim=figure_operation.x_lim_all, ylim=figure_operation.y_lim_all,
    #        zlim=(stacking_cp[0, 0], figure_operation.x_lim_all[1] - figure_operation.x_lim_all[0]))
    # ax.set_axis_off()
    if opt is False:  # 单个叶片
        if stacking_cp is None:  # 无旋转三维拉伸 无偏移 z从0到length
            z_data = np.array([[0, length] for i in range(len(yexing[:, 1]))])
            x_data = np.vstack((yexing[:, 0], yexing[:, 0])).transpose()
            y_data = np.vstack((yexing[:, 1], yexing[:, 1])).transpose()
        else:
            # stacking_cp 是3点控制点
            stacking_line = calcu.bezier_curve(stacking_cp, npoint - 1)
            tmpx = np.concatenate(([stacking_line[0, 0]], stacking_line[:, 0]))
            tmpy = np.concatenate(([stacking_line[0, 1]], stacking_line[:, 1]))
            stacking_line = np.column_stack((tmpx, tmpy))
            x_data = yexing[:, 0]
            y_data = yexing[:, 1]
            z_data = np.ones(len(yexing[:, 0])) * stacking_line[0, 0]
            for i in range(1, npoint):
                x_data = np.vstack((x_data, yexing[:, 0]))
                y_data = np.vstack((y_data, yexing[:, 1] + np.ones(len(yexing[:, 1])) * stacking_line[i, 1]))
                z_data = np.vstack((z_data, np.ones(len(yexing[:, 0])) * stacking_line[i, 0]))  # 等生成点，不等距，等距要用插值
            x_data = x_data.transpose()
            y_data = y_data.transpose()
            z_data = z_data.transpose()
        # print(x_data.shape)
        ax.plot_surface(x_data, y_data, z_data, antialiased=False, alpha=1, color='deepskyblue')
    else:  # 一组叶片
        stacking_line = calcu.bezier_curve(stacking_cp, npoint - 1)
        tmpx = np.concatenate(([stacking_cp[0, 0]], stacking_line[:, 0]))
        tmpy = np.concatenate(([stacking_cp[0, 1]], stacking_line[:, 1]))
        stacking_line = np.column_stack((tmpx, tmpy))
        internal = (stacking_cp[2, 0] - stacking_cp[0, 0]) / (len(yexing) - 1)
        ax.set(xlim=figure_operation.x_lim_max, ylim=figure_operation.y_lim_max,
               zlim=(stacking_cp[0, 0] - internal, stacking_cp[2, 0] + internal), xlabel='x', ylabel='y', zlabel='z')
        now_z = stacking_cp[0, 0]
        # x_data = yexing[k][:, 0]
        # y_data = yexing[k][:, 1]
        # z_data = np.ones(len(yexing[k][:, 0])) * stacking_line[0, 0]
        interpolate = interp1d(stacking_line[:, 0], stacking_line[:, 1], kind='linear', fill_value="extrapolate")
        for k in range(len(yexing)):
            z_data = np.array([now_z for i in range(len(yexing[k][:, 1]))])
            x_data = yexing[k][:, 0]
            delta_y = interpolate(now_z)
            y_data = yexing[k][:, 1] + np.ones(len(yexing[k][:, 1])) * delta_y

            x_data = x_data.transpose()
            y_data = y_data.transpose()
            z_data = z_data.transpose()

            # verts = [list(zip(x_data, y_data, z_data))]
            # ax.add_collection3d(Poly3DCollection(verts))
            ax.plot(x_data, y_data, z_data)

            now_z = now_z + internal
        # print(x_data.shape)
        ax.plot(np.zeros(len(stacking_line)), stacking_line[:, 1], stacking_line[:, 0])
    # , cmap = plt.get_cmap('rainbow')
    # 抗锯齿：antialiased去掉面会断裂 alpha是透明度
    # verts = [list(zip(x_data[:, 0], y_data[:, 0], z_data[:, 0]))]
    # ax.add_collection3d(Poly3DCollection(verts))
    # # facecolors之后加选颜色功能  ax.add_collection3d(Poly3DCollection(verts, facecolors='#E7C261'))
    # verts = [list(zip(x_data[:, npoint - 1], y_data[:, npoint - 1], z_data[:, npoint - 1]))]
    # ax.add_collection3d(Poly3DCollection(verts))
    fig.draw()
