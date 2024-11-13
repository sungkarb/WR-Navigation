import pandas as pd
import math
import numpy as np
import random as random
import networkx as nx
from scipy import spatial
import os

# file paths and names
data_dir = "data"
subsets_dir = "subsets"
random_points_name = "random_points"
path_points_name = "path_points"
path_name = "path"
subset_name = "subset"

random_points_path = os.path.join(data_dir, f"{random_points_name}.csv")
path_points_path = os.path.join(data_dir, f"{path_points_name}.csv")
path_path = os.path.join(data_dir, f"{path_name}.csv")
subsets_path = os.path.join(subsets_dir, f"{subset_name}")

# Hyperparameters and variables

# number of edges per node in the graph
depth = 4

# number of subsets/subgraphs (ideally subsets == resolution)
subsets = 2000

# higher resolution = less points. effective resolution = subsets/resolution
resolution = 2000

# height importance factor
height_factor = 1000

# max tolerated slope angle (degrees) UNUSED
max_slope = 40

# slope importance factor UNUSED
slope_factor = 0.005

# giant array
giant = []

"""Class to find the most optimal path using A* algorithm for robotics. Target change in elevation
    and distance to target
"""
class AStar:
    """"Sets up the graph for the efficient path finding
    
    Args:
        data: numpy array with dimensions (n x 3)
    """
    def __init__(self, data: np.ndarray):
        # process data
        points = pd.DataFrame(data, columns=['x', 'y', 'z'])
        points.drop_duplicates(inplace=True)
        points.sample(frac=1).reset_index(drop=True).to_csv(random_points_path, index=False)

    # helper methods
    def slope_angle(self, x1, y1, z1, x2, y2, z2):
        # v dot w = |v||w|cos(theta)
        # theta = arccos(v dot w / |v||w|)
        v = np.array([(x2 - x1), (y2 - y1), (z2 - z1)])
        w = np.array([0, 0, 1])
        v_norm = np.linalg.norm(v)
        if v_norm == 0:
            return 0
        return abs(math.degrees(math.acos(abs(z2 - z1) / v_norm)))
    
    def create_subsets(self, points: pd.DataFrame, start: pd.DataFrame, end: pd.DataFrame):
        # Number of points per subset based on resolution
        points_per_subset = len(points) // resolution

        for i in range(subsets):
            # Select the subset of points with points_per_subset points
            sub = points.iloc[i * points_per_subset:(i + 1) * points_per_subset].copy()
            
            # Add the start and end points to the subset
            sub = pd.concat([sub, start.T, end.T], ignore_index=True)

            # add it to new giant variable that is the array of all subsets
            giant.append(sub)

    # heuristic function: greater return value means greater cost for the path (best path has low cost)
    def heur(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + height_factor * (z2 - z1) ** 2)
        #  + slope_factor * slope_angle(x1, y1, z1, x2, y2, z2)

    def heur_dist(self, x1, y1, z1, x2, y2, z2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def merge_subsets(self, start: pd.DataFrame, end: pd.DataFrame) -> pd.DataFrame:
        path_points = pd.DataFrame(columns=["x", "y", "z"])
        path_points = pd.concat([path_points, start.T], ignore_index=True, axis=0)
        
        # Define the heuristic function for A*
        def heuristic1(node1, node2):
                    x1, y1, z1 = G.nodes[node1]['x'], G.nodes[node1]['y'], G.nodes[node1]['z']
                    x2, y2, z2 = G.nodes[node2]['x'], G.nodes[node2]['y'], G.nodes[node2]['z']
                    return AStar.heur_dist(self, x1, y1, z1, x2, y2, z2)
        for k in range(subsets):
            #sub = pd.read_csv(os.path.join(subsets_path, f"{subset_name}{k}.csv"))
            sub = giant[k]
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
                                    w = math.sqrt((sub.loc[start_node, 'x'] - sub.loc[i, 'x'])**2 + (sub.loc[start_node, 'y'] - sub.loc[i, 'y'])**2)
                                    G.add_edge(start_node, i, weight=w)
                                    break

            # Find the shortest path using A*
            path = nx.astar_path(G, sub.shape[0] - 2, sub.shape[0] - 1, heuristic=heuristic1)
            path = pd.Series(path)
            
            # add path to path_points
            path_points = pd.concat([path_points, sub.loc[path]], ignore_index=True, axis=0)

            path_points.drop_duplicates(inplace=True, keep='first')
            path_points.reset_index(drop=True, inplace=True)
            # add end point to path_points
            path_points = pd.concat([path_points, end.T], ignore_index=True, axis=0)
            path_points.to_csv(path_points_path, index=False)
            return path_points
     
    def create_path(self, path_points: pd.DataFrame) -> np.ndarray:
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
            distances, indices = tree.query([row['x'], row['y'], row['z']], k=depth+1)
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
        return path
     
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
        path = AStar.create_path(self, path_points)
        temp_path = pd.DataFrame(path, columns=['x', 'y', 'z'])
        temp_path.to_csv(path_path, index=False)
        return path
