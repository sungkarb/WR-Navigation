'''
Processes all of the boxes so that everything else can run
'''

import os
import json
import pandas as pd
import laspy
import numpy as np

print("Create a directory named \"boxes raw\" inside of the \"map_data\" directory")
print("Then make sure inside \"boxes raw\", there is box1.laz, box2.laz ... box12.laz")

print("Starting . . .")
settings_path = os.path.join("src", "settings.json")

with open(settings_path, "r") as f:
    parameters = json.load(f)
    boxes_raw_dir = parameters["boxes_raw_dir"]
    boxes_csv_dir = parameters["boxes_csv_dir"]
    boxes_random_dir = parameters["boxes_random_dir"]

boxes_raw_dir = os.path.join("map_data", boxes_raw_dir)
boxes_csv_dir = os.path.join("map_data", boxes_csv_dir)
boxes_random_dir = os.path.join("map_data", boxes_random_dir)

print("Proessing 12 Boxes (this will take a long time). . .")
for i in range(1, 13):
    print(f"\tBox {i}")
    raw_box_name = f"box{i}.laz"
    box_name = f"box{i}.csv"
    raw_box_path = os.path.join(boxes_raw_dir, raw_box_name)
    las = laspy.read(raw_box_path)
    raw_box = pd.DataFrame(np.vstack((las.x, las.y, las.z)).transpose())
    raw_box.columns = ["x", "y", "z"]
    box = raw_box.sort_values(by=['x', 'y', 'z'])
    box.reset_index(drop=True)
    box_path = os.path.join(boxes_csv_dir, box_name)
    box.to_csv(os.path.join(boxes_csv_dir, box_name), index=False)
    box.sample(frac=1).reset_index(drop=True).to_csv(os.path.join(boxes_random_dir, box_name), index=False)

print("Done!\n")