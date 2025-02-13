import pandas as pd
import numpy as np
import random
import pyhigh
import networkx as nx
import matplotlib.pyplot as plt
from utilities import euclidean
from kdtree import KDTree, KDNode

RANGE = 10
BASE = 1360
LOWER_BOUND = BASE - RANGE 
UPPER_BOUND = BASE + RANGE
EQUAL_DISTANCE = 1e-10
K = 20000
Q = 0.01
GREEDY_WEIGHT = 0.2
X_STD = 0.008
Y_STD = 0.01



class RRT:
    """Implementation of Rapidly Expanding Random Tree algorithm for efficient path search
    """

    def _find_obstacles(self, data, lower_bound=LOWER_BOUND, upper_bound=UPPER_BOUND):
        pass



    """Initializes RRT with obstacles to avoid

    Args:
        traversable - points that you can traverse on as a matrix with (n x d) dimensionality
    """
    def __init__(self, data, lower_bound=LOWER_BOUND, upper_bound=UPPER_BOUND, greedy_weight=GREEDY_WEIGHT, Q=Q):
        ## Prepare kdtree for obstacles
        self._data = data
        self.data = data.drop("Altitude", axis=1)
        self.x_mean = data["Latitude"].mean()
        self.x_std = data["Latitude"].std()
        self.y_mean = data["Longtitude"].mean()
        self.y_std = data["Longtitude"].std()
        self.data["Latitude"] = (self.data["Latitude"] - self.x_mean) / self.x_std
        self.data["Longtitude"] = (self.data["Longtitude"] - self.y_mean) / self.y_std


        self.f = lambda p: ((p[0] - self.x_mean) / self.x_std, (p[1] - self.y_mean) / self.y_std)
        self.inv = lambda p: (p[0] * self.x_std + self.x_mean, p[1] * self.y_std + self.y_mean)
        
        self.xmin = self.data["Latitude"].min()
        self.xmax = self.data["Latitude"].max()
        self.ymin = self.data["Longtitude"].min()
        self.ymax = self.data["Longtitude"].max()

        self.greedy_weight = greedy_weight
        self.Q = Q

    

    def random_config(self, end):
        if np.random.uniform() <= self.greedy_weight:
            return end 
        else:
            point_x = np.random.uniform(self.xmin, self.xmax)
            point_y = np.random.uniform(self.ymin, self.ymax)
            return (point_x, point_y)


    def set_obstacles(self, start):
        """Sets obstacles based on starting location of traversal

        Args:
            start - start point of traversal in GPS coordinates
        """

        x, y = start
        altitude = pyhigh.get_elevation(x, y)
        lower_bound, upper_bound = altitude - RANGE, altitude + RANGE

        df = self._data.query(f"Altitude < {lower_bound} or Altitude > {upper_bound}").drop("Altitude", axis=1)
        df["Latitude"] = (df["Latitude"] - self.x_mean) / self.x_std
        df["Longtitude"] = (df["Longtitude"] - self.y_mean) / self.y_std

        self._obstacles = df 
        self.obstacles = KDTree()
        for _, v in df.iterrows():
            self.obstacles.insert(tuple(v))

    
    def build_RRT(self, start, end):
        """Builds RRT tree from the starting point to the end

        Args:
            start - start point of traversal
            end - end point of traversal

        """
        graph = nx.Graph()
        graph.add_node(start)
        adjacency_graph = KDTree()
        adjacency_graph.insert(start)

        end_approximate = None 
        for i in range(K):
            node_rand = self.random_config(end)
            node_near = adjacency_graph.find_neighbour(node_rand)
            node_new = tuple(np.array(node_near) + self.Q * (np.array(node_rand) - np.array(node_near)))
            
            if euclidean(node_new, self.obstacles.find_neighbour(node_new)) < EQUAL_DISTANCE:
                continue 

            print(f"Iteration #{i}")
            print(f"Generated a point {node_new}")
            temp = adjacency_graph.find_neighbour(end)
            print(f"Distance to target is {euclidean(temp, end)}")


            graph.add_node(node_new)
            graph.add_edge(node_near, node_new)
            adjacency_graph.insert(node_new)

            
            if euclidean(node_new, end) < EQUAL_DISTANCE:
                end_approximate = node_new
                break 

        
        return graph, end_approximate
    

    def _visualize_path(self, path: list[tuple]):
        """Visualizes the path found when running algorithm

        Args:
            path - list of generated points from start to finish

        Returns
            plot representing points on the map and obstacles along the way
        """

        fig, ax = plt.subplots()
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)

        ax.scatter(self._obstacles["Latitude"], self._obstacles["Longtitude"])
        path_x = [x for x, _ in path]
        path_y = [y for _, y in path]
        ax.plot(path_x, path_y, c="red")
        plt.show()


    def find_path(self, start, end, show_path=False) -> list:
        """Finds the path from start to end which avoids obstacles

        Args:
            start - start point of traversal
            end - end point of traversal

        Returns:
            path from start to end.
        """

        """
        if isinstance(start, np.ndarray):
            start = tuple(start)
        if isinstance(end, np.ndarray):
            end = tuple(end)

        graph, end_approximate = self.build_RRT(start, end)
        path = nx.astar_path(graph, start, end_approximate, heuristic=lambda x, y: euclidean(x, y))
        return np.array(path)
        """
        if isinstance(start, np.ndarray):
            start = tuple(start)
        if isinstance(end, np.ndarray):
            end = tuple(end)

        self.set_obstacles(start)
        start = self.f(start)
        end = self.f(end)

        graph, end_approximate = self.build_RRT(start, end)
        path = nx.astar_path(graph, start, end_approximate, heuristic=lambda x, y: euclidean(x, y)) 
        if show_path:
            self._visualize_path(path)

        result = [self.inv(point) for point in path]
        return result


def main():
    df = pd.read_csv("./csv/gps_coordinates_truncated.csv")
    start = np.array([38.36287602583417,-110.84005888328151])
    end = np.array([38.38101409945085,-110.81949324992496])

    tree = RRT(data=df)
    print(tree.find_path(start, end))



if __name__ == '__main__':
    main()
