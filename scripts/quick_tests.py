import unittest

from os.path import join
from matplotlib import pyplot as plt
import pandas as pd

from utility.path_analysis import *
from utility.path_function import *


class QuickTests(unittest.TestCase):
    def setUp(self):
        self.result_file_path = "results"
        self.player_dir = "data/calibrated_player"
        self.player_df_dir = "data/calibrated_player_df"
        self.drone_dir = "data/calibrated_drone"
        self.hostage_file_path = "data/hostageLocations.txt"

        # self.player_path_df_list = generate_path_df()

        # Extract the player path
        # self.player_paths: list[list[Node]] = []
        # for file in os.listdir(self.player_dir):
        #     file_path = os.path.join(self.player_dir, file)
        #     self.player_paths.append(get_player_path(file_path).nodes)

        # Extract the hostage graph
        self.hostage_graph: Graph = get_node_graph(self.hostage_file_path)

        # Obtain the Nearest Neighbor Path
        self.ideal_path_nn: list[Node] = nearest_neighbor(self.hostage_graph, Node((0, 0, 0)))

    def test_generate_path_plot(self):
        destination_path = "results/path_plots"
        path_df = pd.read_csv(join(self.player_df_dir, "participant_029_path_data.csv"))
        title = f"Participant 029's Path"
        h_x, h_y, h_z = nodes_to_coordinates(self.hostage_graph.nodes)
        plt.plot(path_df['x'], path_df['y'])
        plt.scatter(h_x, h_y)
        plt.scatter([-321.176809293348], [-761.8827116025751], color='red')
        plt.title(title)
        save_title = f"participant_029_test_path.png"
        plt.show()

    def test_generate_3d_path_plot(self):
        destination_path = "results/path_plots"
        path_df = pd.read_csv(join(self.player_df_dir, "participant_029_path_data.csv"))
        title = f"Participant 029's Path"
        h_x, h_y, h_z = nodes_to_coordinates(self.hostage_graph.nodes)

        figure = plt.figure()
        ax = plt.axes(projection='3d')

        ax.plot3D(path_df['x'], path_df['y'], path_df['z'])
        ax.scatter3D(h_x, h_y, h_z)
        ax.scatter3D([-321.176809293348], [-761.8827116025751], [-23.82], color='red')
        ax.set_title(title)
        save_title = f"participant_029_test_path.png"
        plt.show()

if __name__ == '__main__':
    unittest.main()
