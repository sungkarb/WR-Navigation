'''
Combines boxes 5, 6, 8, 9, 11, and 12 into one csv file
'''

import os
import pandas as pd
import numpy as np

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
    boxes.append(pd.read_csv(get_name(n)))

print("Joining boxes")
rectangle = pd.DataFrame()
for box in boxes:
    rectangle = pd.concat([rectangle, box], ignore_index=True)

print("Writing to csv (sorted ish)")
rectangle.to_csv(os.path.join(dest, "rectangle.csv"))

print("Writing to csv (randomized)")
rectangle_random_path = os.path.join("src", "data", "rectangle_random.csv")
rectangle.sample(frac=1).reset_index(drop=True).to_csv(rectangle_random_path, index=False)

print("Done!")
