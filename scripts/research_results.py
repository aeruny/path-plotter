import unittest

from os.path import join
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

    def test_path_to_target_df(self):
        table = target_distances_df(self.player_paths[0], self.hostage_graph.nodes)
        print(table)
        table.to_csv(os.path.join(self.result_file_path, "participant001_target_distance_table.csv"))

    def test_nearest_neighbor_table(self):
        table = generate_nearest_target_distance_df(self.player_paths[0], self.hostage_graph.nodes)
        print(table)
        table.to_csv(os.path.join(self.result_file_path, "participant001_nearest_neighbor_table.csv"))

    def test_deviation_nearest_target_table(self):
        destination_path = "results/nearest_target_distance"
        df_table = generate_nearest_neighbor_table(self.player_paths, self.hostage_graph.nodes)
        for i, table in enumerate(df_table):
            table.to_csv(join(destination_path, f"participant_{(i + 1):03}_nearest_target_distance.csv"), index=False)

    def test_nearest_neighbor_graph(self):
        table = generate_nearest_target_distance_df(self.player_paths[0], self.hostage_graph.nodes)
        table.plot.line(x='Timestep', y='Distance')
        plt.show()

    def test_path_df(self):
        path_list = path_df(self.player_paths)
        print(list)

    def test_rescue_order(self):
        rescue_order_list = []
        for path in self.player_paths:
            individual_list = get_rescue_order(path, self.hostage_graph.nodes, 10)
            rescue_order_list.append(individual_list)
            print_path(individual_list)
        print(len(rescue_order_list))

    def test_generate_rescue_order_table(self):
        table, table_with_time = generate_rescue_order_tables(self.player_paths, self.hostage_graph.nodes, 10)
        print(table.head())
        table.to_csv(join(self.result_file_path, "rescue_order_table.csv"), index=False)
        table_with_time.to_csv(join(self.result_file_path, "rescue_order_table_with_time.csv"), index=False)

    def test_generate_deviation_nearest_point_distance(self):
        destination_path = "results/nearest_point_distance"
        df_table = generate_deviation_nearest_point_distance_df_list(self.player_paths, self.hostage_graph.nodes,
                                                                     threshold=5)
        for i, table in enumerate(df_table):
            table.to_csv(join(destination_path, f"participant_{(i + 1):03}_nearest_point_distance.csv"), index=False)


if __name__ == '__main__':
    unittest.main()
