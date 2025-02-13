import sys 
import laspy
import pandas as pd
import numpy as np
from utilities import to_gps
import os 


if len(sys.argv) == 2:
    n = 10000
elif len(sys.argv) == 3:
    n = int(sys.argv[2])
else:
    print("Usage: [laz file] [resolution]")

print(f"Opened a file {sys.argv[1]}")
with laspy.open(sys.argv[1]) as fh:
    las = fh.read()

points = np.vstack((las.x, las.y, las.z)).T
points = to_gps(points)
df = pd.DataFrame(points, columns=["Latitude", "Longtitude", "Altitude"])

df = df.loc[::n]
name = sys.argv[1].split("/")[-1].split(".")[0]
path = os.path.join("csv", f"{name}.csv")
df.to_csv(path, index=False)
print(f"Saved file to {path}")
