# This script is responsible for human path to drone path analysis
from utility.path_function import *


# TODO: path deviation
#       Input: player_path: list[Node], hostage_positions: list[Node]
#       Output: deviation_distance_list: list[float]
#       1. Determine the ideal path (straight line for now)
#       2. Determine the next hostage the player rescues
#       3. Find the point in a straight-line path to the hostage position closest to the player
#       4. Calculate the distance between the point and the player
#       5. Record the distance in a txt file

def path_deviation(hostage_positions: list[Node], player_path: list[Node]):
    # 1. Determine the ideal path
    ideal_path = {}

    # 2. Determine the next hostage the player rescues

    # 3. Find the closest point to the player in the ideal path to the next hostage

    # 4. Calculate the distance between the point and the player

    # 5. Record the distance in a txt file


def rescue_order(hostage_nodes: list[Node], player_path: list[Node], threshold: float = 1) -> list[Node]:
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
