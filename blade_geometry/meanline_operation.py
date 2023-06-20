import numpy as np
from matplotlib import pyplot as plt

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


re_p = txt2curve("../re_p.txt")
re_s = txt2curve("../re_s.txt")
print_curve()
