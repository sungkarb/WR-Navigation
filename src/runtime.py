'''
Class that uses log.csv to estimate the total run time of the algorithm given:
- the number of subsets
- the resolution
- number of points
'''

# TODO implement the estimate_time function

import pandas as pd
import numpy as np
import os
import json

# run a regression on the data

# function that takes in subsets, resolution, and number of points and outputs the time
def estimate_time(subsets, resolution, num_points):
    # read the log.csv file
    log_path = os.path.join("logs", "log.csv")
    log = pd.read_csv(log_path)
    
    # calculate the number of effective points

estimate_time(1000, 5000, 11161732)
