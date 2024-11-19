import pandas as pd
import json
try:
    box = pd.read_csv("data/box1_old.csv", index_col=0)
except FileNotFoundError:
    raise FileNotFoundError("rename box1.csv to box1_old.csv")

with open("settings.json", "r") as f:
    parameters = json.load(f)
    x_offset = parameters['x_offset']
    y_offset = parameters['y_offset']
    z_offset = parameters['z_offset']

# rename the header to "x", "y", "z"
box.columns = ["x", "y", "z"]
box.drop_duplicates(keep='first', inplace=True, ignore_index=True)
# add the offsets
box['x'] -= x_offset
box['y'] -= y_offset
box['z'] -= z_offset
print(box.head())
box.to_csv("data/box1.csv", index=False)

box.sample(frac=1).reset_index(drop=True).to_csv("data/box1_random.csv", index=False)