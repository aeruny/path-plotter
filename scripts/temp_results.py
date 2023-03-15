import matplotlib.pyplot as plt
import numpy as np

from utility.path_analysis import *
from utility.path_function import *

if __name__ == "__main__":
    result_path = "results"
    player_dir = "data/calibrated_player"
    drone_dir = "data/calibrated_drone"
    hostage_path = "data/hostageLocations.txt"
    all_player_paths: list[list[Node]] = []
    for file in os.listdir(player_dir):
        file_path = os.path.join(player_dir, file)
        all_player_paths.append(get_player_path(file_path).nodes)
    hostage_graph: Graph = get_node_graph(hostage_path)

    player_path_table: list[pd.DataFrame] = nearest_neighbor_table(all_player_paths, hostage_graph.nodes)

    max_samples = max([len(size) for size in player_path_table])
    n_steps = 100
    internal_x_ticks = np.arange(0, max_samples, max_samples // n_steps)
    fig, ax = plt.subplots()
    ax.set_xtick = internal_x_ticks

    for path in player_path_table:
        ax.plot(path['Timestep'], path['Distance'])
    ax.plot(player_path_table[0]['Timestep'], player_path_table[0]['Distance'])
    plt.show()
