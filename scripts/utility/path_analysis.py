# This script is responsible for human path to drone path analysis
from typing import Union

import pandas as pd

from utility import vector
from utility.path_function import *


# TODO: path deviation
#       Input: player_path: list[Node], hostage_positions: list[Node]
#       Output: deviation_distance_list: list[float]
#       1. Determine the ideal path (straight line for now)
#       2. Determine the next hostage the player rescued
#       3. Find the point in a straight-line path to the hostage position closest to the player
#       4. Calculate the distance between the point and the player
#       5. Record the distance in a txt file

def path_deviation(hostage_positions: list[Node], player_path: list[Node]):
    # 1. Determine the ideal path
    # ideal_path =

    # 2. Determine the player's order of hostage rescue
    rescue_order = extract_rescue_order(hostage_positions, player_path, 10)

    # 3. Find the closest point to the player in the ideal path to the next hostage

    # 4. Calculate the distance between the point and the player

    # 5. Record the distance in a txt file


def extract_rescue_order(hostage_nodes: list[Node], player_path: list[Node], threshold: float = 1) -> list[Node]:
    rescue_list = []
    for player_node in player_path:
        threshold_list = []
        for hostage_node in hostage_nodes:
            if distance3D(player_node, hostage_node) <= threshold:
                threshold_list.append(hostage_node)
        if len(threshold_list) > 0:
            rescued_hostage = min(threshold_list, key=lambda x: distance3D(x, player_node))
            if rescued_hostage not in rescue_list:
                rescue_list.append(rescued_hostage)
    return rescue_list


def closest_point_distance2D(line: tuple[Node, Node], target: Node) -> float:
    A, B, C = get_standard_form(line)
    return abs(A * target.x + B * target.y + C) / math.sqrt(A * A + B * B)


def get_standard_form(line: tuple[Node, Node]) -> (float, float, float):
    node0, node1 = line
    A = node0.y - node1.y
    B = node1.x - node0.x
    C = (node1.y - node0.y) * node0.x - (node1.x - node0.x) * node0.y
    return A, B, C


def get_closest_point(line: tuple[Node, Node], point: Node) -> Node:
    u = vector.subtract(line[1], line[0])  # Line vector: Q-P
    v = vector.subtract(point, line[0])  # Point to Line vector:X-P

    proj_param = vector.dot_product(u, v) / vector.dot_product(u, u)  # projection parameter: (Q-P)*(X-P) / (X-P)(X-P)
    print(f"Projection Parameter: {proj_param}")
    if proj_param < 0:
        return line[0]
    elif proj_param <= 1:
        return vector.add(line[0], vector.multiply(proj_param, u))  # projection vector: projv(u)
    else:
        return vector.subtract(line[1], point)


def closest_point_distance(line: tuple[Node, Node], point: Node) -> float:
    closest_point = get_closest_point(line, point)
    distance_vector = vector.subtract(point, closest_point)
    return vector.norm(distance_vector)


def target_distances_pandas(path: list[Node], targets: list[Node]):
    data_list = []
    for node in path:
        row = [node.time]
        for target in targets:
            row.append(distance3D(node, target))
        data_list.append(row)

    return pd.DataFrame(data_list, columns=["Timestep"] +
                                           [f"Target {i + 1}" for i in range(len(targets))])


def nearest_neighbor(path: list[Node], targets: list[Node]) -> list[list[Union[float, Node]]]:
    data_list = []
    for node in path:
        distance_dict = {}
        for i, target in enumerate(targets):
            distance_dict[target] = distance3D(node, target)
        target = min(distance_dict, key=distance_dict.get)
        data_list.append([node.time, target, distance_dict[target]])
    return data_list


def nearest_neighbor_pandas(path: list[Node], targets: list[Node]) -> pd.DataFrame:
    data_list = nearest_neighbor(path, targets)
    return pd.DataFrame(data_list, columns=["Timestep", "Nearest Target", "Distance"])
