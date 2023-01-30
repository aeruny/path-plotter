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

# Nea

# plotter.plot_path_gif("Test", graph.nodes, "test.gif")