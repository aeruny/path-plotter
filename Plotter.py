import os
import matplotlib.pyplot as plt

# 2D Plotter for hostage location and shortest path

size = [-100, 100]


def readTxt():
    #       Open the data file
    #       Read and Parse data
    #       Return a list of coordinate data
    return 0


def plot(x, y):
    # Plot Design
    plt.xlim(size[0], size[1])
    plt.ylim(size[0], size[1])
    plt.plot(size, [0, 0], linestyle='-', linewidth=1, color='black')
    plt.plot([0, 0], size, linestyle='-', linewidth=1, color='black')

    # Plot the points
    plt.plot(x, y)
    plt.grid(True)
    plt.show()


plot(range(-5, 6), range(-5, 6))
