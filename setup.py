import os
import json
import laspy

p1 = os.path.join("src", "settings.json")

with open(p1, "r") as f:
    parameters = json.load(f)
    p_name = parameters['points_name']
    data_dir = parameters['data_dir']

try:
    os.mkdir(os.path.join("src", data_dir))
except FileExistsError:
    pass

try:
    os.mkdir(os.path.join("map_data", "boxes csv"))
except FileExistsError:
    pass

try:
    os.mkdir(os.path.join("map_data", "boxes random"))
except FileExistsError:
    pass

try:
    os.mkdir(os.path.join("map_data", "boxes raw"))
except FileExistsError:
    pass

print("Done!\n")
print("Directory setup complete. Make sure that boxes 1-12 (.laz) files are in directory \"boxes raw\" \n")