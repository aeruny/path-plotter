import unittest

from os.path import join
from matplotlib import pyplot as plt

from utility.path_analysis import *
from utility.path_function import *


class QuickTests(unittest.TestCase):
    def setUp(self):
        self.result_file_path = "results"
        self.player_dir = "data/calibrated_player"
        self.player_df_dir = "data/calibrated_player_df"
        self.drone_dir = "data/calibrated_drone"
        self.hostage_file_path = "data/hostageLocations.txt"

        self.player_path_df_list = generate_path_df()

        # Extract the player path
        # self.player_paths: list[list[Node]] = []
        # for file in os.listdir(self.player_dir):
        #     file_path = os.path.join(self.player_dir, file)
        #     self.player_paths.append(get_player_path(file_path).nodes)

        # Extract the hostage graph
        self.hostage_graph: Graph = get_node_graph(self.hostage_file_path)

        # Obtain the Nearest Neighbor Path
        self.ideal_path_nn: list[Node] = nearest_neighbor(self.hostage_graph, Node((0, 0, 0)))

    def test_generate_all_path_plots_separate(self):
        destination_path = "results/path_plots"
        df = read_df_dir(join(self.player_df_dir))
        paths = generate_path_df(self.player_paths)
        for file_name, path in zip(os.listdir(self.player_dir), paths):
            title = f"Participant {file_name.split('_')[0]}'s Path"
            h_x, h_y, h_z = nodes_to_coordinates(self.hostage_graph.nodes)
            plt.plot(path['x'], path['y'])
            plt.scatter(h_x, h_y)
            plt.scatter([-321.176809293348], [-761.8827116025751], marker='O')
            plt.title(title)
            save_title = f"participant_029_test_path.png"
            plt.savefig(join(destination_path, save_title))
            plt.clf()


if __name__ == '__main__':
    unittest.main()
