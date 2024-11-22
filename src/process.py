'''
Script that processes new csv files and applies offsets to the x, y, and z columns, then saves the new csv files.
Also randomizes and drops duplicates from the new csv files.
'''
# input the name of the csv file to process
box_name = "box1"
#

import pandas as pd
import os
import json

with open("settings.json", "r") as f:
    parameters = json.load(f)
    data_dir = parameters['data_dir']
    x_offset = parameters['x_offset']
    y_offset = parameters['y_offset']
    z_offset = parameters['z_offset']

try:
    box = pd.read_csv(os.path.join(data_dir, f"{box_name}_old.csv"), index_col=0)
except FileNotFoundError:
    raise FileNotFoundError(f"rename {box_name}.csv to {box_name}_old.csv")

# rename the header to "x", "y", "z"
box.columns = ["x", "y", "z"]
box.drop_duplicates(keep='first', inplace=True, ignore_index=True)
# add the offsets
box['x'] -= x_offset
box['y'] -= y_offset
box['z'] -= z_offset
print(box.head())
box.to_csv(os.path.join(data_dir, f"{box_name}.csv"), index=False)

box.sample(frac=1).reset_index(drop=True).to_csv(os.path.join(data_dir, f"{box_name}_random.csv"), index=False)