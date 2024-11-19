import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import algorithms_ai as algorithms_ai

# read settings.json

with open("settings.json") as f:
    parameters = json.load(f)
    subsets = parameters['subsets']
    resolution = parameters['resolution']
    data_dir = parameters['data_dir']
    path_points_name = parameters['path_points_name']
    path_name = parameters['path_name']

res = subsets / resolution
# read files
path_points = pd.read_csv(os.path.join(data_dir, f"{path_points_name}.csv"))
path = pd.read_csv(os.path.join(data_dir, f"{path_name}.csv"))

# plot settings
boldness = 0.1

# plot the path
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(path_points["x"], path_points["y"], path_points["z"], c='r', s=boldness*res, marker='.')
ax.plot(path["x"], path["y"], path["z"], c='b', linewidth=1)
ax.set_xlabel('X axis (m)')
ax.set_ylabel('Y axis (m)')
ax.set_zlabel('Z axis (m)')
ax.view_init(elev=50, azim=50)
plt.show()