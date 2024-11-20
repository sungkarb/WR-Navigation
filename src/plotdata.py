import pandas as pd
import matplotlib.pyplot as plt
import os

log_path = os.path.join("logs", "log.csv")

subsets = pd.read_csv(log_path)["subsets"]
resolution = pd.read_csv(log_path)["resolution"]
astar_time = pd.read_csv(log_path)["astar"]
total_time = pd.read_csv(log_path)["total"]

# plot subsets on the x-axis, resolution on the y-axis, and astar_time as the z-axis
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(subsets, resolution, astar_time, c='r', s=10, marker='.')
ax.set_xlabel('Subsets')
ax.set_ylabel('Resolution')
ax.set_zlabel('Time (s)')
plt.show()