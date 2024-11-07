import numpy as np

"""Class to find the most optimal path using A* algorithm for robotics. Target change in elevation
   and distance to target
"""
class AStar:
    """"Sets up the graph for the efficient path finding
    
    Args:
        data: numpy array with dimensions (n x 3)
    """
    def __init__(self, data: np.ndarray):
        pass
    
    
    
    
    """Finds the best path between point A and point B
    
    Args:
        pointA: point A with coordinates (x_a, y_a, z_a)
        pointB: point B with coordinates (x_b, y_b, z_b)
    
    Returns:
        Path of points through the graph representes as an array with shape (m, 3)
    """
    def find_path(self, pointA: np.ndarray, pointB: np.ndarray) -> np.ndarray:
        pass 
