import json
import math
import random
import time
import os
import numpy as np
import pandas as pd
import algorithms
from typing import Tuple

def main():

    print("Starting . . .\n")
    start_time = time.time()
    print("Reading settings.json . . .")

    with open("settings.json", "r") as f:
        parameters = json.load(f)
        start_point = np.array(parameters['start_point'])
        end_point = np.array(parameters['end_point'])
        depth = parameters['depth']
        subsets = parameters['subsets']
        resolution = parameters['resolution']
        height_factor = parameters['height_factor']
        max_slope = parameters['max_slope']
        # slope_factor = parameters['slope_factor']

        # file paths and names
        data_dir = parameters['data_dir']
        subsets_dir = parameters['subsets_dir']
        random_points_name = parameters['random_points_name']
        path_points_name = parameters['path_points_name']
        path_name = parameters['path_name']
        path_i_name = parameters['path_i_name']
        subset_name = parameters['subset_name']
        path_path = os.path.join(data_dir, f"{path_name}.csv")
        path_i_path = os.path.join(data_dir, f"{path_i_name}.csv")

    res = subsets / resolution
    print(f"\tEffective Resolution: \t{res} ({subsets} / {resolution})")
    print(f"\tStart point: \t\t{start_point}")
    print(f"\tEnd point: \t\t{end_point}\n")

    random_points_path = os.path.join(data_dir, f"{random_points_name}.csv")

    def generate_bounds(points: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        # generate a random point from the "points" dataframe
        min_distance = 400
        start_index = random.randint(0, points.shape[0]-1)
        mid1_index = random.randint(0,points.shape[0]-1)
        mid2_index = random.randint(0,points.shape[0]-1)
        mid3_index = random.randint(0,points.shape[0]-1)
        mid4_index = random.randint(0,points.shape[0]-1)
        end_index = random.randint(0, points.shape[0]-1)
        start = points.loc[start_index]
        mid1 = points.loc[mid1_index]
        mid2 = points.loc[mid2_index]
        mid3 = points.loc[mid3_index]
        mid4 = points.loc[mid4_index]
        end = points.loc[end_index]

        # get the distance between two points
        def distance(p1, p2):
            return math.sqrt((p1["x"] - p2["x"])**2 + (p1["y"] - p2["y"])**2 + (p1["z"] - p2["z"])**2)

        while (distance(start, end) < min_distance):
            start_index = random.randint(0, points.shape[0]-1)
            mid1_index = random.randint(0,points.shape[0]-1)
            mid2_index = random.randint(0,points.shape[0]-1)
            mid3_index = random.randint(0,points.shape[0]-1)
            mid4_index = random.randint(0,points.shape[0]-1)
            end_index = random.randint(0, points.shape[0]-1)
            start = points.loc[start_index]
            mid1 = points.loc[mid1_index]
            mid2 = points.loc[mid2_index]
            mid3 = points.loc[mid3_index]
            mid4 = points.loc[mid4_index]
            end = points.loc[end_index]

        print("Start point: ", start["x"], start["y"], start["z"])
        print("Just visiting 1:", mid1["x"], mid1["y"], mid1["z"])
        print("Just visiting 2:", mid2["x"], mid2["y"], mid2["z"])
        print("Just visiting 3:", mid3["x"], mid3["y"], mid3["z"])
        print("Just visiting 4:", mid4["x"], mid4["y"], mid4["z"])
        print("End point: ", end["x"], end["y"], end["z"])
        print()
        return start, mid1, mid2, mid3, mid4, end

    print("Initializing . . .")
    init_start = time.time()
    points = pd.read_csv(random_points_path)
    print(f"Number of points: {points.shape[0]}")
    start_point, point1, point2, point3, point4, end_point = generate_bounds(points)
    AStar = algorithms.AStar()
    init_end = time.time()
    print(f"Initialization took {round(init_end - init_start, 5)} seconds\n")

    print("Finding path . . .")
    astar_start = time.time()
    order_of_traversal = AStar.find_closest_points(start_point, end_point,point1, point2, point3, point4)
    for i in range(len(order_of_traversal)):
        path = AStar.find_path(order_of_traversal[i], order_of_traversal[i+1], path_path + str(i), path_i_path + str(i))
    # path = AStar.find_path(start_point, end_point)
    astar_end = time.time()
    print(f"Path finding took {round(astar_end - astar_start, 5)} seconds\n")

    end_time = time.time()
    print("Done!")
    print(f"Total Runtime: {round(end_time - start_time, 5)} seconds\n")

if __name__ == '__main__':
    main()
