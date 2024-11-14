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