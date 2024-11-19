# algorithms.py
import json
import math
import os
from dataclasses import dataclass
from typing import Tuple, List, Dict
import networkx as nx
import numpy as np
import pandas as pd
from scipy import spatial
from functools import lru_cache

@dataclass
class PathfinderConfig:
    """Configuration class to store pathfinding parameters"""
    depth: int
    subsets: int
    resolution: int
    height_factor: float
    max_slope: float
    slope_factor: float
    data_dir: str
    subsets_dir: str
    random_points_name: str
    path_points_name: str
    path_name: str
    path_i_name: str
    subset_name: str
    points_name: str
    start_point: List[float]
    end_point: List[float]
    x_offset: float 
    y_offset: float
    z_offset: float

    @classmethod
    def from_json(cls, filepath: str) -> 'PathfinderConfig':
        """Create config from JSON file"""
        with open(filepath, "r") as f:
            return cls(**json.load(f))

class AStar:
    """Optimized A* pathfinding implementation for robotics"""
    
    def __init__(self, config_path: str = "settings.json"):
        """Initialize AStar with configuration"""
        self.config = PathfinderConfig.from_json(config_path)
        self.subsets_cache: List[pd.DataFrame] = []
        self._setup_file_paths()
        
    def _setup_file_paths(self) -> None:
        """Set up file paths based on configuration"""
        self.random_points_path = os.path.join(self.config.data_dir, f"{self.config.random_points_name}.csv")
        self.path_points_path = os.path.join(self.config.data_dir, f"{self.config.path_points_name}.csv")
        self.path_path = os.path.join(self.config.data_dir, f"{self.config.path_name}.csv")
        self.path_i_path = os.path.join(self.config.data_dir, f"{self.config.path_i_name}.csv")

    @staticmethod
    @lru_cache(maxsize=1024)
    def _calculate_slope(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
        """Calculate slope angle between two points with caching"""
        v = np.array([(x2 - x1), (y2 - y1), (z2 - z1)])
        v_norm = np.linalg.norm(v)
        return 0 if v_norm == 0 else abs(math.degrees(math.acos(abs(z2 - z1) / v_norm)))

    @staticmethod
    @lru_cache(maxsize=1024)
    def _heuristic_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate 2D distance heuristic with caching"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    @lru_cache(maxsize=1024)
    def _heuristic_3d(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float, height_factor: float) -> float:
        """Calculate 3D distance heuristic with caching"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + height_factor * (z2 - z1) ** 2)

    def _create_graph_from_points(self, points: pd.DataFrame, use_3d: bool = False) -> nx.Graph:
        """Create graph from points with optimized edge creation"""
        G = nx.Graph()
        
        # Vectorized node addition
        node_data = {i: {'x': row['x'], 'y': row['y'], 'z': row['z']} 
                    for i, row in points.iterrows()}
        G.add_nodes_from(node_data.items())

        # Optimized edge creation using KD-Tree
        coords = points[['x', 'y', 'z'] if use_3d else ['x', 'y']].values
        tree = spatial.KDTree(coords)
        
        # Vectorized query for all points
        distances, indices = tree.query(coords, k=self.config.depth + 1)
        
        # Batch edge addition
        edges = [(i, idx, {'weight': dist}) 
                for i in range(len(points))
                for dist, idx in zip(distances[i, 1:], indices[i, 1:])]
        G.add_edges_from(edges)

        return G

    def create_subsets(self, points: pd.DataFrame, start: pd.DataFrame, end: pd.DataFrame) -> None:
        """Create optimized subsets of points"""
        points_per_subset = len(points) // self.config.resolution
        
        # Vectorized subset creation
        self.subsets_cache = [
            pd.concat([
                points.iloc[i * points_per_subset:(i + 1) * points_per_subset],
                start.T,
                end.T
            ], ignore_index=True)
            for i in range(self.config.subsets)
        ]

    def merge_subsets(self, start: pd.DataFrame, end: pd.DataFrame) -> pd.DataFrame:
        """Merge subsets with optimized pathfinding"""
        path_points = pd.concat([pd.DataFrame(columns=["x", "y", "z"]), start.T], 
                              ignore_index=True)

        for subset in self.subsets_cache:
            G = self._create_graph_from_points(subset)
            
            if not nx.is_connected(G):
                self._ensure_graph_connectivity(G, subset)
            
            # A* pathfinding with cached heuristic
            path = nx.astar_path(
                G, 
                subset.shape[0] - 2,
                subset.shape[0] - 1,
                heuristic=lambda n1, n2: self._heuristic_distance(
                    G.nodes[n1]['x'], G.nodes[n1]['y'],
                    G.nodes[n2]['x'], G.nodes[n2]['y']
                )
            )
            
            path_points = pd.concat([path_points, subset.loc[path]], 
                                  ignore_index=True)

        path_points = path_points.drop_duplicates(keep='first').reset_index(drop=True)
        return pd.concat([path_points, end.T], ignore_index=True)

    def find_path(self, point_a: np.ndarray, point_b: np.ndarray) -> np.ndarray:
        """Main pathfinding method with optimized workflow"""
        points = pd.read_csv(self.random_points_path)
        p_a = pd.DataFrame(point_a, index=['x', 'y', 'z'])
        p_b = pd.DataFrame(point_b, index=['x', 'y', 'z'])
        
        # Optimized point processing
        points = pd.concat([points, p_a.T, p_b.T], ignore_index=True).drop_duplicates()
        
        self.create_subsets(points, p_a, p_b)
        path_points = self.merge_subsets(p_a, p_b)
        path, path_i = self._create_final_path(path_points)
        
        # Save results
        pd.DataFrame(path, columns=['x', 'y', 'z']).to_csv(self.path_path, index=False)
        pd.Series(path_i).to_csv(self.path_i_path, index=False)
        
        return path
            

    def _create_final_path(self, path_points: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Create final optimized path"""
        G = self._create_graph_from_points(path_points, use_3d=True)
        
        if not nx.is_connected(G):
            self._ensure_graph_connectivity(G, path_points)
        
        path_i = nx.astar_path(
            G, 0, path_points.shape[0] - 1,
            heuristic=lambda n1, n2: self._heuristic_3d(
                G.nodes[n1]['x'], G.nodes[n1]['y'], G.nodes[n1]['z'],
                G.nodes[n2]['x'], G.nodes[n2]['y'], G.nodes[n2]['z'],
                self.config.height_factor
            )
        )
        
        return path_points.loc[path_i].to_numpy(), np.array(path_i)

    @staticmethod
    def _ensure_graph_connectivity(G: nx.Graph, points: pd.DataFrame) -> None:
        """Ensure graph connectivity with optimized edge addition"""
        start_node = points.shape[0] - 2
        end_node = points.shape[0] - 1
        
        while not nx.has_path(G, start_node, end_node):
            unconnected_nodes = [i for i in G.nodes if not nx.has_path(G, start_node, i)]
            if not unconnected_nodes:
                break
                
            closest_node = min(
                unconnected_nodes,
                key=lambda i: math.sqrt(
                    (points.loc[start_node, 'x'] - points.loc[i, 'x'])**2 +
                    (points.loc[start_node, 'y'] - points.loc[i, 'y'])**2
                )
            )
            G.add_edge(start_node, closest_node)