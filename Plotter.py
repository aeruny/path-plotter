import os
import re
import matplotlib.pyplot as plt

# 2D Plotter for hostage location and shortest path

file_path = "data/hostageLocations.txt"
size = [-1000, 1000]
connect_dots = True


def read_txt(file):
    # Open the data file
    if not os.path.exists(file):
        raise Exception("The file could not be found")

    # Read and split data
    txt = open(file, "r")
    data_str_list = [line.rstrip() for line in txt.readlines()]
    data_str_list = data_str_list[1:]

    # Return a list of coordinate data
    return data_str_list


# Return a tuple of a list of coordinate tuples and numerical time
# Uses Python RegEx re module
def parse_data(data_str_list):
    pattern = re.compile(
        r"\((?P<coord_x>-?\d+(\.\d+)?),(?P<coord_y>-?\d+(\.\d+)?),(?P<coord_z>-?\d+(\.\d+)?)\),(?P<time>\d+)")
    coordinates = []
    time = []
    for element in data_str_list:
        match = pattern.match(element)
        coordinates.append(
            (float(match.group("coord_x")), float(match.group("coord_y")), float(match.group("coord_z"))))
        time.append(match.group("time"))
    return coordinates, time


def plot(x, y):
    # Plot Design
    plt.xlim(size[0], size[1])
    plt.ylim(size[0], size[1])
    plt.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
    plt.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
    plt.title('Hostage Locations')
    plt.xlabel('x')
    plt.ylabel('y')

    # Plot the points
    plt.plot(0, 0, color='blue', marker='.', markersize=10.0)  # Origin (Player)
    if connect_dots:
        plt.plot(x, y, color='red', marker='.', markersize=10.0)
    else:
        plt.plot(x, y, linestyle='None', color='red', marker='.', markersize=10.0)
    plt.grid(True)
    plt.show()


def plot_3d(x, y, z):
    fig = plt.figure()

    # syntax for 3-D projection
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    # plotting
    ax.plot3D(0, 0, 0, marker='.', markersize=10.0, color='blue')  # Origin (Player)
    if connect_dots:  # Hostages
        ax.plot3D(x, y, z, marker='.', markersize=10.0, color='red')
    else:
        ax.plot3D(x, y, z, linestyle='None', marker='.', markersize=10.0, color='red')
    ax.set_title('3D line plot geeks for geeks')
    plt.show()


# Read File
data_str = read_txt(file_path)

# Parse Data
coordinates, time = parse_data(data_str)
for coordinate in coordinates:
    print(coordinate)
x_list = [coordinate[0] for coordinate in coordinates]
y_list = [coordinate[1] for coordinate in coordinates]
z_list = [coordinate[2] for coordinate in coordinates]

# Plot Data
#  Note that Unity's default coordinate system is where:
#  x-axis represents the horizontal distance
#  y-axis represents the vertical distance (height)
#  z-axis represents the depth
#  so a top-down perspective is represented in an xz-plane
plot(x_list, z_list)
plot_3d(x_list, z_list, y_list)
