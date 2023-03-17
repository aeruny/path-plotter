import matplotlib.pyplot as plt
import numpy as np

from utility.path_analysis import *
from utility.path_function import *

if __name__ == "__main__":
    result_path = "results"
    player_dir = "data/calibrated_player"
    drone_dir = "data/calibrated_drone"
    hostage_path = "data/hostageLocations.txt"
    all_player_paths = get_all_player_path(player_dir)
    hostage_graph: Graph = get_node_graph(hostage_path)
    all_player_paths.pop(26)

    player_path_table: list[pd.DataFrame] = generate_nearest_neighbor_table(all_player_paths, hostage_graph.nodes)
    # player_path_table: list[pd.DataFrame] = generate_nearest_path_table(all_player_paths, hostage_graph.nodes)


    for i, path in enumerate(player_path_table):
        print(f"{i}: {path.shape}  {max(path['Timestep'])}")

    max_samples = max([float(max(path['Timestep'])) for path in player_path_table])
    n_steps = 10
    internal_x_ticks = np.arange(0, max_samples, max_samples // n_steps)
    print(internal_x_ticks)
    fig, ax = plt.subplots()
    ax.set_xticks(internal_x_ticks)
    ax.set_title("Closest Target Distance")
    ax.set_xlabel("Timestep (s)")
    ax.set_ylabel("Distance (m)")
    for i, path in enumerate(player_path_table):
        # print(f"{i+1}: {max(path['Distance'])},   {max(path['Timestep'])}")
        ax.plot(path['Timestep'], path['Distance'])
    plt.savefig("temp.png")

    plt.show()


