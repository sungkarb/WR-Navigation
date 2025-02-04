'''
Generates a random pair of start and end points
'''

import os
import json
import pandas as pd
import numpy as np
import random

print("Starting . . . \n")

p1 = os.path.join("settings.json")

with open(p1, "r") as f:
    parameters = json.load(f)
    random_points_name = parameters['random_points_name']

random_points_path = os.path.join("data", f"{random_points_name}.csv")

pool = 10000
seed = random.randint(0, pool-1)
min_distance = 2000

print("Reading points . . . \n")
points = pd.read_csv(random_points_path, skiprows=(lambda x: x % pool != seed), dtype=np.float64)

start_i = random.randint(0, points.shape[0])
end_i = random.randint(0, points.shape[0])

start_point = points.iloc[start_i]
end_point = points.iloc[end_i]

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

print(f"Finding points over {min_distance} units apart . . . \n")
while calculate_distance(start_point, end_point) < min_distance:
    start_i = random.randint(0, points.shape[0])
    end_i = random.randint(0, points.shape[0])
    start_point = points.iloc[start_i]
    end_point = points.iloc[end_i]

print(start_point + "\n")
print(end_point + "\n")

parameters['start_point'] = start_point.tolist()
parameters['end_point'] = end_point.tolist()

with open(p1, "w") as f:
    json.dump(parameters, f, indent=4)

print("Done!\n")