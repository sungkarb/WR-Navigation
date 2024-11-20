import pandas as pd
import os

log_path = os.path.join("logs", "log_old.csv")
total_time = pd.read_csv(log_path)["total"]

# get the sum of the total_time column
total_time_sum = total_time.sum()
print(f"Total time: {total_time_sum/3600} hours")