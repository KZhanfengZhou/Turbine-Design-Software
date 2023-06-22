import numpy as np
import shapely
from numpy.linalg import norm
from matplotlib import pyplot as plt
from shapely import LineString, intersection

# global plot to be used
fig, ax = plt.subplots()


# Transform data inside re_p.txt and re_s.txt into curve in numPy array
def txt2curve(file_name):
    curve = []
    with open(file_name) as data:
        while True:
            dataline = data.readline()
            if not dataline:
                break
            row = dataline.split(" ")
            point = []
            for string in row:
                point.append(float(string.split("\n")[0]))
            curve.append(point)
    return np.array(curve)


# Print the turbine curve of type NumPy array with two rows.
def print_curve():
    ax.plot(re_p[:, 0], re_p[:, 1])
    ax.plot(re_s[:, 0], re_s[:, 1])
    plt.show()
    return


# Normalize a vector.
def normalize(v):
    return v / norm(v)


# Get the normal vector of each point on the curve.
def get_normal(curve):
    normals = [np.array([0.0, 0.0])]
    n = len(curve)
    for i in range(1, n - 1):
        next = normalize(curve[i + 1] - curve[i])
        last = normalize(curve[i] - curve[i - 1])
        vec = normalize(next - last)
        normals.append(vec)
    normals[0] = normals[1]
    normals.append(normals[n - 2])
    return np.array(normals)


# Print one of the turbine curves and its steps of offset. For test only.
def print_step():
    ax.plot(re_p[:, 0], re_p[:, 1], 'b')
    ax.plot(re_s[:, 0], re_s[:, 1], 'r')
    one_step = re_p + get_dir_normal(re_p, re_s) * 3 * ref_scale(re_p)
    ax.plot(one_step[:, 0], one_step[:, 1], 'g')
    one_step = re_s + get_dir_normal(re_s, re_p) * 3 * ref_scale(re_s)
    ax.plot(one_step[:, 0], one_step[:, 1], 'y')
    plt.show()
    return


# Determine the "scale" of the curve; being referred by the offset step length, etc.
def ref_scale(curve):
    sum = 0
    for i in range(1, len(curve)):
        sum += norm(curve[i] - curve[i - 1])
    sum /= len(curve)
    return sum


# ref_p exists:
# Check if the vector is pointing "towards" the curve or "away from" the curve: v1 is the point and v2 is the normal
# towards: return 1
# away: return -1
#ref_p is None:
# Check if two vectors are pointing in the same direction. Same: return 1, different: return -1
def check_direction(v1, v2, ref_p=None):
    if ref_p is None:
        if v1.dot(v2) > 0:
            return 1
        else:
            return -1
    else:
        if np.dot(v2, ref_p - v1) > 0:
            return 1
        return -1


# Get normal vectors on a curve with direction always pointing towards the reference curve.
def get_dir_normal(vec, ref, first=False):
    normals = get_normal(vec)
    n = len(vec)
    for i in range(1, n - 1):
        if first:
            # This means that the normal needs to be checked wrt difference between current curve and reference curve
            normals[i] *= check_direction(vec[i], normals[i], ref[i])
        else:
            # This means that the normal needs to be checked wrt initial normal
            normals[i] *= check_direction(normals[i], ref[i])
    normals[0] = normals[1]
    normals[n - 1] = normals[n - 2]
    return normals


def dynamic_step(i, curve):
    return (1 - np.exp(-0.05 * i)) * 0.5 * ref_scale(curve)


# Calculate meanline between two curves.
def meanline_calc(init_c1, init_c2, steps=100):
    ax.plot(init_c1[:, 0], init_c1[:, 1], 'b')
    ax.plot(init_c2[:, 0], init_c2[:, 1], 'b')
    c1 = init_c1 # c1: current upper curve
    c2 = init_c2 # c2: current lower curve
    init_n1 = [] # normal of initial curve
    init_n2 = []
    for i in range(steps):
        # Check intersection first
        string1 = LineString(c1)
        string2 = LineString(c2)
        inter = intersection(string1, string2)
        # Plot intersection points
        if inter.geom_type == "Point":
            ax.plot(inter.x, inter.y, 'y.')
        elif inter.geom_type == "MultiPoint":
            xs = [point.x for point in inter.geoms]
            ys = [point.y for point in inter.geoms]
            ax.plot(xs, ys, 'g.')
        # Now, update the curves
        if i == 0:
            n1 = get_dir_normal(init_c1, init_c2, True)
            init_n1 = n1
            n2 = get_dir_normal(init_c2, init_c1, True)
            init_n2 = n2
        else:
            n1 = get_dir_normal(c1, init_n1)
            n2 = get_dir_normal(c2, init_n2)
        c1 = c1 + dynamic_step(i, init_c1) * n1
        c2 = c2 + dynamic_step(i, init_c1) * n2
        '''if i % 5 == 1:
            ax.plot(c1[:, 0], c1[:, 1], 'r')
            ax.plot(c2[:, 0], c2[:, 1], 'g')'''
    plt.show()
    return




re_p = txt2curve("../re_p.txt")
re_s = txt2curve("../re_s.txt")
meanline_calc(re_p, re_s)