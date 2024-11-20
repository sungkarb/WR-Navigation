import pandas as pd
import matplotlib.pyplot as plt
import os

log_path = os.path.join("logs", "log.csv")

subsets = pd.read_csv(log_path)["subsets"]
resolution = pd.read_csv(log_path)["resolution"]
astar_time = pd.read_csv(log_path)["astar"]
total_time = pd.read_csv(log_path)["total"]
num_points = pd.read_csv(log_path)["num_points"]

# subsets / resolution
eff_rsn = subsets / resolution

eff_points = eff_rsn * num_points

# plot eff_points against astar_time
fig, ax = plt.subplots()

# color the points based on resolution
sc = ax.scatter(eff_points, astar_time, c=resolution, cmap='viridis')
plt.colorbar(sc, label='Resolution')

ax.set_xlabel('Effective Points')
ax.set_ylabel('A* Time (s)')
ax.set_title('Effective Points vs. A* Time')
plt.show()