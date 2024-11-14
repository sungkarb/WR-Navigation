# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import algorithms as algorithms
import os

# file paths and names
random_points_path = algorithms.random_points_path
path_points_path = algorithms.path_points_path
path_path = algorithms.path_path

# read files
path_points = pd.read_csv(path_points_path)
path = pd.read_csv(path_path)

# plot settings
boldness = 60

# plot the path
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(path_points["x"], path_points["y"], path_points["z"], c='r', s=boldness/algorithms.subsets, marker='.')
ax.plot(path["x"], path["y"], path["z"], c='b')
ax.set_xlabel('X axis (m)')
ax.set_ylabel('Y axis (m)')
ax.set_zlabel('Z axis (m)')
ax.view_init(elev=50, azim=50)
plt.show()