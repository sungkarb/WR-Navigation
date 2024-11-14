# WR-Navigation
Navigation through terrain with Python!

# Installation
Run command in your visual studio code terminal as follows
```bash
.\setup.ps1
```
If you prefer Linux, use this file instead 
```bash
.\setup.sh
```
# Usage
In future, you just activate your virtual python environment as 
```bash
.\robotics\Scripts\activate
```

## Setup
- Open up terminal and type `bash`
	- (so now most of these instructions work on both Windows and Mac)
- Clone this branch into wherever you want it
```bash
git clone -b isaac https://github.com/sungkarb/WR-Navigation.git
```
- You may now close this terminal
- In Visual Studio Code, open up the directory `WR-Navigation` using the either the menu, `Ctrl-O`, or `Cmd-O`
- Follow the README to setup the virtual python environment
- Keep the vscode terminal open after

### Windows users
- Install any necessary python libraries listed here:
```bash
pip install networkx
pip install numpy
pip install pandas
pip install scipy
pip install matplotlib
pip install laspy lazrs
```
- Run `setup.py` to initialize necessary data
```bash
python setup.py
```
- Open up `settings.json` in the `src` folder and configure as needed (start and end points)
- When you are ready to run the program (in the same terminal as before)
```bash
python main.py
```
- To see the results, you may run `visualize.py`
```bash
python visualize.py
```
### Mac users
- Install any necessary python libraries listed here:
```bash
pip3 install networkx
pip3 install numpy
pip3 install pandas
pip3 install scipy
pip3 install matplotlib
pip3 install laspy lazrs
```
- Run `setup.py` to initialize necessary data
```bash
python3 setup.py
```
- Open up `settings.json` in the `src` folder and configure as needed (start and end points)
- When you are ready to run the program (in the same terminal as before)
```bash
python3 main.py
```
- To see the results, you may run `visualize.py`
```bash
python3 visualize.py
```
gg ez

# algorithms.py docs
## Parameters (settings.json)
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

## Variables
- `giant`: array
	- Array of all of the subsets to be used
- `points`: array
	- Stores all of the points (randomized order). Used in forming the subsets
- `path_points`: array
	- Stores all of the points after every subset gets processed. These points are used to then find the best path in method `create_path()`
-  `path`: array
	- Stores all of the points used in the best path including the start and end points. Calculated in method `create_path`
- `path_i`: array
	- Stores the indices of points that `path` uses from the array `path_points`

## Methods
- `__init__(self, data: np.ndarray)`: returns None
	- `data`: the array of points that will be operated on
	- Takes in `data`, removes duplicate entries, randomizes the order of the coordinates. (This is needed for the generation of subsets)
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
## Things that could be a lot better but im bad at coding
- Optimize everything maybe
- Add in the unimplemented features
- Everything is a DataFrame since I don't know how to use the numpy library
- It is 2:21 AM