# Game-of-Life
An implementation of Conway's Game of Life, where the user can choose to pause the simulation and dynamically add or remove cells.


# Instructions

## Setup
Clone project and install requirements:
```console
$ git clone https://github.com/nimeshaTJ/Game-of-Life.git
$ cd Game-of-Life
$ pip install -r requirements.txt
```

## Usage
To place a preset pattern on the board on startup, type 

pattern_name@x,y

as an argument in the cmd command, where x and y are the coordinates where you want the pattern to be placed. Preset patterns are stored in patterns.py, and to add new patterns simply update the dictionary with the name, dimensions of the pattern, and the points relative to its boundary box. 

You can interact with the simulation with:

'Esc' - pause simulation

'Return' - resume simulation

'g' - toggle gridlines

'c' - clear all live cells

'f' - fill the screen with live cells

leftclick - add a live cell

rightclick - remove a live cell

drag the mouse to add/remove multiple cells 


# Version History
23/Aug/2021 - First iteration of Game of Life. Supports user interaction (pausing, resuming, placing/removing cells, toggling gridlines), however simulation breaks at the edges.

27/Aug/2021 - Added ability to clear screen with "c", fill screen with "f", and click+drag the mouse to add/remove multiple cells fluidly. Also updated so that the grid lies on a toroid and wraps around edges. Added ability to place a preset pattern onto the board from the command line. Presets are stored in patterns.py.
