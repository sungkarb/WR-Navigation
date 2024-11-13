import random as random
import pandas as pd
import numpy as np
import math
import algorithms as algorithms
import time
import os

start_time = time.time()

random_points_path = os.path.join("data", "random_points.csv") 

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
    return start, end

points = pd.read_csv(random_points_path)
#point_a, point_b = generate_bounds(points)
AStar = algorithms.AStar(points.to_numpy())
point_a = np.array([1425.0600000005215, 435.96000000089407, 5.399999999999864])
point_b = np.array([218.19000000134113, 223.63000000081956, 34.24000000000001])
path = AStar.find_path(point_a, point_b)
print(path)

end_time = time.time()
print(f"Runtime: {end_time - start_time} seconds")
