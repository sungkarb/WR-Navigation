import json
import os
import random
import time
import numpy as np
import pandas as pd
import algorithms

def generate_bounds(points) -> (np.ndarray, np.ndarray):
    min_distance = 800
    num_points = points.shape[0]

    def distance(p1, p2):
        return np.linalg.norm(p1[['x', 'y', 'z']].values - p2[['x', 'y', 'z']].values)

    while True:
        start_index, end_index = random.sample(range(num_points), 2)
        start, end = points.loc[start_index], points.loc[end_index]
        if distance(start, end) >= min_distance:
            break

    return start, end

def main(subs, rsn):
    subsets = subs
    resolution = rsn
    with open("settings.json", "r") as f:
        parameters = json.load(f)
        parameters['subsets'] = subsets
        parameters['resolution'] = resolution
    with open("settings.json", "w") as f:
        json.dump(parameters, f)

    data = np.ndarray([], dtype=float)
    data = np.append(data, subsets)
    data = np.append(data, resolution)
    random_points_path = algorithms.random_points_path
    points = pd.read_csv(random_points_path)
    start_point, end_point = generate_bounds(points)
    start_time = time.time()
    AStar = algorithms.AStar()

    astar_start = time.time()
    path = AStar.find_path(start_point, end_point)
    astar_end = time.time()
    data = np.append(data, astar_end - astar_start)

    end_time = time.time()
    # remove the first element of data
    data = data[1:]
    data = np.append(data, end_time - start_time)
    with open(os.path.join("logs", "log.csv"), "a", newline='') as f:
        np.savetxt(f, [data], delimiter=",", fmt='%.6f')
    print(data)

for rsn in range(6_000, 4_500-1, -500):
    for sub in range(500, rsn+1, 250):
        main(sub, rsn)