'''
This script calculates the total time spent on a log file.
'''

import pandas as pd
import os

log_path = os.path.join("logs", "log.csv")
total_time = pd.read_csv(log_path)["total"]

# get the sum of the total_time column
total_time_sum = total_time.sum()

# format the time into hour:minute:second
hours = round(total_time_sum // 3600)
minutes = round((total_time_sum % 3600) // 60)
seconds = round(total_time_sum % 60)
if (str(hours).__len__() == 1):
    hours = "0" + str(hours)
if (str(minutes).__len__() == 1):
    minutes = "0" + str(minutes)
if (str(seconds).__len__() == 1):
    seconds = "0" + str(seconds)

print(f"Total time: {hours}:{minutes}:{seconds} (hh:mm:ss)")
print(f"Average time per iteration: {total_time.mean()} seconds")