'''
Creates all necessary files and directories for the project
'''

import os
import json
import pandas as pd
import laspy, lazrs
import numpy as np

print("\nTHIS WILL TAKE ABOUT 10-20 MINUTES TO RUN!!")
print("Setting up . . .")

p1 = os.path.join("src", "settings.json")

with open(p1, "r") as f:
    parameters = json.load(f)
    p_name = parameters['points_name']
    data_dir = parameters['data_dir']
    random_points_name = parameters['random_points_name']
    x_offset = parameters['x_offset']
    y_offset = parameters['y_offset']
    z_offset = parameters['z_offset']

p2 = os.path.join("src", data_dir)

try:
    print("Creating directory \"src/data/\". . .")
    os.mkdir(p2)
except FileExistsError:
    print("Directory already exists")

# generate points.csv
file_path = os.path.join("map_data", "point_cloud.laz")
las = laspy.read(file_path)
points = pd.DataFrame(np.vstack((las.x, las.y, las.z)).transpose())
points.columns = ["x", "y", "z"]

print("Processing points . . .")
points["x"] -= x_offset
points["y"] -= y_offset
points["z"] -= z_offset

p = os.path.join(p2, f"{p_name}.csv")

print("Sorting points . . .")  
sorted_points = points.sort_values(by=['x', 'y', 'z'])
sorted_points.reset_index(drop=True)

print("Writing points . . .")
sorted_points.to_csv(p, index=False)
sorted_points.sample(frac=1).to_csv(os.path.join("src", "data", f"{random_points_name}.csv"), index=False)

print("Done!\n")