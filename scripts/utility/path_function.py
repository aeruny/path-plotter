import math
import os
import random
import re


# Node Class
class Node:
    def __init__(self, coordinate: tuple = (0, 0, 0), time: float = 0.0, label: str = "",
                 unity_coordinate: bool = False):
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1] if not unity_coordinate else coordinate[2]
        self.z = coordinate[2] if not unity_coordinate else coordinate[1]
        self.label = label
        self.time = time
        self.neighbors = []

    def __str__(self) -> str:
        return self.label

    def add_neighbor(self, neighbor):
        if neighbor is self:
            raise Exception("You cannot connect a Node to itself")
        self.neighbors.append(neighbor)

    def add_neighbors(self, neighbors: list):
        for neighbor in neighbors:
            if neighbor is self:
                raise Exception("You cannot connect a Node to itself")
            else:
                self.neighbors.append(neighbor)


# Graph Class
class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.connections = {}

    # apply_complete_connection: connect all nodes with each other
    # public mutator method
    # params: None
    # return: None
    def apply_complete_connection(self):
        nodes = self.nodes.copy()
        for node in self.nodes:
            nodes.remove(node)
            node.add_neighbors(nodes)
            self.connections[node] = nodes
            nodes.append(node)

    # Clear all connections
    def clean_nodes(self):
        for node in self.nodes:
            node.neighbors = []

    def to_coordinates2D(self):
        x, y, labels = [], [], []
        for node in self.nodes:
            x.append(node.x)
            y.append(node.y)
            labels.append(node.label)
        return x, y, labels

    def to_coordinates3D(self):
        x, y, z, labels = [], [], [], []
        for node in self.nodes:
            x.append(node.x)
            y.append(node.y)
            z.append(node.z)
            labels.append(node.label)
        return x, y, z, labels


def read_path_file(file: str) -> Graph:
    # Open the data file
    if not os.path.exists(file):
        raise Exception("The file was not be found")
    with open(file, "r") as txt:
        # Split data
        data_str_list = [line.rstrip() for line in txt.readlines()]

        # Store the node and time lists
        coordinates, times = parse_data(data_str_list)
        labels = ["Time: " + str(time) for time in times]
        nodes = unity_coordinates_to_nodes(coordinates, times, labels)
        graph = Graph(nodes)
        return graph


def create_graph(file: str) -> Graph:
    # Open the data file
    if not os.path.exists(file):
        raise Exception("The file was not be found")
    with open(file, "r") as txt:
        # Split data
        data_str_list = [line.rstrip() for line in txt.readlines()]

        # Store the node and time lists
        coordinates, times = parse_data(data_str_list)
        labels = ["Node " + str(i) for i in range(len(coordinates))]
        nodes = unity_coordinates_to_nodes(coordinates, times, labels)
        graph = Graph(nodes)
        return graph


def parse_data(data_str_list: list[str]) -> (list[tuple[float]], list[str]):
    pattern = re.compile(
        r"\((?P<coord_x>.*),(?P<coord_y>.*),(?P<coord_z>.*)\),(?P<time>.*)")
    coordinates = []
    times = []
    for element in data_str_list:
        match = pattern.match(element)
        coordinates.append(
            (float(match.group("coord_x")), float(match.group("coord_y")), float(match.group("coord_z"))))
        times.append(match.group("time"))
    return coordinates, times


# distance: Euclidean Distance between two 2D nodes
# public function
# params: nodeA[Node], nodeB[Node]
def distance2D(nodeA: Node, nodeB: Node) -> float:
    return __distance2D(nodeA.coordinate, nodeB.coordinate)


# distance: Euclidean Distance between two 3D nodes
# public function
# params: nodeA[Node], nodeB[Node]
def distance3D(nodeA: Node, nodeB: Node) -> float:
    return __distance3D(nodeA.coordinate, nodeB.coordinate)


## Travelling Salesman Problem


# public function
# nearest_neighbor: Nearest Neighbor Algorithm
# params: nodes[list[Node]], start_node[Node]
# return: Dict[Node: Float], Dict[Node: Node]
def nearest_neighbor(graph: Graph, start_node: Node) -> list[Node]:
    nodes = graph.nodes
    path = [start_node]
    visited = []
    current_node = start_node
    min_dist = float(math.inf)
    min_node = None
    for _ in nodes[:-1]:
        visited.append(current_node)
        for temp_node in nodes:
            if temp_node not in visited and temp_node is not current_node:
                temp_dist = distance3D(current_node, temp_node)
                if temp_dist < min_dist:
                    min_dist = temp_dist
                    min_node = temp_node
        min_dist = float(math.inf)
        current_node = min_node
        path.append(current_node)
    return path


def greedy(nodes: list[Node], start_node: Node):
    connection = {}
    for node in nodes:
        connection[node] = []
    for _ in nodes:
        costs = {}
        for nodeA in nodes:
            for nodeB in nodes:
                if nodeA is not nodeB and len(connection[nodeA]) < 2 and len(connection[nodeB]) < 2:
                    if not is_cyclic(connection, nodeA, nodeB, len(nodes)):
                        costs[distance3D(nodeA, nodeB)] = (nodeA, nodeB)
        min_cost = float('inf')
        for cost in costs:
            if cost < min_cost:
                min_cost = cost
        a, b = costs[min_cost]
        connection[a].append(b)
        connection[b].append(a)
        print(f"{a.label} - {b.label}")

    # Convert to path
    current_node = start_node
    path = []
    for _ in nodes:
        # print(f"{current_node.label}: {[x.label for x in connection[current_node]]}")
        path.append(current_node)
        if connection[current_node][0] in path:
            if len(connection[current_node]) == 1:
                path.append(connection[current_node][1])
                break
            current_node = connection[current_node][1]
        else:
            current_node = connection[current_node][0]
    return path


# Random Path
def random_pathing(graph, start_node):
    path = [start_node]
    queue = []
    for node in graph.nodes:
        queue.append(node)
    queue.remove(start_node)

    while queue:
        path.append(queue.pop(random.randrange(0, len(queue))))
    return path


# public function
# dijkstra: Dijkstra's Algorithm
# params: nodes[list[Node]], start_node[Node]
# return: Dict[Node: Float], Dict[Node: Node]
def dijkstra(graph: Graph, start_node: Node, goal_node: Node):
    nodes = graph.nodes
    queue = []
    node_distance = {}
    node_previous = {}
    for node in nodes:
        node_distance[node] = float('inf')
        node_previous[node] = None
        queue.append(node)
    node_distance[start_node] = 0
    while not len(queue) == 0:
        current_node = queue.pop(queue.index(min(set(queue).intersection(node_distance), key=node_distance.get)))
        for neighbor_node in queue:
            new_distance = node_distance[current_node] + distance3D(current_node, neighbor_node)
            if new_distance < node_distance[neighbor_node]:
                node_distance[neighbor_node] = new_distance
                node_previous[neighbor_node] = current_node
    return __dijkstra_extract_path(node_previous, goal_node)


# Prim's Algorithm (Greedy)
# Finds the minimum spanning tree of a graph
def prim(graph, start_node):
    costs = {}
    queue = []
    costs[start_node] = [0, None]
    queue.append(start_node)
    while len(queue) > 0:
        current_node = min(queue, key=lambda x: costs[x])
        queue.remove(current_node)
        for neighbor_node in current_node.neighbors:
            if neighbor_node not in queue:
                queue.append(neighbor_node)
                costs[neighbor_node] = [current_node.neighbors[neighbor_node], current_node]
            elif current_node.neighbors[neighbor_node] < costs[neighbor_node][0]:
                costs[neighbor_node] = [current_node.neighbors[neighbor_node], current_node]
    tree = {}
    for node in costs:
        if costs[node][1] is None:
            continue
        if node not in tree:
            tree[node] = [costs[node][1]]
        else:
            tree[node].append(costs[node][1])
        if costs[node][1] not in tree:
            tree[costs[node][1]] = [node]
        else:
            tree[costs[node][1]].append(node)
    return tree


# unity_coordinates_to_nodes: 3D Vector to Node Converter
# param: coordinates, times, labels
# return: node_list
def unity_coordinates_to_nodes(coordinates: list[tuple[float]], times: list[float], labels: list[str]) -> list[Node]:
    return [Node(coordinate, time, label, unity_coordinate=True) for coordinate, time, label in zip(coordinates, times, labels)]


def nodes_to_coordinates(path: list[Node]):
    x, y, z = [], [], []
    for node in path:
        x.append(node.x)
        y.append(node.y)
        z.append(node.z)
    return x, y, z


def __dijkstra_extract_path(reverse_path: dict[Node], end_node: Node):
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = reverse_path[current_node]
    return path[::-1]


def is_cyclic(connection, node1: Node, node2: Node, nodes_len: int):
    check_node = node1
    visited = []
    index = 0
    while len(connection[check_node]) > 0:
        index += 1
        visited.append(check_node)
        if node2 in connection[check_node]:
            if index == nodes_len - 1:
                return False
            return True

        if connection[check_node][0] in visited:
            if len(connection[check_node]) == 1:
                return False
            check_node = connection[check_node][1]
        else:
            check_node = connection[check_node][0]

    return False


def print_path(path: list[Node]):
    print([node.label for node in path])


def print_path_coordinates(path: list[Node]):
    print([node.coordinate for node in path])


# distance3D: Euclidean Distance between two 3D coordinates
# private utility function
# params: coordA[3D vector], coordB[3D vector]
# return: float
def __distance3D(coordA: tuple[float], coordB: tuple[float]) -> float:
    return math.sqrt(sum([(a - b) * (a - b) for a, b in zip(coordA, coordB)]))


# distance2D: Euclidean Distance between two 2D coordinates
# private utility function
# params: coordA[3D vector], coordB[3D vector]
# return: float
def __distance2D(coordA: tuple[float], coordB: tuple[float]) -> float:
    return math.sqrt(pow(coordA[0] - coordB[0], 2) + pow(coordA[1] - coordB[1], 2))
