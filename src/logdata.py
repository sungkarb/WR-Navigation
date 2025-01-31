import json
import os
import random
import time
import numpy as np
import pandas as pd
from typing import Tuple

import algorithms

'''
    higher subsets = takes longer to run
    lower resolution = takes longer to run
    s_rsn is the starting resolution
    e_rsn is the ending resolution
    rsn_step is the step size for the resolution (must be negative)
    sub_step is the step size for the number of subsets (must be positive)
    rsn_step and sub_step must be factors of the difference between s_rsn and e_rsn
'''

s_rsn = 6_000
e_rsn = 4_000
rsn_step = -400
sub_step = 100

iter = 0
for rsn in range(s_rsn, e_rsn-1, rsn_step):
    for sub in range(sub_step, rsn+1, sub_step):
        iter += 1

print(f"Total iterations: {iter}")

# Check if the parameters are valid
if (s_rsn < e_rsn):
    raise ValueError("s_rsn must be greater than e_rsn")
if (s_rsn - e_rsn) % rsn_step != 0:
    raise ValueError("rsn_step must be a factor of the difference between s_rsn and e_rsn")
if (e_rsn - s_rsn) % sub_step != 0:
    raise ValueError("sub_step must be a factor of the difference between s_rsn and e_rsn")
if (sub_step < 0) or (rsn_step > 0):
    raise ValueError("sub_step must be positive and rsn_step must be negative")

def generate_bounds(points) -> Tuple[np.ndarray, np.ndarray]:
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
        start_point = parameters['start_point']
        end_point = parameters['end_point']
        parameters['subsets'] = subsets
        parameters['resolution'] = resolution
    with open("settings.json", "w") as f:
        json.dump(parameters, f, indent=4)

    data = np.ndarray([], dtype=float)
    data = np.append(data, subsets)
    data = np.append(data, resolution)
    random_points_path = algorithms.random_points_path
    points = pd.read_csv(random_points_path)
    start_time = time.time()
    AStar = algorithms.AStar()

    astar_start = time.time()
    path = AStar.find_path(start_point, end_point)
    astar_end = time.time()
    data = np.append(data, astar_end - astar_start)

    end_time = time.time()
    # remove the first element of data, which is an empty value
    data = data[1:]
    data = np.append(data, end_time - start_time)
    data = np.append(data, points.shape[0])
    data = np.append(data, AStar.get_cost())
    data = np.append(data, AStar.get_path_length())

    with open(os.path.join("logs", "log.csv"), "a", newline='') as f:
        np.savetxt(f, [data], delimiter=",", fmt='%.6f')
    print(data)


# set the header of the csv file
with open(os.path.join("logs", "log.csv"), "w", newline='') as f:
    np.savetxt(f, ["subsets,resolution,astar,total,num_points,cost,path_length"], fmt='%s')

for rsn in range(s_rsn, e_rsn-1, rsn_step):
    for sub in range(sub_step, rsn+1, sub_step):
        main(sub, rsn)