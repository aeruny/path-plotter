import unittest

from path_analysis import *
from utility.path_function import *


class PathAnalysisTest(unittest.TestCase):
    def test_extract_rescue_order(self):
        hostage_nodes = create_graph("data/hostageLocations.txt").nodes
        player_path = read_path_file("data/001_playerMovements.txt").nodes
        test_value = extract_rescue_order(hostage_nodes, player_path, threshold=10)
        print_path(test_value)


if __name__ == '__main__':
    unittest.main()
