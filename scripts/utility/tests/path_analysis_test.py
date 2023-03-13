import unittest

from utility.path_analysis import *
from utility.path_function import *


class PathAnalysisTest(unittest.TestCase):
    def test_extract_rescue_order(self):
        hostage_nodes = get_node_graph("../../data/hostageLocations.txt").nodes
        player_path = get_player_path("../../data/player/001_playerMovements.txt").nodes
        test_value = extract_rescue_order(hostage_nodes, player_path, threshold=5)
        print_path(test_value)

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

    def test_extract_rescue_order(self):
        pass


if __name__ == '__main__':
    unittest.main()
