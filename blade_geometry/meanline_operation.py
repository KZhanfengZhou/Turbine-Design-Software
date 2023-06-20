import numpy as np
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
def get_normal(curve, ref_curve):
    normals = [np.array([0.0, 0.0])]
    n = len(curve)
    for i in range(1, n - 1):
        next = normalize(curve[i + 1] - curve[i])
        last = normalize(curve[i] - curve[i - 1])
        vec = normalize(next - last)
        vec *= check_direction(curve[i], vec, ref_curve[i])
        normals.append(vec)
    normals[0] = normals[1]
    normals.append(normals[n - 2])
    return np.array(normals)


# Print one of the turbine curves and its steps of offset. For test only.
def print_step():
    ax.plot(re_p[:, 0], re_p[:, 1])
    one_step = re_p + get_normal(re_p, re_s) * 3 * ref_scale(re_p)
    ax.plot(one_step[:, 0], one_step[:, 1])
    plt.show()
    return


# Determine the "scale" of the curve; being referred by the offset step length, etc.
def ref_scale(curve):
    sum = 0
    for i in range(1, len(curve)):
        sum += norm(curve[i] - curve[i - 1])
    sum /= len(curve)
    return sum


# Check if the vector is pointing "towards" the curve or "away from" the curve:
# towards: return 1
# away: return -1
def check_direction(p, v, ref_p):
    if np.dot(v, ref_p - p) > 0:
        return 1
    return -1


re_p = txt2curve("../re_p.txt")
re_s = txt2curve("../re_s.txt")
n_p = get_normal(re_p, re_s)
print_step()