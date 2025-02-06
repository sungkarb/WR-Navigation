import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
path = os.path.join("data", "rectangle_random.csv")

print("Reading the CSV file . . . \n")
rectangle = pd.read_csv(path, dtype=np.float64, skiprows=(lambda x: x % 10000 != 0))

# Plot the points
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(rectangle["x"], rectangle["y"], rectangle["z"], c='r', s=0.1, marker='.')
ax.set_xlabel('X axis (m)')
ax.set_ylabel('Y axis (m)')
ax.set_zlabel('Z axis (m)')
ax.view_init(elev=50, azim=50)
plt.show()
