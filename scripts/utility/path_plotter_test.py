import unittest
from path_function import *
from path_plotter import PathPlotter


class PathPlotterTest(unittest.TestCase):

    def test_plotter(self):
        pass
    # TODO: Test No Input Failure

    def test_plot2D(self):
        file = read_path_file("../data/001_playerMovement.txt")
        plotter = PathPlotter()
        pass


if __name__ == '__main__':
    unittest.main()
