import unittest

from utility.path_plotter import *
from utility.path_analysis import *


def test_all_participant_path_plot():
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


class ResearchResults(unittest.TestCase):
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




    def test_path_to_target_table(self):
        table = target_distances_pandas(self.player_paths[0], self.hostage_graph.nodes)
        print(table)
        table.to_csv(os.path.join(self.result_file_path, "participant001_target_distance_table.csv"))

    def test_nearest_neighbor_table(self):
        table = nearest_neighbor_list(self.player_paths[0], self.hostage_graph.nodes)
        print(table)
        table.to_csv(os.path.join(self.result_file_path, "participant001_nearest_neighbor_table.csv"))

    def test_nearest_neighbor_graph(self):
        table = nearest_neighbor_list(self.player_paths[0], self.hostage_graph.nodes)
        table.plot.line(x='Timestep', y='Distance')
        plt.show()

    def test_path_list(self):
        list = path_list_pandas(self.player_paths)
        print(list)
        print(f"{list[0]}")

    def test_path_deviation_ideal(self):
        path_deviation_ideal(self.player_paths)





if __name__ == '__main__':
    unittest.main()
