#Function that fills in patterns on the board given a list of coordinates and an origin point
def fill_cells(grid,origin,size,points):
	subgrid = grid[origin[0]:origin[0]+size[0],origin[1]:origin[1]+size[1]]
	for point in points:
		subgrid[point[0],point[1]] = 1

#Function that decodes RLE format into coordinate points
def decode(rle):
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
	points = []

	for rowindex,line in enumerate(lines):
		for colindex,value in enumerate(line):
			if value == 'o':
				points.append((rowindex,colindex))
			elif value == '!':
				return points

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
