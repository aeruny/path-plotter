import math
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# Node Class
class Node:
    def __init__(self, coordinate: list, label: str):
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = coordinate[2]
        self.label = label
        self.visited = False
        self.neighbors = {}
        self.prev = None
        self.next = None

    def __str__(self):
        return self.label

    def distance(self, node):
        return math.sqrt(
            pow(self.coordinate[0] - node.coordinate[0], 2) + pow(self.coordinate[2] - node.coordinate[2], 2))

    def add_neighbors(self, neighbor_nodes):
        for neighbor in neighbor_nodes:
            if neighbor is not self:
                self.neighbors[neighbor] = self.distance(neighbor)


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
        self.__assign_neighbors()
        self.xz = False

    def read_file(self, file_path):
        data = self.__read_txt(file_path)
        self.nodes, self.time = self.__parse_data(data)

    # Return a tuple of a list of coordinate tuples and numerical time
    # Uses Python RegEx re module
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

    def __parse_data(self, data_str_list) -> (list[Node], list[float]):
        pattern = re.compile(
            r"\((?P<coord_x>-?\d+(\.\d+)?),(?P<coord_y>-?\d+(\.\d+)?),(?P<coord_z>-?\d+(\.\d+)?)\),(?P<time>\d+)")
        coordinates = []
        time = []
        for element in data_str_list:
            match = pattern.match(element)
            coordinates.append(
                (float(match.group("coord_x")), float(match.group("coord_y")), float(match.group("coord_z"))))
            time.append(match.group("time"))
        return self.__wrap_to_nodes(coordinates), time

    def __wrap_to_nodes(self, coordinates) -> list[Node]:
        nodes = []
        for coordinate, index in zip(coordinates, range(len(coordinates))):
            nodes.append(Node(coordinate=coordinate, label=index))
        return nodes

    def __assign_neighbors(self):
        for node in self.nodes:
            node.add_neighbors(self.nodes)

    def __plot_design_ax(self) -> plt.axes:
        ax = plt.axes
        size = self.plot_size
        ax.xlim(size[0], size[1])
        ax.ylim(size[0], size[1])
        ax.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
        ax.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
        ax.xlabel('x')
        if self.xz:
            ax.ylabel('z')
        else:
            ax.ylabel('y')

    def __positions_ax(self) -> plt.axes:
        ax = plt.axes

        xList = [node.coordinate[0] for node in self.nodes]
        yList = [node.coordinate[2] for node in self.nodes] if self.xz else [node.coordinate[1] for node in self.nodes]

        # Plot the points
        ax.plot(0, 0, color='blue', marker='.', markersize=10.0)  # Origin (Player)

        for index, node in enumerate(self.nodes):
            plt.annotate(node.label, (xList[index], yList[index]))
        ax.plot(xList, yList, linestyle='None', color='red', marker='.', markersize=10.0)

    def plot(self):
        self.__plot_design_ax()
        plt.title('Hostage Locations')
        plt.grid(True)
        plt.show()

    def plot_path(self, plot_name: str, x: list[float], y: list[float]):
        xList = [node.coordinate[0] for node in self.nodes]
        yList = [node.coordinate[2] for node in self.nodes] if self.xz else [node.coordinate[1] for node in self.nodes]
        size = self.plot_size

        # Plot Design
        plt.xlim(size[0], size[1])
        plt.ylim(size[0], size[1])
        plt.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
        plt.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(plot_name)

        # Plot the points

        plt.plot(xList, yList, linestyle='None', color='red', marker='.', markersize=10.0)
        plt.plot(0, 0, color='blue', marker='.', markersize=10.0)  # Origin (Player)
        plt.plot(x, y, color='red', marker='.', markersize=10.0)

        for index, node in enumerate(self.nodes):
            plt.annotate(node.label, (xList[index], yList[index]))

        plt.grid(True)
        plt.show()

    def plot2D(self):
        xList = [node.coordinate[0] for node in self.nodes]
        yList = [node.coordinate[1] for node in self.nodes]
        zList = [node.coordinate[2] for node in self.nodes]
        size = self.plot_size

        # Plot Design
        plt.xlim(size[0], size[1])
        plt.ylim(size[0], size[1])
        plt.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
        plt.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
        plt.xlabel('x')
        plt.ylabel('y')

        # Plot the points
        plt.plot(0, 0, color='blue', marker='.', markersize=10.0)  # Origin (Player)
        if self.connect_dots:
            plt.title('By the Recorded Order')
            plt.plot(xList, zList, color='red', marker='.', markersize=10.0)
        else:
            plt.title('Hostage Locations')
            plt.plot(xList, zList, linestyle='None', color='red', marker='.', markersize=10.0)

        for index, node in enumerate(self.nodes):
            plt.annotate(node.label, (xList[index], zList[index]))

        plt.grid(True)
        plt.show()

    # def plotPath(self, path_x, path_y):

    def plot3D(self):
        xList = [node.coordinate[0] for node in self.nodes]
        yList = [node.coordinate[1] for node in self.nodes]
        zList = [node.coordinate[2] for node in self.nodes]
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

    def plot_path_gif(self, plot_name: str, x: list[float], y: list[float], file_name: str):
        xList = [node.coordinate[0] for node in self.nodes]
        yList = [node.coordinate[2] for node in self.nodes] if self.xz else [node.coordinate[1] for node in self.nodes]

        print(f"x list: {xList}  {len(xList)}")
        print(f"y list: {yList}  {len(yList)}")
        size = self.plot_size

        fig, ax = plt.subplots()
        def animate(i):
            ax.clear()
            ax.set_xlim(size[0], size[1])
            ax.set_ylim(size[0], size[1])
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(plot_name)
            lineX, = ax.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
            lineY, = ax.plot([0, 0], size, linestyle='-', linewidth=1, color='black')
            line, = ax.plot(xList[:i+1], yList[:i+1], color='blue', marker='.', markersize=10.0)
            # for index, node in enumerate(self.nodes[:i+1]):
            #     ax.annotate(node.label, (xList[index], yList[index]))
            return line, lineX, lineY


        animation = FuncAnimation(fig, animate, interval=40, blit=True, repeat=True, frames=len(xList))
        animation.save(file_name, dpi=300, writer=PillowWriter(fps=3))
