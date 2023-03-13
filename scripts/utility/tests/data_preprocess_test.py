import os.path
import unittest
from utility.path_plotter import *
from utility.data_preprocess import *


class DataPreprocessTest(unittest.TestCase):
    def test_player_path(self):
        translation = (6.04, -20.47, -21.14)
        rotation = (0, 32.7, 0)

        hostage_graph = get_node_graph("../../data/hostageLocations.txt")

        plotter = PathPlotter()
        coordinates, times = convert_local_to_global_positions("../../data/player/001_playerMovements.txt", translation, rotation)
        nodes = unity_coords_to_nodes(coordinates)
        plotter.plot2D("Calibrated Path With Translation", nodes, hostage_graph)

        player_path = get_player_path("../../data/player/003_playerMovements.txt").nodes
        plotter.plot2D("Player 2D Path", player_path, hostage_graph)

    def test_drone_path(self):
        translation = (-9.15, -10.84, 8.32)
        rotation = (0, -174.52, 0)

        hostage_graph = get_node_graph("../../data/hostageLocations.txt")

        plotter = PathPlotter()
        coordinates, times = convert_local_to_global_positions("../../data/drone/001_droneMovements.txt", translation, rotation)
        nodes = unity_coords_to_nodes(coordinates)
        plotter.plot2D("Calibrated Drone Path", nodes, hostage_graph)

        player_path = get_player_path("../../data/drone/001_droneMovements.txt").nodes
        plotter.plot2D("Uncalibrated Drone Path", player_path, hostage_graph)



if __name__ == '__main__':
    unittest.main()
