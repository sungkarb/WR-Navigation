import heapq
import numpy as np

# Heuristic function to estimate distance to the goal
def heuristic(node, goal):
    return np.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2)

# Function to get neighbors of a node
def get_neighbors(node, grid):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Down, Left, Right
    for d in directions:
        neighbor = (node[0] + d[0], node[1] + d[1])
        if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
            if grid[neighbor[0], neighbor[1]] == 0:  # Check if traversable
                neighbors.append(neighbor)
    return neighbors

# Main A* algorithm
def a_star(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current, grid):
            tentative_g_cost = g_cost[current] + 1  # Assuming uniform cost for simplicity
            
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_cost
                f_cost[neighbor] = g_cost[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_cost[neighbor], neighbor))
    
    return None  # Return None if no path is found

# Function to reconstruct the path
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
