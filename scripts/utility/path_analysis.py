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
    rescue_order = get_rescue_order(hostage_positions, player_path, 10)

    # 3. Find the closest point to the player in the ideal path to the next hostage

    # 4. Calculate the distance between the point and the player

    # 5. Record the distance in a txt file


# Calculates the path deviation from the ideal path
def path_deviation_ideal(player_paths: list[list[Node]], ideal_path: list[Node]):
    pass  # return extract_rescue_order()


def get_rescue_order(player_path: list[Node], hostage_nodes: list[Node], threshold: float) -> (list[Node], list[float]):
    rescue_list = []
    time_list = []
    for player_node in player_path:
        threshold_list = []
        for hostage_node in hostage_nodes:
            if distance3D(player_node, hostage_node) <= threshold:
                threshold_list.append(hostage_node)
        if len(threshold_list) > 0:
            rescued_hostage = min(threshold_list, key=lambda h_candidate: distance3D(h_candidate, player_node))
            if rescued_hostage not in rescue_list:
                rescue_list.append(rescued_hostage)
                time_list.append(player_node.time)
    return rescue_list, time_list


def generate_rescue_order_tables(player_paths: list[list[Node]], hostage_nodes: list[Node], threshold: float):
    rescue_data_list = []
    rescue_data_list_t = []
    for i, path in enumerate(player_paths):
        rescue_order, time_list = get_rescue_order(path, hostage_nodes, threshold)
        rescue_data_row = [i + 1]
        rescue_data_row_t = [i + 1]
        for rescued_hostage, time in zip(rescue_order, time_list):
            rescue_data_row.append(int(rescued_hostage.label.split(' ')[-1]))
            rescue_data_row_t.append(int(rescued_hostage.label.split(' ')[-1]))
            rescue_data_row_t.append(time)
        rescue_data_list.append(rescue_data_row)
        rescue_data_list_t.append(rescue_data_row_t)
    table = pd.DataFrame(rescue_data_list, columns=["Participant"] + [f"Rescue {i + 1}" for i in range(15)])
    table_with_time = pd.DataFrame(rescue_data_list_t,
                                   columns=["Participant"] + ["Hostage" if x % 2 == 0 else "Time" for x in range(30)])
    return table, table_with_time


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


def target_distances_df(path: list[Node], targets: list[Node]):
    data_list = []
    for node in path:
        row = [node.time]
        for target in targets:
            row.append(distance3D(node, target))
        data_list.append(row)

    return pd.DataFrame(data_list, columns=["Timestep"] +
                                           [f"Target {i + 1}" for i in range(len(targets))])


def deviation_nearest_target_distance(path: list[Node], targets: list[Node]) -> list[list[Union[float, Node]]]:
    data_list = []
    for node in path:
        distance_dict = {}
        for target in targets:
            distance_dict[target] = distance3D(node, target)
        target = min(distance_dict, key=distance_dict.get)
        data_list.append([node.time, target, distance_dict[target]])
    return data_list


def generate_nearest_target_distance_df(path: list[Node], targets: list[Node]) -> pd.DataFrame:
    data_list = deviation_nearest_target_distance(path, targets)
    return pd.DataFrame(data_list, columns=["Timestep", "Nearest Target", "Distance"])


def generate_nearest_target_distance_df_list(paths: list[list[Node]], targets: list[Node]) -> list[pd.DataFrame]:
    return [generate_nearest_target_distance_df(path, targets) for path in paths]


def deviation_nearest_point_distance(path: list[Node], targets: list[Node], threshold: float = 5):
    rescue_order, rescue_time = get_rescue_order(path, targets, threshold)

    # The first node is the start location of the player
    rescue_order.insert(0, path[0])
    #
    path_lines = [(rescue_order[i], rescue_order[i + 1]) for i in range(len(rescue_order) - 1)]
    p_index = 0
    path_distances = []
    path_targets = []
    for node in path:
        path_distances.append(closest_point_distance(path_lines[p_index], node))
        path_targets.append(int(str(rescue_order[p_index + 1]).split(" ")[-1]))
        if node.time == rescue_time[p_index]:
            p_index += 1
            if p_index >= len(rescue_time):
                break
    return path_distances, path_targets


def generate_deviation_nearest_point_distance_df(path: list[Node], targets: list[Node], threshold: float = 5):
    distance_list, target_list = deviation_nearest_point_distance(path, targets, threshold)
    df_data_list = [[node.time, target, distance] for node, target, distance in zip(path, target_list, distance_list)]
    return pd.DataFrame(df_data_list, columns=["Timestep", "Next Target", "Distance"])


def generate_deviation_nearest_point_distance_df_list(paths: list[list[Node]], targets: list[Node],
                                                      threshold: float = 5):
    return [generate_deviation_nearest_point_distance_df(path, targets, threshold) for path in paths]


def generate_path_df(paths: list[list[Node]]) -> list[pd.DataFrame]:
    path_df_list = []
    for path in paths:
        path_data = []
        for node in path:
            path_data.append([node.time, node.x, node.y, node.z])
        path_df_list.append(pd.DataFrame(path_data, columns=["Timestep", "x", "y", "z"]))
    return path_df_list
