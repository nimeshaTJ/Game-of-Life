import numpy as np
import pygame
import patterns
import sys

#Function that fills in patterns on the board given a list of coordinates and an origin point
def fill_cells(origin,size,points):
	subgrid = initial_state[origin[0]:origin[0]+size[0],origin[1]:origin[1]+size[1]]
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
def update():
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

#Function to draw the current state of all cells (white for living cells, black for dead cells)
def draw_grid():
	gameDisplay.fill(black)
	for rowindex, row in enumerate(current_state):

		for colindex, value in enumerate(row):

			if value == 1:
				pygame.draw.rect(gameDisplay,white,[colindex*cell_size,rowindex*cell_size,cell_size,cell_size])
			if gridlines==True:
				pygame.draw.rect(gameDisplay,grey,[colindex*cell_size,rowindex*cell_size,cell_size,cell_size], 1)

pygame.init()

#Parameters for the simulation 
display_height = 720
display_width = 1000
cell_size = 10
num_rows = display_height//cell_size
num_cols = display_width//cell_size
gridlines = False
frame_rate = 120

#Defining colours
white = (255,255,255)
black = (0,0,0)		
grey = (50,50,50)

#Initializing the array of cells
initial_state = np.zeros((num_rows,num_cols))

#Adding user-specified patterns 
for arg in sys.argv[1:]:
	origin = tuple(map(int,arg.split("@")[1].split(",")))
	pattern = arg.split("@")[0]
	points = decode(patterns.patterns[pattern]["RLE"])
	fill_cells((origin),patterns.patterns[pattern]["size"], points )

#Copy of initial state from which values will be read 
current_state = initial_state

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
crashed = False
paused = True
	
if __name__ == "__main__":

	while not crashed:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				crashed = True

			pos = pygame.mouse.get_pos()
			coords = [pos[1]//cell_size, pos[0]//cell_size]
			pressed = pygame.mouse.get_pressed()

			#Allows user to place or remove cells by holding down the mouse
			if pressed[0] == True:
				current_state[coords[0], coords[1]] = 1
			if pressed[2] == True:
				current_state[coords[0], coords[1]] = 0

			#Allows user to toggle gridlines, pause, resume, and clear the screen		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:
					gridlines = not gridlines
				if event.key == pygame.K_RETURN:
					paused = False	
				if event.key == pygame.K_ESCAPE:
					paused = True		
				if event.key == pygame.K_c:
					current_state[:,:] = 0
				if event.key == pygame.K_f:
					current_state[:,:] = 1
		draw_grid()
		if paused == False:
			current_state = update()		
		
		pygame.display.update()
		clock.tick(frame_rate)

pygame.quit()
quit()
