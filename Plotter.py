import math

from data_plotter import DataPlotter


# Node Class
class Node:
    def __init__(self, coordinate, label=""):
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = coordinate[2]
        self.label = label
        self.neighbors = []


# distance3D: Euclidean Distance Calculator
# private utility function
# params: coordA[3D vector], coordB[3D vector]
# return: Float
def __distance3D(coordA, coordB):
    return math.sqrt(sum([(a - b) * (a - b) for a, b in zip(coordA, coordB)]))


# distance2D: Euclidean Distance Calculator
# private utility function
# params: coordA[3D vector], coordB[3D vector], xz[boolean]
# return: Float
def __distance2D(coordA, coordB, xz=False):
    if xz:
        return math.sqrt(pow(coordA[0] - coordB[0], 2) + pow(coordA[2] - coordB[2], 2))
    else:
        return math.sqrt(pow(coordA[0] - coordB[0], 2) + pow(coordA[1] - coordB[1], 2))


# distance: Euclidean Distance Calculator
# public function
# params: nodeA[Node], nodeB[Node], xz[boolean]
def distance(nodeA, nodeB, xz=False):
    return __distance2D(nodeA.coordinate, nodeB.coordinate, xz)


# dijkstra: Dijkstra's Algorithm
# public function
# params: nodes[list[Node]], start_node[Node]
# return: Dict[Node: Float], Dict[Node: Node]
def dijkstra(nodes, start_node):
    queue = []
    node_distance = {}
    previous_node = {}
    for node in nodes:
        node_distance[node] = math.inf
        previous_node[node] = None
        queue.append(node)
    node_distance[start_node] = 0

    # print([node for node in node_distance.values()])

    while not len(queue) == 0:
        current_node = queue.pop(queue.index(min(set(queue).intersection(node_distance), key=node_distance.get)))
        # print(f"{current_node.label}:   {node_distance[current_node]}")
        for neighbor_node in current_node.neighbors:
            new_distance = node_distance[current_node] + distance(current_node, neighbor_node, xz=True)
            if new_distance < node_distance[neighbor_node]:
                node_distance[neighbor_node] = new_distance
                previous_node[neighbor_node] = current_node

    return node_distance, previous_node


# wrap_coordinates: 3D Vector to Node Converter
# param: coordinates[3D Vector]
# return: Node
def wrap_coordinates(coordinates):
    nodes = []
    for coordinate, index in zip(coordinates, range(len(coordinates))):
        nodes.append(Node(coordinate, label=index))
    return nodes


file = "data/hostageLocations.txt"
size = [-1000, 1000]
connect_dots = True

# Instantiate the plotter
plotter = DataPlotter(file, size, connect_dots)

nodes = wrap_coordinates(plotter.coordinates)


def assign_neighbors(nodes):
    for node in nodes:
        for candidate in nodes:
            if candidate is not node and distance(node, candidate) <= 100 and candidate not in node.neighbors:
                node.neighbors.append(candidate)


assign_neighbors(nodes)

dist, prev = dijkstra(nodes, nodes[1])
print([d for d in dist.values()])
print([p.label for p in prev.values() if p is not None])
