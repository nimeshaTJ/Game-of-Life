import numpy as np
import pygame
import patterns
from GoLfuncs import *
import sys

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
	params = arg.split("/")
	array = None
	pattern = params[0]
	array = decode(patterns.patterns[pattern]["RLE"], patterns.patterns[pattern]["size"])
	origin = tuple(map(int,params[1].split(",")))
	for param in params[2:]:
		if param.isalpha():
			array = flip(array,param)
		else:
			array = rotate(array,int(param))
	size = [len(array),len(array[0])]
	fill_cells(initial_state, (origin), size, array)

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
			current_state = update(current_state)		
		
		pygame.display.update()
		clock.tick(frame_rate)

pygame.quit()
quit()
