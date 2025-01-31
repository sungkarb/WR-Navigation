'''
You only need to run this code if you are instructed to do so (by running main.py)
This program essentially resets "rectangle_random.csv"
It will take about 5 minutes to run idk
'''

import os
import pandas as pd

rectangle_path = os.path.join("data", "rectangle.csv")
rectangle_random_path = os.path.join("data", "rectangle_random.csv")

print("Reading rectangle.csv")
rectangle = pd.read_csv(rectangle_path, engine='pyarrow')

print("Writing rectangle_random.csv")
rectangle.sample(frac=1).to_csv(rectangle_random_path, index=False)

print("Done\n")


'''
    "start_point": [
        516839.34,
        4252795.26,
        1401.86
    ],
    "end_point": [
        521245.26,
        4250998.71,
        1340.74
    ],
    
'''