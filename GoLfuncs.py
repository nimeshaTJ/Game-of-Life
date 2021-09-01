import numpy as np

#Function that adds a pattern to the board given a pattern name, origin and transformations
def place_pattern(params, patterns, grid):
	param_list = params.split("/")
	array = None
	pattern = param_list[0]
	if pattern not in patterns:
		print("\nNo such pattern saved.\n")
		return None
	if len(param_list)<2:
		print("Invalid format. Please try again.")
		return None
	array = decode(patterns[pattern]["RLE"], patterns[pattern]["size"])
	origin = tuple(map(int,param_list[1].split(",")))
	for param in param_list[2:]:
		if param.isalpha():
			array = flip(array,param)
		else:
			array = rotate(array,int(param))
	fill_cells(grid, origin, array)

#Function that fills in patterns on the board given an origin point and a list of coordinates or an array 
def fill_cells(grid,origin,points):
	try:
		if type(points) == list:
			subgrid = grid[origin[0]:,origin[1]:].copy()
			for point in points:
				subgrid[point[0],point[1]] = 1
			grid[origin[0]:,origin[1]:] = subgrid.copy()
		else:
			size = [len(points), len(points[0])]
			grid[origin[0]:origin[0]+size[0],origin[1]:origin[1]+size[1]] = points
	except (ValueError,IndexError) as error:
		print("\nCannot fit pattern on board. Try a different pattern or origin.\n")

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

#Function that encodes an array of cells into RLE format
def encode(array):

	leftcols2strip = len(array[0])
	for row in array:
		leading0s = 0
		index = 0
		while row[index]==0:
			leading0s+=1
			if index<len(row)-1:
				index+=1
			else:
				break
			
		if leading0s<leftcols2strip:
			leftcols2strip = leading0s

	leftstrip = array[:,leftcols2strip:]
	rle = ''
	for rowindex,row in enumerate(leftstrip):
		for colindex,value in enumerate(row):
			if value == 0:				
				rle += 'b'
			else:
				rle += 'o'
		if rowindex < len(leftstrip)-1:	
			rle += '$'
	
	split = rle.split('$')
	for rowindex,row in enumerate(split):
		split[rowindex] = row.rstrip('b')

	rle = '$'.join(split).strip('$')
	split = rle.split('$')
	final = ''
	multiple = 1
	for index,value in enumerate(rle[1:]):
		if rle[index] == value:
			multiple += 1
			if index == len(rle)-2:
				final+=(str(multiple)+value)
		else:
			if multiple>1:
				final+=(str(multiple)+rle[index])
			else:
				final+=rle[index]
			if index == len(rle)-2:
				final+=value
			multiple = 1

	num_rows = len(split)
	num_cols = 0
	for row in split:
		count = 0
		for value in row:
			count+=1
		if num_cols<count:
			num_cols = count
	final+='!'
	size = [num_rows,num_cols]
	return final, size 		

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
