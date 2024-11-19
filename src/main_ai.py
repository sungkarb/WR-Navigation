# main.py
import json
import time
import os
import numpy as np
import pandas as pd
from algorithms_ai import AStar

def main():
    print("Starting . . .\n")
    start_time = time.time()
    
    print("Reading settings.json . . .")
    # Initialize AStar with settings
    astar = AStar()
    config = astar.config
    
    # Calculate and display effective resolution
    res = config.subsets / config.resolution
    print(f"\tEffective Resolution: \t{res} ({config.subsets} / {config.resolution})")
    print(f"\tStart point: \t\t{config.start_point}")
    print(f"\tEnd point: \t\t{config.end_point}\n")

    # Initialize pathfinding
    print("Initializing . . .")
    init_start = time.time()
    points = pd.read_csv(astar.random_points_path)
    init_end = time.time()
    print(f"Initialization took {round(init_end - init_start, 5)} seconds\n")

    # Find path
    print("Finding path . . .")
    astar_start = time.time()
    path = astar.find_path(np.array(config.start_point), np.array(config.end_point))
    astar_end = time.time()
    print(f"Path finding took {round(astar_end - astar_start, 5)} seconds\n")

    end_time = time.time()
    print("Done!")
    print(f"Total Runtime: {round(end_time - start_time, 5)} seconds\n")
    
    return path


if __name__ == "__main__":
    main()