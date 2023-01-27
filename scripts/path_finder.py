import math
import random

import numpy as np

from data_plotter import DataPlotter, Node


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
def __distance2D(coordA, coordB, xz):
    if xz:
        return math.sqrt(pow(coordA[0] - coordB[0], 2) + pow(coordA[2] - coordB[2], 2))
    else:
        return math.sqrt(pow(coordA[0] - coordB[0], 2) + pow(coordA[1] - coordB[1], 2))


# distance: Euclidean Distance Calculator
# public function
# params: nodeA[Node], nodeB[Node], xz[boolean]
def distance(nodeA, nodeB, xz=True):
    return __distance2D(nodeA.coordinate, nodeB.coordinate, xz)

# distance: Euclidean Distance Calculator
# public function
# params: nodeA[Node], nodeB[Node], xz[boolean]
def distance3D(nodeA, nodeB):
    return __distance3D(nodeA.coordinate, nodeB.coordinate)


# public function
# dijkstra: Dijkstra's Algorithm
# params: nodes[list[Node]], start_node[Node]
# return: Dict[Node: Float], Dict[Node: Node]
def dijkstra(nodes, start_node):
    queue = []
    node_distance = {}
    previous_node = {}
    for node in nodes:
        node_distance[node] = float('inf')
        previous_node[node] = None
        queue.append(node)
    node_distance[start_node] = 0

    # print([node for node in node_distance.values()])

    while not len(queue) == 0:
        current_node = queue.pop(queue.index(min(set(queue).intersection(node_distance), key=node_distance.get)))
        # print(f"{current_node.label}:   {node_distance[current_node]}")
        for neighbor_node in queue:
            new_distance = node_distance[current_node] + distance(current_node, neighbor_node, xz=True)
            if new_distance < node_distance[neighbor_node]:
                node_distance[neighbor_node] = new_distance
                previous_node[neighbor_node] = current_node

    return node_distance, previous_node


def clean_nodes(nodes: list[Node]):
    for node in nodes:
        node.visited = False
        node.neighbors = []
        node.prev = None
        node.next = None


def nearest_neighbor(nodes: list[Node], start_node: Node) -> list[Node]:
    clean_nodes(nodes)
    path = [start_node]
    current_node = start_node
    min_dist = float(math.inf)
    min_node = None
    for _ in nodes[:-1]:
        current_node.visited = True
        for temp_node in nodes:
            if not temp_node.visited and temp_node is not current_node:
                temp_dist = distance(current_node, temp_node)
                if temp_dist < min_dist:
                    min_dist = temp_dist
                    min_node = temp_node
        min_dist = float(math.inf)
        current_node = min_node
        path.append(current_node)
    return path




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

def greedy(nodes: list[Node], start_node: Node):
    connection = {}
    for node in nodes:
        connection[node] = []
    for _ in nodes:
        costs = {}
        for a in nodes:
            for b in nodes:
                if a is not b and len(connection[a]) < 2 and len(connection[b]) < 2:
                    if not is_cyclic(connection, a, b, len(nodes)):
                        costs[distance(a, b)] = (a, b)
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
    for node in graph:
        queue.append(node)
    queue.remove(start_node)

    while queue:
        path.append(queue.pop(random.randrange(0, len(queue))))
    return path


# Prim's Algorithm (Greedy)
# Finds the minimum spanning tree of a graph
def prim(graph, start_node):
    costs = {}
    queue = []
    # costs[start_node] = 0
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
        if costs[node][1] == None:
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


# def travelling_salesman_problem(nodes, start_node):
#     return tsp_recursion(nodes, start_node)
#
#
# def tsp_recursion(nodes: list, current_node: Node) -> dict:
#     current_node.visited = True
#     cost = {}
#     if len(nodes) == 2:
#         c = nodes.pop()
#         if c is not current_node:
#             cost[c] = distance(c, current_node)
#             return cost
#     else:
#         for a in nodes:
#             for b in nodes:
#                 if not b.visited and a is not b and a is not current_node:
#                     nodes.remove(b)
#                     costs = [x for x in tsp_recursion(nodes, a).values()]
#                     costs.append(distance(a, b))
#                     cost[a] = min(costs)
#     return cost


# wrap_coordinates: 3D Vector to Node Converter
# param: coordinates[3D Vector]
# return: Node
def wrap_to_nodes(coordinates) -> list:
    nodes = []
    for coordinate, index in zip(coordinates, range(len(coordinates))):
        nodes.append(Node(coordinate, label=index))
    return nodes


def path_to_coordinates(path: list[Node], xz=True):
    x = []
    y = []
    for node in path:
        x.append(node.x)
        y.append(node.z if xz else node.y)
    return x, y


# Travelling Salesman Problem
# cost = travelling_salesman_problem(nodes, nodes[0])
# print([x for x in cost.keys()][0].label)


# def assign_neighbors(nodes):
#     for node in nodes:
#         for candidate in nodes:
#             if candidate is not node and distance(node, candidate) <= 100 and candidate not in node.neighbors:
#                 node.neighbors.append(candidate)


# assign_neighbors(nodes)

# dist, prev = dijkstra(nodes, nodes[0])
# print([d for d in dist.values()])
# print([p.label for p in prev.values() if p is not None])
