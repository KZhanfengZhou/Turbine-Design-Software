import numpy as np
import math

from blade_geometry import Slope
from blade_geometry import calcu


def getFootPoint(point, line_p1, line_p2):
    """
    @point, line_p1, line_p2 : [x, y]
    """
    x0 = point[0]
    y0 = point[1]

    x1 = line_p1[0]
    y1 = line_p1[1]

    x2 = line_p2[0]
    y2 = line_p2[1]

    k = -((x1 - x0) * (x2 - x1) + (y1 - y0) * (y2 - y1) + 0 * 0) / \
        ((x2 - x1) ** 2 + (y2 - y1) ** 2 + 0 ** 2) * 1.0

    xn = k * (x2 - x1) + x1
    yn = k * (y2 - y1) + y1

    return (xn, yn)

def swap(cc, m):
    for i in range(0,int(m/2)):
        temp1 = cc[i, 0]
        temp2 = cc[i, 1]
        cc[i] = cc[m-i-1]
        cc[m-i-1, 0] = temp1
        cc[m-i-1, 1] = temp2
    return cc

def angle(center, point):
    if point[0] - center[0] >= 0:
        angle = np.arctan((point[1] - center[1]) / (point[0]-center[0]))
        if angle < 0:
            angle = angle + 2 * np.pi
    else:
        angle = np.arctan((point[1] - center[1]) / (point[0] - center[0])) + np.pi
    return angle


def circle(theta, point1, point2, m, point):        #theta为角度制
    theta = theta / 180 * np.pi
    cc1 = np.zeros((m, 2))
    cc2 = np.zeros((m, 2))
    cc1[m-1] = point1
    cc2[m-1] = point2
    array = np.zeros((2, 2))
    array[0] = point1
    array[1] = point2
    k1 = Slope.slope(array)
    k2 = point - point1
    costheta = (k1[0] * k2[0] + k1[1] * k2[1]) / np.sqrt(k1[0] * k1[0] + k1[1] * k1[1]) / np.sqrt(k2[0] * k2[0] + k2[1] * k2[1])
    if costheta <= 0:
        k1 = -k1
    d = np.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2)) / 2
    center = (point1 + point2) / 2 + k1 * d * np.tan(theta / 2)
    r = d / np.cos(theta / 2)
    theta1 = angle(center, point1)
    theta2 = angle(center, point2)
    theta0 = angle(center, point)
    if theta1 > theta2:
        temp = theta1
        theta1 = theta2
        theta2 = temp
    if theta0 > np.pi:
        if theta0 < theta2:
            flag = 0
        else:
            flag = 1
    else:
        if theta0 < theta1:
            flag = 1
        else:
            flag = 0
    ranget = (np.pi - theta) / 2
    if flag == 1:
        for i in range(m - 2, -1, -1):
            cc1[i][0] = r * np.cos(ranget / (m - 1) * (m - i - 1) + theta1) + center[0]
            cc1[i][1] = r * np.sin(ranget / (m - 1) * (m - i - 1) + theta1) + center[1]
            cc2[i][0] = r * np.cos(-ranget / (m - 1) * (m - i - 1) + theta2) + center[0]
            cc2[i][1] = r * np.sin(-ranget / (m - 1) * (m - i - 1) + theta2) + center[1]
    else:
        for i in range(m - 2, -1, -1):
            cc1[i][0] = r * np.cos(-ranget / (m - 1) * (m - i - 1) + theta1) + center[0]
            cc1[i][1] = r * np.sin(-ranget / (m - 1) * (m - i - 1) + theta1) + center[1]
            cc2[i][0] = r * np.cos(ranget / (m - 1) * (m - i - 1) + theta2) + center[0]
            cc2[i][1] = r * np.sin(ranget / (m - 1) * (m - i - 1) + theta2) + center[1]
    if calcu.distance(point2[0], point2[1], cc1[m - 2][0], cc1[m - 2][1]) < calcu.distance(point1[0], point1[1], cc1[m - 2][0], cc1[m - 2][1]):
        cc2[m - 1] = point1
        cc1[m - 1] = point2
        return cc2, cc1
    return cc1, cc2