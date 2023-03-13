import unittest

import pandas as pd
from utility.path_plotter import *

from utility.path_function import *


class ResearchResults(unittest.TestCase):
    def setUp(self):
        self.result_path = "results"
        self.player_dir = "data/calibrated_player"
        self.drone_dir = "data/calibrated_drone"
        self.hostage_path = "data/hostageLocations.txt"

        self.player_paths: list[list[Node]] = []
        for file in os.listdir(self.player_dir):
            file_path = os.path.join(self.player_dir, file)
            self.player_paths.append(get_player_path(file_path).nodes)

        self.hostage_graph: Graph = get_node_graph(self.hostage_path)

    def test_path_to_hostage_table(self):
        path = self.player_paths[0]
        data_list = []
        for node in path:
            row = [node.time]
            for hostage in self.hostage_graph.nodes:
                row.append(distance3D(node, hostage))
            data_list.append(row)

        table = pd.DataFrame(data_list, columns=["Timestep"] + [f"Hostage {i + 1}" for i in range(self.hostage_graph.size())])
        print(table)
        table.to_csv(os.path.join(self.result_path, "participant001_hostage_distance_table.csv"))

    def test_nearest_hostage_table(self):
        path = self.player_paths[0]
        data_list = []
        for node in path:
            distance_dict = {}
            for i, hostage in enumerate(self.hostage_graph.nodes):
                distance_dict[i + 1] = distance3D(node, hostage)
            target_num = min(distance_dict, key=distance_dict.get)
            data_list.append([node.time, target_num, distance_dict[target_num]])

        table = pd.DataFrame(data_list, columns=["Timestep", "Nearest Neighbor", "Distance"])
        print(table)
        table.to_csv(os.path.join(self.result_path, "participant001_nearest_neighbor_table.csv"))

    def test_all_participant_path_plot(self):
        player_src_dir = "data/calibrated_player"
        # drone_src_dir = "data/calibrated_drone"
        hostage_locations_file = "data/hostageLocations.txt"

        hostage_locations = get_node_graph(hostage_locations_file)

        player_paths = []
        for file in os.listdir(player_src_dir):
            file_path = os.path.join(player_src_dir, file)
            player_paths.append(get_player_path(file_path).nodes)

        shortest_path = nearest_neighbor(hostage_locations, hostage_locations.nodes[0])

        plotter = PathPlotter()
        plotter.plot_all_paths2D("Participant Paths", player_paths, hostage_locations, shortest_path)

        self.assertEqual(1, 2)


if __name__ == '__main__':
    unittest.main()
