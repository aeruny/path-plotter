import matplotlib.pyplot as plt

from data_plotter import DataPlotter
from scripts.path_finder import nearest_neighbor, path_to_coordinates, greedy, random_pathing

file = "../data/hostageLocations.txt"

size = [-1000, 1000]
connect_dots = True

# Instantiate the plotter
# plotter = DataPlotter(file, size, connect_dots)

# plotter.plot()

# print(plotter.coordinates)


# Plot Data
#  Note that Unity's default coordinate system is where:
#  x-axis represents the horizontal distance
#  y-axis represents the vertical distance (height)
#  z-axis represents the depth
#  so a top-down perspective is represented in an xz-plane

# plotter.plot3D()


# Instantiate the plotter
plotter = DataPlotter(file, size, connect_dots=False)
plotter.xz = True

nodes = plotter.nodes
# Clean Scatter Plot
plotter.plot2D()


# Nearest Neighbor Heuristic
NNH_path = nearest_neighbor(nodes, nodes[0])
print([x.label for x in NNH_path])
x, y = path_to_coordinates(NNH_path)
plotter.plot_path("Nearest Neighbor Heuristic", x, y)

# Greedy Heuristic
GH_path = greedy(nodes, nodes[0])
print([x.label for x in GH_path])
x, y = path_to_coordinates(GH_path)
plotter.plot_path("Greedy Heuristic", x, y)

# Random
random_path = random_pathing(nodes, nodes[0])
print([x.label for x in random_path])
x, y = path_to_coordinates(random_path)
plotter.plot_path("Random Path", x, y)

# Order
plotter.connect_dots = True
plotter.plot2D()
