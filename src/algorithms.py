import json
import math
import os
import random as random
import time as time
import networkx as nx
import numpy as np
import pandas as pd
from scipy import spatial
from typing import Tuple
import multiprocessing as mp

with open("settings.json", "r") as f:
    parameters = json.load(f)
    depth = parameters['depth']
    subsets = parameters['subsets']
    resolution = parameters['resolution']
    height_factor = parameters['height_factor']
    max_slope = parameters['max_slope']
    slope_factor = parameters['slope_factor']


    # file paths and names
    data_dir = parameters['data_dir']
    subsets_dir = parameters['subsets_dir']
    random_points_name = parameters['random_points_name']
    path_points_name = parameters['path_points_name']
    path_name = parameters['path_name']
    path_i_name = parameters['path_i_name']
    subset_name = parameters['subset_name']

    # Processes for multiprocessing
    processes_param = parameters['processes_mult']

random_points_path = os.path.join(data_dir, f"{random_points_name}.csv")
path_points_path = os.path.join(data_dir, f"{path_points_name}.csv")
path_path = os.path.join(data_dir, f"{path_name}.csv")
path_i_path = os.path.join(data_dir, f"{path_i_name}.csv")
subsets_path = os.path.join(subsets_dir, f"{subset_name}")

# giant array
giant = []

# cost
cost = 0

# length of the path
path_length = 0

"""Class to find the most optimal path using A* algorithm for robotics. Target change in elevation
    and distance to target
"""
class AStar:
    """"Sets up the graph for the efficient path finding
    
    Args:
        data: numpy array with dimensions (n x 3)
    """
    def __init__(self) -> None:
        # process data. assumes that the given data is unique and randomized
        # points = pd.DataFrame(data, columns=['x', 'y', 'z'])
        # points.drop_duplicates(inplace=True)
        # points.sample(frac=1).reset_index(drop=True).to_csv(random_points_path, index=False)
        global cost; cost = 0
        global path_length; path_length = 0
        global subsets
        global resolution
        with open("settings.json", "r") as f:
            parameters = json.load(f)
            subsets = parameters['subsets']
            resolution = parameters['resolution']

    # helper methods
    def slope_angle(self, x1, y1, z1, x2, y2, z2) -> float:
        # v dot w = |v||w|cos(theta)
        # theta = arccos(v dot w / |v||w|)
        v = np.array([(x2 - x1), (y2 - y1), (z2 - z1)])
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            return 0
        return abs(math.degrees(math.acos(abs(z2 - z1) / v_norm)))
    
    def create_subsets(self, points: pd.DataFrame, start: pd.DataFrame, end: pd.DataFrame) -> None:
        start_time = time.time()
        time_array = np.array([])

        # Number of points per subset based on resolution
        points_per_subset = len(points) // resolution

        for i in range(subsets):
            s_t = time.time()
            # Select the subset of points with points_per_subset points
            sub = points[i * points_per_subset:(i + 1) * points_per_subset].copy()
            
            # Add the start and end points to the subset
            sub = pd.concat([sub, start.T, end.T], ignore_index=True)

            # add it to new giant variable that is the array of all subsets
            giant.append(sub)
            e_t = time.time()
            time_array = np.append(time_array, e_t - s_t)
        
        avg_time = np.mean(time_array)
        end_time = time.time()
        print(f"\tEach subset took an average of {round(avg_time, 5)} seconds")
        print(f"\tCreating subsets took {round(end_time - start_time, 5)} seconds\n")

    # heuristic function: greater return value means greater cost for the path (best path has low cost)
    def heur(self, x1, y1, z1, x2, y2, z2) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + height_factor * (z2 - z1) ** 2)
        #  + slope_factor * slope_angle(x1, y1, z1, x2, y2, z2)

    def heur_dist(self, x1, y1, x2, y2) -> float:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def distance(self, x1, y1, z1, x2, y2, z2) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    
    def process_subset(self, sub : pd.DataFrame):
        def heuristic1(node1, node2) -> float:
            x1, y1 = G.nodes[node1]['x'], G.nodes[node1]['y']
            x2, y2 = G.nodes[node2]['x'], G.nodes[node2]['y']
            return AStar.heur_dist(self, x1, y1, x2, y2)

        s_t = time.time()
        #sub = pd.read_csv(os.path.join(subsets_path, f"{subset_name}{k}.csv"))
        G = nx.Graph()

            # Add nodes from subset
        for i, row in sub.iterrows():
            G.add_node(i, x = row['x'], y = row['y'], z = row['z'])

            # Add edges between the closest nodes (ignoring height)
        coords = sub[['x', 'y']].values
        tree = spatial.KDTree(coords)
        for i, row in sub.iterrows():
            distances, indices = tree.query([row['x'], row['y']], k=depth+1)
            for j in range(1, len(indices)):  # skip the first index because it is the point itself
                G.add_edge(i, indices[j], weight=distances[j])

            # check if the graph is connected
        if not nx.is_connected(G):
                # start at a node. add an edge to the closest node that is not connected
                # repeat until the graph is connected
            start_node = sub.shape[0] - 2
            end_node = sub.shape[0] - 1
            while not nx.has_path(G, start_node, end_node):
                    # find the closest node that is not connected
                for i, row in sub.iterrows():
                    if not nx.has_path(G, start_node, i):
                        w = math.sqrt((sub.loc[start_node, 'x'] - sub.loc[i, 'x'])**2 
                                            + (sub.loc[start_node, 'y'] - sub.loc[i, 'y'])**2)
                        G.add_edge(start_node, i, weight=w)
                        break
            
            # Find the shortest path using A*
        path = nx.astar_path(G, sub.shape[0] - 2, sub.shape[0] - 1, heuristic=heuristic1)
        path = pd.Series(path)
        return sub.loc[path]
        
    def merge_subsets(self, start: pd.DataFrame, end: pd.DataFrame) -> pd.DataFrame:
        s_t = time.time()
        time_array = np.array([])

        path_points = pd.DataFrame(start.T, columns=["x", "y", "z"])

        # Define the heuristic function for A*
            # add path to path_points
        # cpu_count = mp.cpu_count
        with mp.Pool(processes=processes_param) as pool:
            result = pool.map(self.process_subset, giant)
        path_points = pd.concat(result, ignore_index=True)
        e_t = time.time()
        time_array = np.append(time_array, e_t - s_t)

        path_points.drop_duplicates(inplace=True, keep='first')
        path_points.reset_index(drop=True, inplace=True)
        # add end point to path_points
        path_points = pd.concat([path_points, end.T], ignore_index=True, axis=0)
        path_points.to_csv(path_points_path, index=False)

        avg_time = np.mean(time_array)
        end_time = time.time()
        print(f"\tPathing each subset took an average of {round(avg_time, 5)} seconds")
        print(f"\tMerging subsets took {round(end_time - s_t, 5)} seconds\n")
        return path_points
     
    
    def create_path(self, path_points: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        start_time = time.time()

        # make new graph using path_points
        G = nx.Graph()

        # Define the heuristic function for A*
        def heuristic2(node1, node2):
            x1, y1, z1 = G.nodes[node1]['x'], G.nodes[node1]['y'], G.nodes[node1]['z']
            x2, y2, z2 = G.nodes[node2]['x'], G.nodes[node2]['y'], G.nodes[node2]['z']
            return AStar.heur(self, x1, y1, z1, x2, y2, z2)

        # Add nodes from path_points
        for i, row in path_points.iterrows():
            G.add_node(i, x = row['x'], y = row['y'], z = row['z'])

        # Add edges between the closest nodes
        coords = path_points[['x', 'y', 'z']].values
        tree = spatial.KDTree(coords)
        for i, row in path_points.iterrows():
            _, indices = tree.query([row['x'], row['y'], row['z']], k=depth+1)
            for j in range(1, len(indices)):  # skip the first index because it is the point itself
                node1 = i
                node2 = indices[j]
                G.add_edge(node1, node2, weight=heuristic2(node1, node2))

        # check if the graph is connected
        if not nx.is_connected(G):
            # start at a node. add an edge to the closest node that is not connected
            # repeat until the graph is connected
            start_node = path_points.shape[0] - 2
            end_node = path_points.shape[0] - 1
            while not nx.has_path(G, start_node, end_node):
                # find the closest node that is not connected
                for i, row in path_points.iterrows():
                    if not nx.has_path(G, start_node, i):
                        w = heuristic2(start_node, i)
                        G.add_edge(start_node, i, weight=w)
                        break
        
        # Find the shortest path using A*
        path_i = nx.astar_path(G, 0, path_points.shape[0] - 1, heuristic=heuristic2)
        path_i = pd.Series(path_i)
        path_i = np.ndarray.flatten(path_i.to_numpy())
        path = path_points.loc[path_i]
        path = path.to_numpy()

        end_time = time.time()
        print(f"\tCreating path took {round(end_time - start_time, 5)} seconds")

        # get the cost of the path taken
        global cost
        for i in range(len(path_i) - 1):
            cost += heuristic2(path_i[i], path_i[i + 1])
        print(f"\tCost of path: {round(cost, 5)}\n")

        # get the length of the path taken
        global path_length
        for i in range(len(path) - 1):
            path_length += self.distance(path[i][0], path[i][1], path[i][2], path[i + 1][0], path[i + 1][1], path[i + 1][2])
        print(f"\tLength of path: {round(path_length, 5)}\n")

        return (path, path_i)
    
    def get_cost(self) -> float:
        return cost

    def get_path_length(self) -> float:
        return path_length
     
    """Finds the best path between point A and point B
    
    Args:
        pointA: point A with coordinates (x_a, y_a, z_a)
        pointB: point B with coordinates (x_b, y_b, z_b)
    
    Returns:
        Path of points through the graph representes as an array with shape (m, 3)
    """
    def find_path(self, point_a: np.ndarray, point_b: np.ndarray) -> np.ndarray:
        points = pd.read_csv(random_points_path)
        p_a = pd.DataFrame(point_a, index=['x', 'y', 'z'])
        p_b = pd.DataFrame(point_b, index=['x', 'y', 'z'])
        points = pd.concat([points, p_a.T, p_b.T], ignore_index=True, axis=0)
        points.drop_duplicates(inplace=True)
        AStar.create_subsets(self, points, p_a, p_b)
        path_points = AStar.merge_subsets(self, p_a, p_b)
        path, path_i = AStar.create_path(self, path_points)

        start_time = time.time()

        temp_path = pd.DataFrame(path, columns=['x', 'y', 'z'])
        temp_path.to_csv(path_path, index=False)
        path_i = pd.Series(path_i)
        path_i.to_csv(path_i_path, index=False)

        end_time = time.time()
        print(f"\tSaving path took {round(end_time - start_time, 5)} seconds\n")

        return path