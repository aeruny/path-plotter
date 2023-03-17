import unittest

from utility.path_analysis import *
from utility.path_function import *


class PathAnalysisTest(unittest.TestCase):
    def setUp(self):
        self.result_file_path = "results"
        self.player_dir = "../../data/calibrated_player"
        self.drone_dir = "../../data/calibrated_drone"
        self.hostage_file_path = "../../data/hostageLocations.txt"

        # Extract the player path
        self.player_paths: list[list[Node]] = []
        for file in os.listdir(self.player_dir):
            file_path = os.path.join(self.player_dir, file)
            self.player_paths.append(get_player_path(file_path).nodes)

        # Extract the hostage graph
        self.hostage_graph: Graph = get_node_graph(self.hostage_file_path)

        # Obtain the Nearest Neighbor Path
        self.ideal_path_nn: list[Node] = nearest_neighbor(self.hostage_graph, Node((0, 0, 0)))

    def test_get_rescue_order(self):
        hostage_nodes = get_node_graph("../../data/hostageLocations.txt").nodes
        player_path = get_player_path("../../data/calibrated_player/001_playerMovements.txt").nodes
        test_value = get_rescue_order(player_path, hostage_nodes, threshold=5)
        print_path(test_value)
        print(test_value)

    def test_closest_point_distance(self):
        horizontal_line = Node((0, 0, 0)), Node((100, 0, 0))
        point = Node((50, 100, 0))
        test_value = closest_point_distance(horizontal_line, point)
        true_value = 100
        self.assertEqual(true_value, test_value)

        line = Node((0, 0, 0)), Node((100, 100, 0))
        point = Node((0, 100, 0))
        test_value = closest_point_distance(line, point)
        true_value = math.sqrt(100 * 100 + 100 * 100) / 2
        self.assertEqual(true_value, test_value)

    def test_get_standard_form(self):
        line = Node((0, 0, 0)), Node((2, 3, 0))
        true_value = (-3, 2, 0)
        test_value = get_standard_form(line)
        self.assertTupleEqual(true_value, test_value)

        line = Node((0, 1, 0)), Node((2, 4, 0))
        true_value = (-3, 2, -2)
        test_value = get_standard_form(line)
        self.assertTupleEqual(true_value, test_value)

    def test_closest_point_distance3D(self):
        horizontal_line = Node((0, 0, 0)), Node((100, 0, 0))
        point = Node((50, 100, 0))
        test_value = closest_point_distance(horizontal_line, point)
        true_value = 100
        self.assertEqual(true_value, test_value)

        line = Node((0, 0, 0)), Node((100, 100, 0))
        point = Node((0, 100, 0))
        test_value = closest_point_distance(line, point)
        true_value = math.sqrt(100 * 100 + 100 * 100) / 2
        self.assertEqual(true_value, test_value)

        line = Node((0, 0, 0)), Node((100, 100, 100))
        point = Node((0, 100, 0))
        test_value = closest_point_distance(line, point)
        true_value = math.sqrt(100 * 100 + 100 * 100) / 2
        #self.assertEqual(true_value, test_value)

        line = Node((0, 0, 0)), Node((100, 100, 100))
        point = Node((150, 150, 150))
        test_value = closest_point_distance(line, point)
        true_value = math.sqrt(200 * 200 + 200 * 200 + 200 * 200)
        self.assertEqual(true_value, test_value)

    def test_deviation_nearest_path_point(self):
        print(deviation_nearest_point_distance(self.player_paths[2], self.hostage_graph.nodes, 10))

    def test_generate_deviation_nearest_path_point(self):
        pass


if __name__ == '__main__':
    unittest.main()
