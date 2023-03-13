from utility.path_analysis import extract_rescue_order
from utility.path_function import *
from utility.path_plotter import PathPlotter

hostage_graph = get_node_graph("data/hostageLocations.txt")
player_path = get_player_path("data/player/003_playerMovements.txt").nodes
drone_path = get_drone_path("data/drone/001_droneMovements.txt").nodes
print(f"player nodes: {len(player_path)}")
print(f"drone nodes: {len(drone_path)}")
test_value = extract_rescue_order(hostage_graph.nodes, player_path, threshold=50)
print_path(test_value)

plotter = PathPlotter()
# plotter.plot2D("Hotage Locations", hostage_graph.nodes, hostage_graph)
# plotter.plot2D("Player 2D Path", player_path, hostage_graph)
# plotter.plot3D("Player 3D Path", player_path, hostage_graph)
# plotter.plot2D("Drone001 2D Path", drone_path, hostage_graph)
# plotter.plot3D("Drone001 3D Path", drone_path, hostage_graph)
