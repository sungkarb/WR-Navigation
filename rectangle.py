'''
Combines boxes 5, 6, 8, 9, 11, and 12 into one csv file
'''

import os
import pandas as pd

print("Starting . . .")

boxes_csv_dir = os.path.join("map_data", "boxes csv")
dest = os.path.join("src", "data")

def get_name(x):
    return os.path.join(boxes_csv_dir, f"box{x}.csv")

indices = [5, 6, 8, 9, 11, 12]

print("Reading boxes")
boxes = []
for i, n in enumerate(indices):
    print(f"\tProcessing box {n}")
    boxes.append(pd.read_csv(get_name(n), dtype={'x': 'float64', 'y': 'float64', 'z': 'float64'}, engine='pyarrow'))

print("Joining boxes")
rectangle = pd.DataFrame()
rectangle = pd.concat(boxes, ignore_index=True)
rectangle.drop_duplicates(inplace=True)

print("Writing to csv (sorted ish)")
sorted_points = rectangle.sort_values(by=['x', 'y', 'z'])
sorted_points.reset_index(drop=True)
sorted_points.to_csv(os.path.join(dest, "rectangle.csv"), index=False)

print("Writing to csv (randomized)")
rectangle_random_path = os.path.join("src", "data", "rectangle_random.csv")
rectangle.sample(frac=1).reset_index(drop=True).to_csv(rectangle_random_path, index=False)

print("Done!\n")
