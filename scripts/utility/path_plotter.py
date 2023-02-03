from path_function import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# DataPlotter Class
class PathPlotter:
    def __init__(self, graph: Graph = None, plot_size=None, label_on=False):
        self.graph = graph
        if plot_size is None:
            plot_size = [2000, 2000]
        self.plot_size = plot_size
        self.label_on = label_on

    def plot(self):
        self.__plot_design_ax()
        plt.title('Hostage Locations')
        plt.grid(True)
        plt.show()

    def plot2D(self, plot_name: str, path: list[Node]):
        # Plot Design
        # plt.xlim(-self.plot_size[0]//2, self.plot_size[0]//2)
        # plt.ylim(-self.plot_size[1]//2, self.plot_size[1]//2)
        x_lim, y_lim = self.__get_center_limits(path, offset=50)
        plt.xlim(x_lim[0], x_lim[1])
        plt.ylim(y_lim[0], y_lim[1])

        plt.axhline(y=0, color="black", linestyle="-")
        plt.axvline(x=0, color="black", linestyle="-")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(plot_name)

        # Plot Graph Nodes
        g_x, g_y, labels = self.graph.to_coordinates2D()
        plt.plot(g_x, g_y, linestyle='None', color='red', marker='.', markersize=10.0)
        labels = [i for i in range(len(labels))]
        if self.label_on:
            for x, y, label in zip(g_x, g_y, labels):
                plt.annotate(label, (x, y))

        # Plot Path
        p_x, p_y, p_z = nodes_to_coordinates(path)
        plt.plot(p_x, p_y, linestyle='-', color='blue', markersize=10.0)

        plt.grid(True)
        plt.show()

    def plot3D(self, plot_name: str, nodes: list[Node]):
        g_x, g_y, g_z, labels = self.graph.to_coordinates3D()
        n_x, n_y, n_z = nodes_to_coordinates(nodes)

        # syntax for 3-D projection
        ax = plt.axes(projection='3d')

        ax.set_title(plot_name)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # Plot Graph Nodes
        ax.scatter3D(g_x, g_y, g_z, color='blue')
        if self.label_on:
            for x, y, z, label in zip(g_x, g_y, g_z, labels):
                ax.text(x, y, z, label)

        # plotting
        ax.plot3D(n_x, n_y, n_z, color='red')
        ax.scatter3D(n_x, n_y, n_z, color='blue')

        plt.show()

    def plot_path_gif(self, plot_name: str, nodes: list[Node], output_file_name: str):
        n_x, n_y, n_z = nodes_to_coordinates(nodes)
        fig, ax = plt.subplots()

        def animate(i):
            ax.clear()
            ax.grid()
            xlim, ylim = self.__get_center_limits(nodes)
            ax.set_xlim(xlim[0], xlim[1])
            ax.set_ylim(ylim[0], ylim[1])
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(plot_name)
            hLine = ax.axhline(y=0, color='black', linestyle="-")
            vLine = ax.axvline(x=0, color='black', linestyle="-")

            line, = ax.plot(n_x[:i + 1], n_y[:i + 1], color='blue', marker='.', markersize=10.0)
            points = ax.scatter(n_x, n_y, color='red')
            # for index, node in enumerate(self.nodes[:i+1]):
            #     ax.annotate(node.label, (xList[index], yList[index]))
            return line, hLine, vLine, points

        animation = FuncAnimation(fig, animate, interval=40, blit=True, repeat=True, frames=len(n_x))
        animation.save(output_file_name, dpi=300, writer=PillowWriter(fps=2))
        plt.show()

    def __get_center_limits(self, nodes: list[Node], offset: float = 50):
        x, y, z = nodes_to_coordinates(nodes)
        x_max, x_min, y_max, y_min = max(x), min(x), max(y), min(y)
        # x_max = max(x_max, self.plot_size[0]//2)
        # x_min = min(x_max, -self.plot_size[0]//2)
        # y_max = max(y_max, self.plot_size[1]//2)
        # y_max = max(y_max, -self.plot_size[1]//2)
        return (x_min - offset, x_max + offset), (y_min - offset, y_max + offset)

    def __get_soft_center_limits(self, nodes: list[Node], offset: float = 50):
        (x_max, x_min), (y_max, y_min) = self.__get_center_limits(nodes, 0)
        x_max = max(x_max, self.plot_size[0] // 2)
        x_min = min(x_max, -self.plot_size[0] // 2)
        y_max = max(y_max, self.plot_size[1] // 2)
        y_max = max(y_max, -self.plot_size[1] // 2)

        return (x_min - offset, x_max + offset), (y_min - offset, y_max + offset)

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
