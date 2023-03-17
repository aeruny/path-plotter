import unittest

from utility.path_plotter import PathPlotter


def read_path_file(param):
    pass


class PathPlotterTest(unittest.TestCase):

    def test_plotter(self):
        pass
    # TODO: Test No Input Failure

    def test_plot2D(self):
        file = read_path_file("../data/calibrated_player/025_playerMovement.txt")
        plotter = PathPlotter()
        pass


if __name__ == '__main__':
    unittest.main()
