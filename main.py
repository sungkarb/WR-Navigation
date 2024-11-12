import random as random
import pandas as pd
import numpy as np
import math
import algorithms
import time

def generate_bounds(points) -> (np.ndarray, np.ndarray):
    # generate a random point from the "points" dataframe
    minDistance = 800
    start_index = random.randint(0, points.shape[0])
    end_index = random.randint(0, points.shape[0])
    start = points.loc[start_index]
    end = points.loc[end_index]

    # get the distance between two points
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

    while (distance(start, end) < minDistance):
        start_index = random.randint(0, points.shape[0])
        end_index = random.randint(0, points.shape[0])
        start = points.loc[start_index]
        end = points.loc[end_index]

    print("Start point: ", start["x"], start["y"], start["z"])
    print("End point: ", end["x"], end["y"], end["z"])
    return start, end

start_time = time.time()

points = pd.read_csv("random_points.csv")
point_a, point_b = generate_bounds(points)
AStar = algorithms.AStar(points.to_numpy())
path = AStar.find_path(point_a.to_numpy(), point_b.to_numpy())
print(path)

end_time = time.time()
print(f"Runtime: {end_time - start_time} seconds")