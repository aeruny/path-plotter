import unittest
from path_finder import distance, distance3D

class TestDNN(unittest.TestCase):
    def setup_method(self, test_method):
        point1 = (145, 200, 65)
        point2 = 1
        point3 = 2

    def test_distance_2D(self):
        # 2 points in 2d space
        # True value
        true_value = 1
        # Function value
        func_value = 1
        self.assertEqual(true_value, func_value)

    def test_distance_3D(self):
        # 2 points in 3d space
        # True value
        true_value = 3
        # Function value
        func_value = 4
        self.assertEqual(true_value, func_value)


if __name__ == '__main__':
    TestDNN.main()
