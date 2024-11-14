## Setup
- Open up terminal and type `bash`
	- (so now most of these instructions work on both Windows and Mac)
- Clone this branch into wherever you want it
```bash
git clone -b isaac https://github.com/sungkarb/WR-Navigation.git
```
- cd into the repository
```bash
cd WR-Navigation/src/
```

### Windows users
- Install any necessary python libraries listed here:
```bash
pip install networkx
pip install numpy
pip install pandas
pip install scipy
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