from utility.path_plotter import *

player_src_dir = "data/calibrated_player"
drone_src_dir = "data/calibrated_drone"
hostage_locations_file = "data/hostageLocations.txt"

hostage_locations = get_node_graph(hostage_locations_file)

player_paths = []
for file in os.listdir(player_src_dir):
    file_path = os.path.join(player_src_dir, file)
    player_paths.append(get_player_path(file_path).nodes)

shortest_path = nearest_neighbor(hostage_locations, hostage_locations.nodes[0])

plotter = PathPlotter()
plotter.plot_all_paths2D("Player Paths", player_paths, hostage_locations, shortest_path)


