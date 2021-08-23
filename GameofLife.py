import numpy as np
import pygame

def fill_cells(points):
	for point in points:
		initial_state[point[0]+1,point[1]+1] = 1

def update():
	
	next_state = current_state.copy()
	for rowindex, row in enumerate(next_state[1:-1]):

		for colindex, value in enumerate(row[1:-1]):

			subgrid = current_state[rowindex:rowindex+3,colindex:colindex+3].copy()
			subgrid[1,1] = 0
			live_cells = np.count_nonzero(subgrid==1)
			
			if ((live_cells == 2 or live_cells == 3) and value == 1) or (live_cells == 3 and value == 0):
				next_state[rowindex+1,colindex+1] = 1
			else:
				next_state[rowindex+1,colindex+1] = 0

	return next_state.copy()

def draw_grid():

	gameDisplay.fill(black)
	for rowindex, row in enumerate(current_state[1:-1]):

		for colindex, value in enumerate(row[1:-1]):

			if value == 1:
				pygame.draw.rect(gameDisplay,white,[colindex*cell_size,rowindex*cell_size,cell_size,cell_size])
			if gridlines==True:
				pygame.draw.rect(gameDisplay,grey,[colindex*cell_size,rowindex*cell_size,cell_size,cell_size], 1)

pygame.init()

display_height = 720
display_width = 1000
cell_size = 10
white = (255,255,255)
black = (0,0,0)		
grey = (50,50,50)
gridlines = False

initial_state = np.zeros((int(display_height/cell_size)+2,int(display_width/cell_size)+2))
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
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				coords = [int(pos[1]/cell_size)+1, int(pos[0]/cell_size)+1]
				if event.button == 1:
					current_state[coords[0], coords[1]] = 1
				if event.button == 3:
					current_state[coords[0], coords[1]] = 0

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_g:
					gridlines = not gridlines
				if event.key == pygame.K_RETURN:
					paused = False	
				if event.key == pygame.K_ESCAPE:
					paused = True		
		
		draw_grid()
		if paused == False:
			current_state = update()		
		
		pygame.display.update()
		clock.tick(20)

pygame.quit()
quit()