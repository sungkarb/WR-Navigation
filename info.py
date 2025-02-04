import os
import pandas as pd
import numpy as np

rectangle_name = "rectangle"
rectangle_path = os.path.join("src", "data", f"{rectangle_name}.csv")

print("Starting . . \n")
points = pd.read_csv(rectangle_path, dtype=np.float64, engine='pyarrow')

min_x_point = points.loc[points['x'].idxmin()]
min_y_point = points.loc[points['y'].idxmin()]
print(min_x_point)
print(min_y_point)

max_x_point = points.loc[points['x'].idxmax()]
max_y_point = points.loc[points['y'].idxmax()]
print(max_x_point)
print(max_y_point)
