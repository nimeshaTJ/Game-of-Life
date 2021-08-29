import numpy as np

#Function that fills in patterns on the board given an origin point and a list of coordinates or an array 
def fill_cells(grid,origin,size,points):
		if type(points) == list:
			subgrid = grid[origin[0]:origin[0]+size[0],origin[1]:origin[1]+size[1]]
			for point in points:
				subgrid[point[0],point[1]] = 1
		else:
			grid[origin[0]:origin[0]+size[0],origin[1]:origin[1]+size[1]] = points

#Function that flips a given pattern vertically pr horizontally
def flip(array,axis):
	flipped = array.copy()
	num_rows = len(array)
	num_cols = len(array[0])
	for rowindex, row in enumerate(array):
		for colindex, value in enumerate(row):
			if axis == 'v':
				flipped[(num_rows-1)-rowindex,colindex] = value
			else:
				flipped[rowindex,(num_cols-1)-colindex] = value
	return flipped

#Function that rotates a given pattern 90° clockwise 'rotations' times
def rotate(array,rotations):
	rotated = array.copy()
	for n in range(rotations):
		rotated = rotated.transpose()
		rotated = flip(rotated,'h')
	return rotated

#Function that decodes RLE format into an array of cells
def decode(rle,size):
	expanded = ''
	multiple = ''

	for c in rle:
		if c.isnumeric():
			multiple += c
		else:
			if multiple=='':
				expanded += c
			else:
				expanded += c*int(multiple)
			multiple = ''

	lines = expanded.split("$")
	array = np.zeros((size[0],size[1]))

	for rowindex,line in enumerate(lines):
		for colindex,value in enumerate(line):
			if value == 'o':
				array[rowindex,colindex] = 1
			elif value == '!':
				return array

#Function that calculates and returns the state of all cells at the next timestep
def update(current_state):
	num_rows = len(current_state)
	num_cols = len(current_state[0])
	#Temporary variable to store the state of all cells at the next timestep
	next_state = current_state.copy()
	#Iterating through the array of cells
	for rowindex, row in enumerate(next_state):

		for colindex, value in enumerate(row):
			#Counting the number of living cells around each cell 
			live_cells = current_state[rowindex-1,colindex-1]+current_state[rowindex-1,colindex]+current_state[rowindex-1,(colindex+1)%num_cols]+ \
					  current_state[rowindex,colindex-1]+current_state[rowindex,(colindex+1)%num_cols]+current_state[(rowindex+1)%num_rows,colindex-1]+ \
					  current_state[(rowindex+1)%num_rows,colindex]+current_state[(rowindex+1)%num_rows,(colindex+1)%num_cols]
						
			#Enforcing the Game of Life ruleset
			if ((live_cells == 2 or live_cells == 3) and value == 1) or (live_cells == 3 and value == 0):
				next_state[rowindex,colindex] = 1
			else:
				next_state[rowindex,colindex] = 0

	return next_state.copy()
