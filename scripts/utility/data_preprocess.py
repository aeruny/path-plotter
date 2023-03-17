# This script is used for fixing issues with data files
from utility import vector
from utility.path_function import *
from utility.path_plotter import *
import numpy as np


def local_to_global_position(local_position: tuple, translation: tuple, rotation: tuple) -> tuple[float, float, float]:
    # Rotate the translated position
    roll, pitch, yaw = np.radians(rotation)

    # Define the rotation matrix using Euler angles
    R_roll = np.array([[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
    R_pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])
    R_yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    R = np.dot(R_yaw, np.dot(R_pitch, R_roll))

    # Define the translation matrix
    T = np.array([[1, 0, 0, translation[0]],
                  [0, 1, 0, translation[1]],
                  [0, 0, 1, translation[2]],
                  [0, 0, 0, 1]])

    # Define the transformation matrix
    M = np.dot(T, np.vstack((np.hstack((R, np.zeros((3, 1)))), np.array([0, 0, 0, 1]))))

    # Transform the local point to global coordinates
    local_point = np.hstack((local_position, 1))
    global_point = np.dot(M, local_point)[:3]

    return tuple(global_point)


def convert_local_to_global_positions(coordinates: list[tuple], translation: tuple, rotation: tuple):
    new_coordinates = [local_to_global_position(coordinate, translation, rotation) for coordinate in coordinates]
    return new_coordinates


def zero_start_time(time: list[float]) -> list[float]:
    start_time = time[0]
    new_time = [t - start_time for t in time]
    return new_time


def calibrate_data_file(source_file: str, dest_file: str, translation, rotation):
    coordinates, time = read_file(source_file)
    coordinates = convert_local_to_global_positions(coordinates, translation, rotation)
    time = zero_start_time(time)
    with open(dest_file, "w") as dest:
        for coordinate, time in zip(coordinates, time):
            dest.write(f"({coordinate[0]},{coordinate[1]},{coordinate[2]}),{time}\n")


if __name__ == "__main__":
    base_path = "../"

    # Player Path Calibration
    player_src_dir = os.path.join(base_path, "data/player")
    player_dest_dir = os.path.join(base_path, "data/calibrated_player")
    player_translation = (6.04 - 5.5, -20.47, -21.14 + 12)  # (6.04, -20.47, -21.14)
    player_rotation = (0, 32.7, 0)
    for file in os.listdir(player_src_dir):
        calibrate_data_file(os.path.join(player_src_dir, file), os.path.join(player_dest_dir, file), player_translation,
                            player_rotation)

    # Drone Calibration
    drone_src_dir = os.path.join(base_path, "data/drone")
    drone_dest_dir = os.path.join(base_path, "data/calibrated_drone")
    drone_translation = (-9.15, -10.84, 8.32)
    drone_rotation = (0, -174.52, 0)
    for file in os.listdir(drone_src_dir):
        drone_translation = (-9.15, -10.84, 8.32)
        calibrate_data_file(os.path.join(drone_src_dir, file), os.path.join(drone_dest_dir, file), drone_translation,
                            drone_rotation)
