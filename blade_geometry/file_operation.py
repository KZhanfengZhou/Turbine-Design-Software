import math
import numpy as np
from design_calculation import data_list


# def excelinput(file_name, the_sheet_name='Sheet1'):
#     data = pd.read_excel(file_name, sheet_name=the_sheet_name)
#     return data


def txtinput(file_name):  # 从txt输入，格式 0.1,0.1回车0.2，0.2。。。
    f = open(file_name)
    pair = f.readline()
    if pair[0] == '[':
        p = [[], [], []]  # camber，pp，ps
        num = -1

        while pair:
            if pair[0] == '[':
                num = num + 1
            elif pair == '\n':
                pair = f.readline()
                continue
            else:
                if num == 0:
                    p[num].append([float(pair.split(',')[0]), float(pair.split(',')[1])])
                else:
                    p[num].append(float(pair))
            pair = f.readline()
        f.close()
        return np.array(p[0]), np.array(p[1]), np.array(p[2]), False
    else:
        # 读到当前级数就下一个
        z = int(pair[4])
        zr = int(pair[13])
        pair = f.readline()  # 空行
        pair = f.readline()  # 当前级数
        retz = []
        retppz = []
        retpsz = []
        for i in range(z):
            retzr = []  # retzr里面有zrx2组数据
            retppzr = []
            retpszr = []
            for j in range(zr):
                retzr.append([])
                retppzr.append([])
                retpszr.append([])
                # 静叶
                pair = f.readline()
                ret = []
                p = [[], [], []]  # camber，pp，ps
                num = -1
                flag = False  # 中弧线取完标志
                while True:
                    if not pair or pair[0] == '级':
                        break
                    if pair[0] == '[':
                        num = num + 1
                    elif pair == '\n':
                        pair = f.readline()
                        if num == 0:
                            if flag is False:
                                ret.append(np.array(p[0]))
                            flag = True
                        continue
                    else:
                        if num == 0:
                            if flag is False:  # 中弧线
                                p[num].append([float(pair.split(',')[0]), float(pair.split(',')[1])])
                            else:  # 其他几何参数
                                if len(pair.split(',')) == 2:
                                    ret.append([float(pair.split(',')[0]), float(pair.split(',')[1])])
                                else:
                                    ret.append(float(pair))
                        else:
                            p[num].append(float(pair))
                    pair = f.readline()

                retzr[len(retzr) - 1].append(ret)
                retppzr[len(retppzr) - 1].append(p[1])
                retpszr[len(retpszr) - 1].append(p[2])
                # 动叶
                pair = f.readline()
                ret = []
                p = [[], [], []]  # camber，pp，ps
                num = -1
                flag = False  # 中弧线取完标志
                while True:
                    if not pair or pair[0] == '级':
                        break
                    if pair[0] == '[':
                        num = num + 1
                    elif pair == '\n':
                        pair = f.readline()
                        if num == 0:
                            if flag is False:
                                ret.append(np.array(p[0]))
                            flag = True
                        continue
                    else:
                        if num == 0:
                            if flag is False:  # 中弧线
                                p[num].append([float(pair.split(',')[0]), float(pair.split(',')[1])])
                            else:  # 其他几何参数
                                if len(pair.split(',')) == 2:
                                    ret.append([float(pair.split(',')[0]), float(pair.split(',')[1])])
                                else:
                                    ret.append(float(pair))
                        else:
                            p[num].append(float(pair))
                    pair = f.readline()

                retzr[len(retzr) - 1].append(ret)
                retppzr[len(retppzr) - 1].append(p[1])
                retpszr[len(retpszr) - 1].append(p[2])
                # 接下来输入动叶
            retz.append(retzr)
            retppz.append(retppzr)
            retpsz.append(retpszr)
        return retz, retppz, retpsz, [z, zr]


def txtoutput(file_name, camber, pp, ps, opt):  # camber控制点 pp、ps比距离 opt=False 单个叶片 opt=True 一组叶片
    f = open(file_name, mode='w')
    if opt is False:  # 还需要输出其他参数，例如尾缘半径
        print('[CAMBER]', file=f)
        for i in range(len(camber)):
            print(f'{camber[i, 0]},{camber[i, 1]}', file=f)
        print('', file=f)
        print('[PRESSURE SIDE]', file=f)
        for i in range(len(pp)):
            print(f'{pp[i]}', file=f)
        print('', file=f)
        print('[SUCTION SIDE]', file=f)
        for i in range(len(ps)):
            print(f'{ps[i]}', file=f)
    else:
        z = len(pp)
        zr = len(pp[0])
        print(f'总级数：{z}, 总计算站数：{zr}', file=f)
        print('', file=f)
        for j in range(z):
            for k in range(zr):
                print(f'级数：{j + 1}, 计算站数：{k + 1}, 静叶', file=f)
                print('[CAMBER]', file=f)
                for i in range(len(camber[j][k][0][0])):
                    print(f'{camber[j][k][0][0][i, 0]},{camber[j][k][0][0][i, 1]}', file=f)
                print('', file=f)
                for i in range(1, len(camber[j][k][0])):
                    if isinstance(camber[j][k][0][i], list):
                        print(f'{camber[j][k][0][i][0]},{camber[j][k][0][i][1]}', file=f)
                    else:
                        print(camber[j][k][0][i], file=f)
                print('', file=f)
                print('[PRESSURE SIDE]', file=f)
                for i in range(len(pp[j][k][0])):
                    print(f'{pp[j][k][0][i]}', file=f)
                print('', file=f)
                print('[SUCTION SIDE]', file=f)
                for i in range(len(ps[j][k][0])):
                    print(f'{ps[j][k][0][i]}', file=f)
                print('', file=f)

                print(f'级数：{j + 1}, 计算站数：{k + 1}, 动叶', file=f)
                print('[CAMBER]', file=f)
                for i in range(len(camber[j][k][1][0])):
                    print(f'{camber[j][k][1][0][i, 0]},{camber[j][k][1][0][i, 1]}', file=f)
                print('', file=f)
                for i in range(1, len(camber[j][k][1])):
                    if isinstance(camber[j][k][1][i], list):
                        print(f'{camber[j][k][1][i][0]},{camber[j][k][1][i][1]}', file=f)
                    else:
                        print(camber[j][k][1][i], file=f)
                print('', file=f)
                print('[PRESSURE SIDE]', file=f)
                for i in range(len(pp[j][k][1])):
                    print(f'{pp[j][k][1][i]}', file=f)
                print('', file=f)
                print('[SUCTION SIDE]', file=f)
                for i in range(len(ps[j][k][1])):
                    print(f'{ps[j][k][1][i]}', file=f)
                print('', file=f)
    f.close()


# 以下都是geomTurbo文件的结构输出
stack = []  # 输出处理栈
top = -1  # 一层3个空格
prefix_blank = ''
output_ready_flag = True  # 当这个flag等于True时才能输出


def geom_print(content, file):
    global output_ready_flag
    if output_ready_flag is True:
        print(f'{prefix_blank}{content}', file=file, end='', sep='')


def plane2cylinder(number, x_max, series, file, offset=0):
    geom_print(f'# section {number}\n', file)
    geom_print('XYZ\n', file)
    total = len(series)
    geom_print(f'+{total}\n', file)
    for point in series:
        z = point[0] + offset
        # 原来的纵轴变成了R*THETA，包裹圆柱
        theta = point[1] / x_max
        y = math.sin(theta) * x_max
        x = math.cos(theta) * x_max
        geom_print(f'{x}\t{y}\t{z}\t\n', file)


# 这个函数，包括下面的生成轮毂、机匣的代码都有问题：1.什么时候用科学计算表示？ 2.数据有效位数不对

def generate_NIROW_data(title, total, series, end_walls, file, offset=0):
    geom_print(f'{title}\n', file)
    geom_print('SECTIONAL\n', file)
    geom_print(f'{total}\n', file)
    for i in range(total):
        plane2cylinder(i + 1, end_walls[0] + (end_walls[1] - end_walls[0]) / (total - 1) * i,
                       series if np.ndim(series) == 2 else series[i], file, offset)


def push_stack(event_name, file):
    global stack
    global top
    global prefix_blank
    geom_print(f'NI_BEGIN\t{event_name}\n', file)  # 这里应该是制表符的，不知道用空格可不可以
    top = top + 1
    prefix_blank = prefix_blank + '   '
    stack.append(event_name)


def pop_stack(file):
    global stack
    global top
    global prefix_blank
    prefix_blank = prefix_blank[:-3]
    geom_print(f'NI_END\t{stack[top]}\n', file)
    stack.pop()
    top = top - 1


def generate_hub_shroud_curve(total, x, begin, end, file):
    geom_print(f'+{total}\n', file)
    interval = (end - begin) / total
    for i in range(total):
        p = interval * i + begin
        geom_print(f'{p}\t{x}\t\n', file)


def print_NIROW_info(number_of_blades, file):
    geom_print('NAME\t\trow 1\n', file)
    geom_print('TYPE\t\tnormal\n', file)
    geom_print('PERIODICITY\t90\n', file)
    push_stack('NIBLADE', file)
    geom_print('NAME\t\tMain Blade\n', file)
    push_stack('NIBLADEGEOMETRY', file)
    geom_print('TYPE\t\t\tGEOMTURBO\n', file)
    geom_print('GEOMETRY_MODIFIED\t0\n', file)
    geom_print('GEOMETRY TURBO VERSION\t5\n', file)  # 这个\t不知道是不是空格，看不出来
    geom_print('blade_expansion_factor_hub       0.1\n', file)  # 这里往下用的都是空格，很诡异
    geom_print('blade_expansion_factor_shroud    0.05\n', file)
    geom_print('intersection_npts                10\n', file)
    geom_print('intersection_control             0\n', file)
    geom_print('data_reduction                   0\n', file)
    geom_print('data_reduction_spacing_tolerance 1E-006\n', file)  # 这个真的是一个空格
    geom_print('data_reduction_angle_tolerance   90\n', file)
    geom_print('units                          1\n', file)
    geom_print(f'number_of_blades               {number_of_blades}\n', file)
    geom_print('blade_tangential_definition                        +0\n', file)


def geomturbo_output(re_p, re_s, end_walls, file_name, b=None, offset=0, expansion_angle=0, last_TE=None,
                     number_of_blades=90):
    global output_ready_flag
    if output_ready_flag is True:
        file = open(f'{file_name}', 'w')
    else:
        file = None
    head_info = 'GEOMETRY TURBO\nVERSION 5.5\nTOLERANCE                                          1E-006\n'
    geom_print(head_info, file)
    if last_TE is None:
        push_stack('CHANNEL', file)
        push_stack('basic_curve', file)
        geom_print('NAME\t\t\thub_crv_1\n', file)
        geom_print('DISCRETISATION\t\t10\n', file)
        geom_print('DATA_REDUCTION\t\t0\n', file)
        push_stack('zrcurve', file)
        geom_print('ZR\n', file)
        if np.ndim(re_p) == 2:
            generate_hub_shroud_curve(144, end_walls[0], -50, 240, file)  # 通流长度用10倍叶宽来算
        else:
            generate_hub_shroud_curve(144, end_walls[0], re_p[0][0, 0] - 10 * b, re_p[0][-1, 0] + 10 * b, file)
        pop_stack(file)
        pop_stack(file)

        push_stack('basic_curve', file)
        geom_print('NAME\t\t\tshroud_crv_1\n', file)
        geom_print('DISCRETISATION\t\t10\n', file)
        geom_print('DATA_REDUCTION\t\t0\n', file)
        push_stack('zrcurve', file)
        geom_print('ZR\n', file)
        if np.ndim(re_p) == 2:
            generate_hub_shroud_curve(144, end_walls[1], -50, 240, file)
        else:
            generate_hub_shroud_curve(144, end_walls[1], re_p[0][0, 0] - 10 * b, re_p[0][-1, 0] + 10 * b, file)
        pop_stack(file)
        pop_stack(file)

        push_stack('channel_curve hub', file)
        geom_print('NAME\t\thub\n', file)
        geom_print('VERTEX\tCURVE_P\thub_crv_1\t0\n', file)
        geom_print('VERTEX\tCURVE_P\thub_crv_1\t1\n', file)
        pop_stack(file)
        push_stack('channel_curve shroud', file)
        geom_print('NAME\t\tshroud\n', file)
        geom_print('VERTEX\tCURVE_P\tshroud_crv_1\t0\n', file)
        geom_print('VERTEX\tCURVE_P\tshroud_crv_1\t1\n', file)
        pop_stack(file)
        pop_stack(file)
    else:
        # 先算交点
        # 叶底
        point_LE = [[re_p[i][0, 0] + offset, end_walls[0] + i * (end_walls[1] - end_walls[0]) / (len(re_p) - 1)] for i
                    in range(len(re_p))]
        expansion_angle = expansion_angle / 180 * math.pi
        if data_list.blade_layout_method == 0:
            hub_x, hub_y = intersection([re_p[0][-1, 0] + offset, end_walls[0]], -math.tan(expansion_angle), point_LE)
        elif data_list.blade_layout_method == 1:
            # hub_x, hub_y = intersection([re_p[0][-1, 0] + offset, end_walls[0]], -math.tan(0), point_LE)
            hub_x = point_LE[0][0]
            hub_y = point_LE[0][1]
        shroud_x, shroud_y = intersection([re_p[-1][-1, 0] + offset, end_walls[1]], math.tan(expansion_angle), point_LE)

        tmp_hub = []
        tmp_shroud = []
        hub = []
        shroud = []
        # 第一段 连接上一段 或者 添加延伸段
        if last_TE == []:
            x_interval = (re_p[0][-1, 0] - re_p[0][0, 0]) / 20
            for i in range(20):
                tmp_hub.append([hub_x + (i - 20) * x_interval, hub_y])
                tmp_shroud.append([shroud_x + (i - 20) * x_interval, shroud_y])
            tmp_hub.append([hub_x, hub_y])
            tmp_shroud.append([shroud_x, shroud_y])
        else:
            hub_x_interval = (hub_x - last_TE[0][0]) / 20
            shroud_x_interval = (shroud_x - last_TE[1][0]) / 20
            for i in range(20):
                tmp_hub.append([last_TE[0][0] + i * hub_x_interval,
                                i * hub_x_interval / (hub_x - last_TE[0][0]) * (hub_y - last_TE[0][1]) + last_TE[0][1]])
                tmp_shroud.append([last_TE[1][0] + i * shroud_x_interval,
                                   i * shroud_x_interval / (shroud_x - last_TE[1][0]) * (
                                           shroud_y - last_TE[1][1]) + last_TE[1][1]])
            tmp_hub.append([hub_x, hub_y])
            tmp_shroud.append([shroud_x, shroud_y])
        hub.append(tmp_hub)
        shroud.append(tmp_shroud)
        tmp_hub = []
        tmp_shroud = []
        # 第二段 叶顶
        hub_x_interval = (re_p[0][-1, 0] + offset - hub_x) / 20
        shroud_x_interval = (re_p[-1][-1, 0] + offset - shroud_x) / 20
        for i in range(20):
            tmp_hub.append([hub_x + i * hub_x_interval,
                            i * hub_x_interval / (re_p[0][-1, 0] + offset - hub_x) * (end_walls[0] - hub_y) + hub_y])
            tmp_shroud.append([shroud_x + i * shroud_x_interval,
                               i * shroud_x_interval / (re_p[-1][-1, 0] + offset - shroud_x) * (
                                       end_walls[1] - shroud_y) + shroud_y])
        hub.append(tmp_hub)
        shroud.append(tmp_shroud)

    push_stack('NIROW', file)
    print_NIROW_info(number_of_blades, file)  # 这里面有两个push_stack()
    if np.ndim(re_p) == 2:
        generate_NIROW_data('suction', 2, re_p, end_walls, file)
        generate_NIROW_data('pressure', 2, re_s, end_walls, file)
    else:
        generate_NIROW_data('suction', len(re_p), re_p, end_walls, file, offset)
        generate_NIROW_data('pressure', len(re_s), re_s, end_walls, file, offset)
    pop_stack(file)
    pop_stack(file)
    pop_stack(file)
    if last_TE is None:
        geom_print('NI_END\tGEOMTURBO\n\n', file)  # 这东西不进栈
        push_stack('GEOMETRY', file)
        pop_stack(file)
    if output_ready_flag is True:
        file.close()
    if last_TE is not None:
        return hub, shroud


def print_all_meridional(hub, shroud, file_name):
    global output_ready_flag
    if output_ready_flag is True:
        file = open(f'{file_name}', 'a')
    else:
        file = None

    push_stack('CHANNEL', file)

    for i in range(len(hub)):
        push_stack('basic_curve', file)
        geom_print(f'NAME\t\t\thub_crv_{i + 1}\n', file)
        geom_print('DISCRETISATION\t\t10\n', file)
        geom_print('DATA_REDUCTION\t\t0\n', file)
        push_stack('zrcurve', file)
        geom_print('ZR\n', file)
        geom_print(f'+{len(hub[i])}\n', file)
        for j in range(len(hub[i])):
            geom_print(f'{hub[i][j][0]}\t{hub[i][j][1]}\t\n', file)
        pop_stack(file)
        pop_stack(file)

    for i in range(len(shroud)):
        push_stack('basic_curve', file)
        geom_print(f'NAME\t\t\tshroud_crv_{i + 1}\n', file)
        geom_print('DISCRETISATION\t\t10\n', file)
        geom_print('DATA_REDUCTION\t\t0\n', file)
        push_stack('zrcurve', file)
        geom_print('ZR\n', file)
        geom_print(f'+{len(shroud[i])}\n', file)
        for j in range(len(shroud[i])):
            geom_print(f'{shroud[i][j][0]}\t{shroud[i][j][1]}\t\n', file)
        pop_stack(file)
        pop_stack(file)

    push_stack('channel_curve hub', file)
    geom_print('NAME\t\thub\n', file)
    for i in range(len(hub)):
        geom_print(f'VERTEX\tCURVE_P\thub_crv_{i + 1}\t0\n', file)
        geom_print(f'VERTEX\tCURVE_P\thub_crv_{i + 1}\t1\n', file)
    pop_stack(file)
    push_stack('channel_curve shroud', file)
    geom_print('NAME\t\tshroud\n', file)
    for i in range(len(shroud)):
        geom_print(f'VERTEX\tCURVE_P\tshroud_crv_{i + 1}\t0\n', file)
        geom_print(f'VERTEX\tCURVE_P\tshroud_crv_{i + 1}\t1\n', file)
    pop_stack(file)
    pop_stack(file)

    geom_print('NI_END\tGEOMTURBO\n\n', file)
    push_stack('GEOMETRY', file)
    pop_stack(file)
    if output_ready_flag is True:
        file.close()


def intersection(line_point, line_slope, curve_points):
    line_b = line_point[1] - line_slope * line_point[0]
    for i in range(len(curve_points) - 1):
        x1 = curve_points[i][0]
        y1 = curve_points[i][1]
        x2 = curve_points[i + 1][0]
        y2 = curve_points[i + 1][1]
        if math.fabs(x2 - x1) < 1e-5:
            # segment_slope = float("inf")
            # segment_b = x1
            intersection_x = x1
        else:
            segment_slope = (y2 - y1) / (x2 - x1)
            segment_b = y1 - segment_slope * x1
            intersection_x = (segment_b - line_b) / (line_slope - segment_slope)
        # if segment_slope == line_slope:
        #     continue
        intersection_y = line_slope * intersection_x + line_b
        if (x1 <= intersection_x <= x2 or x2 <= intersection_x <= x1) and (
                y1 <= intersection_y <= y2 or y2 <= intersection_y <= y1):
            return intersection_x, intersection_y
    return None
