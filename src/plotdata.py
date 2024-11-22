import pandas as pd
import matplotlib.pyplot as plt
import os

log_path = os.path.join("logs", "log.csv")

subsets = pd.read_csv(log_path)["subsets"]
resolution = pd.read_csv(log_path)["resolution"]
astar_time = pd.read_csv(log_path)["astar"]
total_time = pd.read_csv(log_path)["total"]
num_points = pd.read_csv(log_path)["num_points"]
cost = pd.read_csv(log_path)["cost"]
path_length = pd.read_csv(log_path)["path_length"]

# subsets / resolution
eff_rsn = subsets / resolution

eff_points = eff_rsn * num_points / 1_000_000

eff_cost = cost / path_length - 1

# plot eff_points, astar_time, and eff_cost on a 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# color the points based on resolution
ax.scatter(eff_rsn, astar_time, eff_cost, s=7, c=resolution, cmap='turbo')

# add color bar
cbar = plt.colorbar(ax.scatter(eff_rsn, astar_time, eff_cost, s=5, c=resolution, cmap='turbo'))

ax.set_xlabel('Effective Points (millions)')
ax.set_ylabel('A* Time (s)')
ax.set_zlabel('Cost')
plt.show()
