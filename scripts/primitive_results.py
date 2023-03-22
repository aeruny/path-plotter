import unittest

from os.path import join
from matplotlib import pyplot as plt
from utility.path_function import *


class PrimitiveResults(unittest.TestCase):
    def setUp(self):
        self.result_file_path = "results"
        self.player_dir = "data/calibrated_player"
        self.drone_dir = "data/calibrated_drone"
        self.hostage_file_path = "data/hostageLocations.txt"

        # Extract the player path
        self.player_paths: list[list[Node]] = []
        for file in os.listdir(self.player_dir):
            file_path = os.path.join(self.player_dir, file)
            self.player_paths.append(get_player_path(file_path).nodes)

        # Extract the hostage graph
        self.hostage_graph: Graph = get_node_graph(self.hostage_file_path)

        # Obtain the Nearest Neighbor Path
        self.ideal_path_nn: list[Node] = nearest_neighbor(self.hostage_graph, Node((0, 0, 0)))

    def test_plot_hostage_names(self):
        result_destination = "results"
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Hostage Names")

        # Plot Graph Nodes
        h_x, h_y, h_z, labels = self.hostage_graph.to_coordinates3D()
        plt.plot(h_x, h_y, linestyle='None', color='red', marker='.', markersize=10.0)
        labels = [i + 1 for i in range(len(labels))]
        for x, y, label in zip(h_x, h_y, labels):
            plt.annotate(label, (x, y))

        plt.savefig(join(result_destination, "hostage_label_plot.png"))
        plt.show()



if __name__ == '__main__':
    unittest.main()
