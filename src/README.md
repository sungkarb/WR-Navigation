# Improvements (not in any particular order, please help me)
- Optimize everything (`algorithms.py` mainly)
- Add `json` configuration files for the scripts (and create a separate directory for them)
- Add in the unimplemented features/files
    - Max slope setting (set it to 45 degrees): the path is limited by this slope
    - `runtime.py` script:
        - Estimates the time it takes to find a path given certain parameters
    - Documentation for everything
        - `algorithms.py` has some (outdated) but none of the other files do
- Everything is a DataFrame since I don't know how to use the numpy library
    - Convert things to Numpy: np.ndarray types
# How to use the data logger
- *See also:* [*`logdata.py`* docs](#logdata)
## Setup for `logdata.py`
- Open `logdata.py`
- Edit the data logging parameters at the top
- Ensure that you have enough time to run the files
	- Assume each iteration takes 5 minutes
- Data will be uploaded to `src/logs/log.csv/`
- If you want to run the data logger again, make sure to save the previous run (rename the file) or else all of the new data will be added to the same file
# `algorithms.py` docs {#algorithms}
## About
- File that encapsulates the path-finding process. Uses a *"divide and conquer"* like strategy to break up the dataset into sparser subsets, and then recompiles the subsets before using the A\* algorithm to create the final path. 
## Parameters (settings.json) {#parameters}
- `depth`: int
	- Controls the maximum number of edges a node may have in any of the graphs used in path-finding (both for the subsets and for the main path)
- `subsets`: int
	- Number of subsets to take from the set of all points. Increase in `subsets` = more data = takes longer to run = higher effective resolution
- `resolution`: int
	- Each subset will have 1 point per <resolution\> number of points of the full set of points. Increase in `resolution` = less effective resolution. (Totally not confusing)
- `height_factor`: float
	- Weight of change in elevation in the path-finding heuristic function used in method  `create_path()`. Increase in `height_factor` = more emphasis in finding the flattest path (ideally)
- `max_slope`: float | UNUSED
	- The maximum slope that the path is allowed to have. In degrees, must be a positive number. Increase in `max_slope` = path may go up and down more = less safe but potentially faster path
- `slope_factor`: float | UNUSED
	- The weight of the slope in the path-finding heuristic function used in method `create_path()`. Increase in `slope_factor` = more emphasis in finding a less hilly path

## Variables {#variables}
- `giant`: array
	- Array of all of the subsets to be used
- `points`: array
	- Stores all of the points (randomized order). Used in forming the subsets
- `path_points`: array
	- Stores all of the points after every subset gets processed. These points are used to then find the best path in method `create_path()`
-  `path`: array
	- Stores all of the points used in the best path including the start and end points. Calculated in method `create_path()`
- `path_i`: array
	- Stores the indices of points that `path` uses from the array `path_points`

## Methods
- `__init__(self)`: returns None
	- Updates subsets and resolution appropiately
- `slope_angle(self, x1, y1, z1, x2, y2, z2)`: returns float | UNUSED
	- `args`: the coordinates of the two vectors to be operated on
	- Finds the absolute value of the angle in degrees between the two vectors
	- Doesn't work (i forgot how vectors work lol)
	- Returns the angle calculated
- `create_subsets(self, points: pd.DataFrame, start: pd.DataFrame, end: pd.DataFrame)`: returns None
	- `points`: the array of points to be operated on
	- `start`: the coordinate of the start of the path
	- `end`: the coordinate of the end of the path
	- Generates a random subsample of `points` specified by parameters `subsets` and `resolution`. `start` and `end` will be added to each subset.
- `heur(self, x1, y1, z1, x2, y2, z2)`: returns float
	- `args`: the two point coordinates to be operated on
	- The heuristic function used in method `create_path()`.
	- Returns the weight of the edge between the two nodes
- `heur_dist(self, x1, y1, x2, y2)`: returns float
	- `args` the two points coordinates to be operated on
	- The heuristic function used in method `merge_subsets()`. Only used the x and y coordinates to make a grid-like pattern of edges in the graphs of the subsets. Ask me for more details if you're curious
	- Returns the weight of the edge between the two nodes
- `merge_subsets(self, start: pd.DataFrame, end: pd.DataFrame)`: returns pd.DataFrame
	- `start`: the start point of the path
	- `end`: the end point of the path
	- Uses variable `giant` to iterate through each subset and finds the shortest path in the x-y plane (ignores elevation), then adds that to variable `path_points`
	- Returns an array of all points that were a part of a path in a subset, including the start and end points
- `create_path(self, path_points: pd.DataFrame)`: returns (np.ndarray, np.ndarray)
	- `path_points`: the points generated by method `merge_subsets()`
	- Calculates the best path from the start point the end point using heuristic function `heur`
	- Returns the points of the path and the indices of the path points relative to variable `path_points`
## Other notes/terms
- Effective resolution is the fraction of points used from variable `points`. For example, if it says "Effective Resolution: 0.1 (500/5000)" then you are using one tenth of all points in finding the best path, and are doing so with 500 subsets, with each subset having 1/5000 points from the variable `points`
# `logdata.py` docs {#logdata}
## About
- A driver of `algorithms.py` that logs the data related to the path generated. Logs subsets, resolution, A* time, total time, number of points, cost of path, and path length into a `csv` file.
- This data is available to view using `plotdata.py`
- *See also:* [*`plotdata.py`* docs](#plotdata)
## Parameters
- ` s_rsn`: int
    - The starting resolution. The logger will begin logging at this specified resolution. 
    - *See also:* [*`algorithms.py`* Parameters: resolution](#parameters)
- `e_rsn`: int
    - The ending resolution (inclusive). The logger will still collect data at this resolution.
- `rsn_step`: int
    - The step size for resolution. The second resolution run by the data logger will be at `s_rsn + rsn_step`. These "steps" will be taken until `e_rsn` is hit.
- `sub_step`: int
    - The starting and step number of subsets that the data logger will use. These "steps" will be taken until the target resolution is hit, then the number of subsets will be reset once the next resolution is being run. 
    - *See also:* [*`algorithms.py`* Parameters: subsets](#parameters)
# `plotdata.py` docs {#plotdata}
## About
- Plots key data generated by `logdata.py`.
- *See also:* [*`logdata.py`* docs](#logdata)
# `runtime.py` docs
TODO: implement all features
## About
- Estimates how long `algorithms.py` will take to calculate a path. Takes in a data log created by `logdata.py` and outputs an estimated runtime based on:
    - Subsets
    - Resolution
    - Points dataset (or path to one)
    - * See also: [`algorithms.py`](#algorithms)
- Additionally, it will make your computer calculate some paths so it can estimate how long it will take your own computer to run.
- Still needs to be implemented (someone plz help)
# `process.py` docs
## About
- Processes a `csv` dataset of points: reorganizes the columns, applies the offsets given in `settings.json`, and stores this file into the `src/data/` directory. Also stores a separate `csv` file of the data with randomized indices so it can be used by `algorithms.py`.
# `visualize.py` docs
## About
- Plots the path most recently generated onto a 3d graph, along with the points from `path_points`.
- *See also:* [*`algorithms.py`* Variables: path\_points](#variables)