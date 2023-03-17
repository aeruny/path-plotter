from utility.path_function import *
from utility.path_plotter import PathPlotter

hostage_graph = get_node_graph("data/hostageLocations.txt")
player_path = get_player_path("data/calibrated_player/001_playerMovements.txt").nodes
drone_path = get_drone_path("data/calibrated_drone/001_droneMovements.txt").nodes
print(f"player nodes: {len(player_path)}")
print(f"drone nodes: {len(drone_path)}")

plotter = PathPlotter()
# plotter.plot2D("Hotage Locations", hostage_graph.nodes, hostage_graph)
plotter.plot2D("Player 001 Path", player_path, hostage_graph)
# plotter.plot2D("Player 027 xy Path", player_path, unity_coordinate=True)
# plotter.plot3D("Player 3D Path", player_path, hostage_graph)
# plotter.plot2D("Drone001 2D Path", drone_path, hostage_graph)
# plotter.plot3D("Drone001 3D Path", drone_path, hostage_graph)

# hostage_order_list, rescue_time_list = extract_rescue_order(hostage_graph.nodes, player_path, threshold=20)
# print(len(hostage_order_list))
# print_path(hostage_order_list)
# print(rescue_time_list)

