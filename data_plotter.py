import math
import os
import re
import matplotlib.pyplot as plt








# DataPlotter Class
class DataPlotter:
    def __init__(self, file_path, plot_size=None, connect_dots=False):
        if plot_size is None:
            plot_size = [1000, 1000]
        self.file_path = file_path
        self.plot_size = plot_size
        self.connect_dots = connect_dots
        if os.path.exists(file_path):
            self.read_file(self.file_path)

    def read_file(self, file_path):
        data = self.__read_txt(file_path)
        self.coordinates, self.time = self.__parse_data(data)

    # Return a tuple of a list of coordinate tuples and numerical time
    # Uses Python RegEx re module
    def __parse_data(self, data_str_list):
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

    def __read_txt(self, file):
        # Open the data file
        if not os.path.exists(file):
            raise Exception("The file could not be found")

        # Read and split data
        txt = open(file, "r")
        data_str_list = [line.rstrip() for line in txt.readlines()]
        data_str_list = data_str_list[1:]

        # Return a list of coordinate data
        return data_str_list

    def plot2D(self):
        xList = [coordinate[0] for coordinate in self.coordinates]
        yList = [coordinate[1] for coordinate in self.coordinates]
        zList = [coordinate[2] for coordinate in self.coordinates]
        size = self.plot_size

        # Plot Design
        plt.xlim(size[0], size[1])
        plt.ylim(size[0], size[1])
        plt.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
        plt.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Hostage Locations')

        # Plot the points
        plt.plot(0, 0, color='blue', marker='.', markersize=10.0)  # Origin (Player)
        if self.connect_dots:
            plt.plot(xList, yList, color='red', marker='.', markersize=10.0)
        else:
            plt.plot(xList, yList, linestyle='None', color='red', marker='.', markersize=10.0)
        for index in range(len(self.coordinates)):
            plt.annotate(index, (xList[index], yList[index]))

        plt.grid(True)
        plt.show()

    def plot3D(self):
        xList = [coordinate[0] for coordinate in self.coordinates]
        yList = [coordinate[1] for coordinate in self.coordinates]
        zList = [coordinate[2] for coordinate in self.coordinates]
        fig = plt.figure()

        # syntax for 3-D projection
        ax = plt.axes(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # plotting
        ax.plot3D(0, 0, 0, marker='.', markersize=10.0, color='blue')  # Origin (Player)
        if self.connect_dots:  # Hostages
            ax.plot3D(xList, yList, zList, marker='.', markersize=10.0, color='red')
        else:
            ax.plot3D(xList, yList, zList, linestyle='None', marker='.', markersize=10.0, color='red')
        ax.set_title('3D line plot geeks for geeks')
        plt.show()
