import json
import math
import random
import time
import os
import numpy as np
import pandas as pd
import algorithms_og

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
    slope_factor = parameters['slope_factor']

    # file paths and names
    data_dir = parameters['data_dir']
    subsets_dir = parameters['subsets_dir']
    random_points_name = parameters['random_points_name']
    path_points_name = parameters['path_points_name']
    path_name = parameters['path_name']
    path_i_name = parameters['path_i_name']
    subset_name = parameters['subset_name']

res = subsets / resolution
print(f"\tEffective Resolution: \t{res} ({subsets} / {resolution})")
print(f"\tStart point: \t\t{start_point}")
print(f"\tEnd point: \t\t{end_point}\n")

random_points_path = os.path.join(data_dir, f"{random_points_name}.csv")

def generate_bounds(points) -> (np.ndarray, np.ndarray):
    # generate a random point from the "points" dataframe
    minDistance = 800
    start_index = random.randint(0, points.shape[0])
    end_index = random.randint(0, points.shape[0])
    start = points.loc[start_index]
    end = points.loc[end_index]

    # get the distance between two points
    def distance(p1, p2):
        return math.sqrt((p1["x"] - p2["x"])**2 + (p1["y"] - p2["y"])**2 + (p1["z"] - p2["z"])**2)

    while (distance(start, end) < minDistance):
        start_index = random.randint(0, points.shape[0])
        end_index = random.randint(0, points.shape[0])
        start = points.loc[start_index]
        end = points.loc[end_index]

    print("Start point: ", start["x"], start["y"], start["z"])
    print("End point: ", end["x"], end["y"], end["z"])
    print()
    return start, end

print("Initializing . . .")
init_start = time.time()
points = pd.read_csv(random_points_path)
AStar = algorithms_og.AStar()
init_end = time.time()
print(f"Initialization took {round(init_end - init_start, 5)} seconds\n")

print("Finding path . . .")
astar_start = time.time()
path = AStar.find_path(start_point, end_point)
astar_end = time.time()
print(f"Path finding took {round(astar_end - astar_start, 5)} seconds\n")

end_time = time.time()
print("Done!")
print(f"Total Runtime: {round(end_time - start_time, 5)} seconds\n")