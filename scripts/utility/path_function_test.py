import os.path
import unittest
from path_function import *


class PathFunctionTest(unittest.TestCase):

    def test_Node(self):
        # Test Coordinate Return
        true_value = (0, 0, 0)
        test_node = Node((0, 0, 0))
        test_value = test_node.coordinate
        self.assertEqual(true_value, test_value)

        # Test Label
        true_value = ""
        test_node = Node((0, 0, 0))
        test_value = test_node.label
        self.assertEqual(true_value, test_value)

        true_value = "test node"
        test_node = Node((0, 0, 0), "test node")
        test_value = test_node.label
        self.assertEqual(true_value, test_value)

        # Test Neighbors
        nodeA = Node((100, 100, 0))
        nodeB = Node((-100, -100, 0))
        nodeC = Node((1000, 2000, 0))
        true_value = [nodeA, nodeB, nodeC]
        test_node = Node((0, 0, 0), "test node")
        test_node.add_neighbors([nodeA, nodeB, nodeC])
        test_value = test_node.neighbors
        self.assertListEqual(true_value, test_value)

    def test_Graph(self):
        pass

    def test_create_graph(self):
        true_value = (0, 0, 0)
        data_file = "data\hostageLocations.txt"
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), data_file)
        graph = create_graph(path)
        test_value = graph.nodes[0].coordinate
        self.assertEqual(true_value, test_value)

        true_value = 17
        test_value = len(graph.nodes)
        self.assertEqual(true_value, test_value)

    def test_node(self):
        self.nodeA = Node((0, 0, 0))
        self.nodeB = Node((100, 100, 100))

    def test_distance2D(self):
        nodeO = Node((0, 0, 0))
        nodeA = Node((100, 100, 0))
        nodeB = Node((-100, -100, 0))
        nodeC = Node((1000, 2000, 0))

        # Check the 2D distance between nodeO and nodeA
        true_value = 141.42135623730950488016887242097
        test_value = distance2D(nodeO, nodeA)
        self.assertEqual(true_value, test_value)

        # Check the 2D distance between nodeO and nodeB
        true_value = 141.42135623730950488016887242097
        test_value = distance2D(nodeO, nodeB)
        self.assertEqual(true_value, test_value)

        # Check the 2D distance between nodeA and nodeB
        true_value = 2 * 141.42135623730950488016887242097
        test_value = distance2D(nodeA, nodeB)
        self.assertEqual(true_value, test_value)

        # Check the 2D distance between nodeA and nodeC
        true_value = 2102.3796041628638288419857057496
        test_value = distance2D(nodeA, nodeC)
        self.assertEqual(true_value, test_value)

    def test_distance3D(self):
        nodeO = Node((0, 0, 0))
        nodeA = Node((100, 100, 100))
        nodeB = Node((-100, -100, -100))
        nodeC = Node((1000, 2000, 3000))

        # Check the 3D distance between nodeO and nodeA
        true_value = 173.20508075688772935274463415059
        test_value = distance3D(nodeO, nodeA)
        self.assertEqual(true_value, test_value)

        # Check the 3D distance between nodeO and nodeB
        true_value = 173.20508075688772935274463415059
        test_value = distance3D(nodeO, nodeB)
        self.assertEqual(true_value, test_value)

        # Check the 3D distance between nodeA and nodeB
        true_value = 2 * 173.20508075688772935274463415059
        test_value = distance3D(nodeA, nodeB)
        self.assertEqual(true_value, test_value)

        # Check the 3D distance between nodeA and nodeC
        true_value = 3581.8989377144632107873375100241
        test_value = distance3D(nodeA, nodeC)
        self.assertEqual(true_value, test_value)

    def test_dijkstra(self):
        nodes = [Node((0, 0, 0), "nodeO"), Node((100, 100, 100), "nodeA"), Node((-100, -100, -100), "nodeB"),
                 Node((150, 300, 450), "nodeC"), Node((-200, -400, 500), "nodeD"), Node((450, -500, -400), "nodeE"),
                 Node((-250, 200, 300), "nodeF"), Node((-200, 250, 300), "nodeG")]
        graph = Graph(nodes)

        true_value = [nodes[0], nodes[-1]]
        test_value = dijkstra(graph, nodes[0], nodes[-1])
        print_path(test_value)
        self.assertListEqual(true_value, test_value)


if __name__ == '__main__':
    unittest.main()
