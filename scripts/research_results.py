import unittest
from os.path import join

from utility.path_analysis import *
from utility.path_plotter import *


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

    # This code plots and saves all player paths into the destination path
    def test_generate_all_path_plots_separate(self):
        destination_path = "results/path_plots"

        paths = generate_path_df(self.player_paths)
        for file_name, path in zip(os.listdir(self.player_dir), paths):
            title = f"Participant {file_name.split('_')[0]}'s Path"
            h_x, h_y, h_z = nodes_to_coordinates(self.hostage_graph.nodes)
            plt.plot(path['x'], path['y'])
            plt.scatter(h_x, h_y)
            plt.title(title)
            save_title = f"participant_{file_name.split('_')[0]}_path.png"
            plt.savefig(join(destination_path, save_title))
            plt.clf()

    # This code plots and saves all player paths as 3D plots into the destination path
    def test_generate_all_path_plots_3D(self):
        destination_path = "results/path_3d_plots"

        path_df_list = generate_path_df(self.player_paths)

        for file_name, path_df in zip(os.listdir(self.player_dir), path_df_list):
            title = f"Participant {file_name.split('_')[0]}'s Path"
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.set_title(title)

            h_x, h_y, h_z = nodes_to_coordinates(self.hostage_graph.nodes)
            ax.plot3D(path_df['x'], path_df['y'], path_df['z'])
            ax.scatter3D(h_x, h_y, h_z)

            save_title = f"participant_{file_name.split('_')[0]}_path.png"
            fig.savefig(join(destination_path, save_title))
            plt.close(fig)

    # Nearest Target Distance

    def test_deviation_nearest_target_df_list(self):
        destination_path = "results/nearest_target_distance"
        df_list = generate_nearest_target_distance_df_list(self.player_paths, self.hostage_graph.nodes)
        for i, table in enumerate(df_list):
            table.to_csv(join(destination_path, f"participant_{(i + 1):03}_nearest_target_distance.csv"), index=False)

    def test_plot_deviation_nearest_target_distance(self):
        destination_path = "results"
        df_table = generate_nearest_target_distance_df_list(self.player_paths, self.hostage_graph.nodes)
        for df_list in df_table:
            plt.plot(df_list['Timestep'], df_list['Distance'])

        plt.title("Nearest Target Distance")
        plt.xlabel("Timestep (s)")
        plt.ylabel("Distance (m)")

        plt.savefig(join(destination_path, "nearest_target_distance.png"))
        plt.show()

    # Nearest Path Point Distance

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
        destination_path = "results/nearest_path_distance"
        file_name_list = os.listdir(self.player_dir)
        df_list = generate_deviation_nearest_point_distance_df_list(self.player_paths, self.hostage_graph.nodes,
                                                                    threshold=5)
        for file_name, table in zip(file_name_list, df_list):
            table.to_csv(join(destination_path, f"participant_{file_name.split('_')[0]}_nearest_path_distance.csv"), index=False)

    def test_deviation_nearest_point_distance(self):
        distance_df_028 = generate_deviation_nearest_point_distance_df(self.player_paths[28],
                                                                       self.hostage_graph.nodes,
                                                                       threshold=5)
        # distance_df_031 = generate_deviation_nearest_point_distance_df(self.player_paths[30],
        #                                                                self.hostage_graph.nodes,
        #                                                                threshold=5)
        for time, dist in zip(distance_df_028['Timestep'], distance_df_028['Distance']):
            # if dist > 1000:
            print(f"{time}: {dist}")

    def test_plot_deviation_nearest_point_distance(self):
        destination_path = "results"
        df_table: list[pd.DataFrame] = generate_deviation_nearest_point_distance_df_list(self.player_paths,
                                                                                         self.hostage_graph.nodes,
                                                                                         threshold=5)
        fig, ax = plt.subplots()

        for df_list in df_table:
            ax.plot(df_list['Timestep'], df_list['Distance'])

        plt.title("Nearest Path Point Distance")
        plt.xlabel("Timestep (s)")
        plt.ylabel("Distance (m)")

        plt.savefig(join(destination_path, "nearest_path_point_distance.png"))
        plt.show()


if __name__ == '__main__':
    unittest.main()
