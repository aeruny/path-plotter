from path_function import *
from utility.data_plotter import DataPlotter

data_file = "data\hostageLocations.txt"
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), data_file)

graph = create_graph(path)
graph.apply_complete_connection()
# print_path(graph.nodes)


plotter = DataPlotter(graph)

# Nearest Neighbor Heuristic
NNH_path = nearest_neighbor(graph, graph.nodes[0])
print_path(NNH_path)
plotter.plot3D("Nearest Neighbor Heuristic", NNH_path)

# plotter.plot_path_gif("Test", graph.nodes, "test.gif")

# import matplotlib.pyplot as plt
#
# from data_plotter import DataPlotter
# #from scripts.path_finder import nearest_neighbor, path_to_coordinates, greedy, random_pathing
#
# file = "../data/hostageLocations.txt"
#
# size = [-1000, 1000]
# connect_dots = True
#
# # Plot Data
# #  Note that Unity's default coordinate system is where:
# #  x-axis represents the horizontal distance
# #  y-axis represents the vertical distance (height)
# #  z-axis represents the depth
# #  so a top-down perspective is represented in an xz-plane
#
# # plotter.plot3D()
#
# # Instantiate the plotter
# plotter = DataPlotter(file, size, connect_dots=False)
# plotter.xz = True
#
# nodes = plotter.nodes
# # Clean Scatter Plot
# # plotter.plot2D()
#
#
# # Nearest Neighbor Heuristic
# NNH_path = nearest_neighbor(nodes, nodes[0])
# print([x.label for x in NNH_path])
# x, y = path_to_coordinates(NNH_path)
# plotter.plot_path("Nearest Neighbor Heuristic", x, y)
# #plotter.plot_path_gif("Nearest Neighbor Heuristic Path", x, y, "NNH.gif")
#
# # Greedy Heuristic
# GH_path = greedy(nodes, nodes[0])
# print([x.label for x in GH_path])
# x, y = path_to_coordinates(GH_path)
# plotter.plot_path("Greedy Heuristic", x, y)
# #plotter.plot_path_gif("Greedy Heuristic Path", x, y, "Greedy.gif")
#
# # Random
# random_path = random_pathing(nodes, nodes[0])
# print([x.label for x in random_path])
# x, y = path_to_coordinates(random_path)
# # plotter.plot_path("Random Path", x, y)
#
# # Order
# plotter.connect_dots = True
# # plotter.plot2D()
