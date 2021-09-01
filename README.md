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

pattern_name/row,col/r/f

as an argument in the cmd command, where row and col are the coordinates where you want the pattern's origin to be placed (origin is at top right of pattern bounding box), r is the number of times you want the shape to be rotated 90° clockwise (1,2, or 3), and f is the axis you want the pattern to be flipped across (h or v). The positions of r and f are interchangeable. Preset patterns are stored in patterns.py, and to add new patterns simply update the dictionary with the name, dimensions of the pattern, and its RLE (Run Length Encoded) format. 

You can interact with the simulation with:

leftclick - add a live cell

rightclick - remove a live cell

drag the mouse to add/remove multiple cells

'Esc' - pause simulation

'Return' - resume simulation

'g' - toggle gridlines

'c' - clear all live cells

'f' - fill the screen with live cells

's' - save the current boardstate (enter desired name in terminal)

'a' - add a saved pattern onto the board (using above format)


# Version History
23/Aug/2021 - First iteration of Game of Life. Supports user interaction (pausing, resuming, placing/removing cells, toggling gridlines), however simulation breaks at the edges.

27/Aug/2021 - Added ability to clear screen with "c", fill screen with "f", and click+drag the mouse to add/remove multiple cells fluidly. Also updated so that the grid lies on a toroid and wraps around edges. Added ability to place a preset pattern onto the board from the command line. Presets are stored in patterns.py.

28/Aug/2021 - patterns.py now stores patterns in their RLE format, which GameofLife.py decodes into point coordinates and places on the board.

29/Aug/2021 - Added ability to rotate and flip patterns before placing on the grid.

01/Sep/2021 - Changed patterns.py to patterns.json; added ability to save the current boardstate to patterns.json

01/Sep/2021 - Can add patterns to board with 'a'; custom error messages

