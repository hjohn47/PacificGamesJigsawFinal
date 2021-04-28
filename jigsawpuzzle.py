#!/usr/bin/env python3
"""
	The puzzle game.
"""

import pygame
import os
import sys
from functions.soundsinit import init
from random import randrange,choice,shuffle 
from glob import glob
from PIL import Image
import subprocess

__author__ = "Hailey Johnson, Krikor Herlopian, Charitha Sree Jayaramireddy , Syrina Haldiman and Tatiyana Bramwell"
__copyright__ = "Copyright 2021, University of New Haven Final Project"

imageSelected = ''
blacktile  = None
playing = True
postCongratulations = False
def grab(screen, x, y, width, height):
	"Grab part of screen blit on => screenshot"
	sub = screen.subsurface(x, y, width, height)
	screenshot = pygame.Surface((width, height))
	screenshot.blit(sub, (0, 0))
	return screenshot
    
#resize image down to 1 pixel. Get most dominant color.
def get_dominant_color(pil_img):
	"""
		Get the most dominant color of the image
	"""
	img = pil_img.copy()
	img.convert("RGB")
	img.resize((1, 1), resample=0)
	dominant_color = img.getpixel((0, 0))
	return dominant_color

#
def floor(number_to_round):
	"Return a rounded number. Ex.: 520 => 500; 26 => 20"
	str_number = str(number_to_round)
	#EXAMPLE 510 will give length_string = 3. 90 will give length_string = 2 
	length_string = len(str_number)
	#list comprehension, append first 1..then a list of 0s based on length_string
	#so 510 will give 100. 5100 will give 1000
	str_number = ["1"] + ["0" for _ in range(1, length_string)]
	str_number = "".join(str_number)
	str_number = int(str_number)
	#for example  510//100  will give 5 then multiply by 100 will give 500.
	#510 will return 500.
	floor_result = number_to_round // str_number * str_number
	return floor_result

class Puzzle:
	tiles_positioned_correct = 0 	# a counter how many tiles guessed correctly.In the begining 0 tiles guessed right.
	sounds, winsounds = init("sounds")
	clock = pygame.time.Clock()
	photo = None
	width = 0
	height = 0
	screen = None
	bar = None
	BLACKTILE = None
	
	@staticmethod
	def setValues():
		"""
			Set all values of puzzle.based on image size.
		"""
		global imageSelected
		Puzzle.tiles_positioned_correct = 0
		Puzzle.photo = pygame.image.load(imageSelected)
		Puzzle.width, Puzzle.height = Puzzle.photo.get_size()
		Puzzle.width = floor(Puzzle.width)
		Puzzle.height = floor(Puzzle.height)
		Puzzle.screen = pygame.display.set_mode((Puzzle.width * 3 - Puzzle.width // 2 + 14, Puzzle.height))
		
		pygame.display.set_caption("Puzzle-mania")
		Puzzle.photo.convert()
		Puzzle.bar = pygame.Surface((7, Puzzle.height))
		Puzzle.bar.fill(get_dominant_color(Image.open(imageSelected)))
		Puzzle.BLACKTILE = (get_dominant_color(Image.open(imageSelected)))

class Tile:
	width = 0
	height = 0	
	@staticmethod
	def setValues(level):
		"""
			set tiles based on level, level 1 means we want to have 2*2.
		"""
		Tile.width = Puzzle.width // int(level)
		Tile.height = Puzzle.height // int(level)

def check_if_ok(tile3, tile1, numtile):
	"""
		We are checking if tile put in correct position, and also if puzzle is completed.
	"""
	global rects3, puzzle3, puzzle,imageSelected
	# Check if the images are the same (same color)
	uguale = 0
	for pxh in range(Tile.height):
		for pxw in range(Tile.width):
			if tile3.get_at((pxw, pxh)) ==  tile1.get_at((pxw, pxh)):
				uguale += 1
			else:
				# if there is one pixel that is different it quits
				# they are not equal, so break - avoid time consuming
				break
	pixels = Tile.height * Tile.width
    ###########################################################################
    #                          YOU PUT IT IN THE RIGHT SPOT                   #
    ###########################################################################
	if pixels == uguale:
		print("you got right")
		#pygame.mixer.music.pause()
		#pygame.mixer.Sound.play(choice(Puzzle.winsounds))
		brighten = 32
		tile3.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
		puzzle3[numtile][1] = tile3
		puzzle[numtile][1] = tile3
		Puzzle.tiles_positioned_correct += 1 # Another tile fixed correctly , update counter.
	# Check if the puzzle is finished
	if Puzzle.tiles_positioned_correct == (Puzzle.width // Tile.width) * (Puzzle.height // Tile.height):
		global postCongratulations
		postCongratulations = True
		subprocess.check_output([sys.executable, "congrats.py"])

def blit(part, x, y):
	Puzzle.screen.blit(part, (x, y))

def play(snd):
	"""
		play sound
	"""
	pygame.mixer.Sound.play(Puzzle.sounds[snd])

def get_coordinates(event):
	"""
		get coordinates of event.
	"""
	global coords
	mousex, mousey = event
	mx = ((mousex - 7 - Puzzle.width // 2) // Tile.width ) * Tile.width
	my = (mousey // Tile.height) * Tile.height
	for coord in coords:
		if coord[1] == mx and coord[2] == my:
			return coord

def get_coordinates2(event):
    "Returns the coordinates of the piece you leave on the table"
    global coords
    # mouse coordinates
    mousex, mousey = event
    # transform coordinates into 
    mx = ((mousex - 14 - Puzzle.width - Puzzle.width // 2) // Tile.width) * Tile.width
    my = (mousey // Tile.height) * Tile.height
    # In coord we have all the coordinates of the first correct puzzle
    for coord in coords:
        # if the mouse touches a tile that has the same coordinates
        if coord[1] == mx and coord[2] == my:
            # show the number of the tile
            return coord

class Event_listener():
	"""
		detect all mouse events/movements/drags, and if user quit too.
	"""
	global coords, puzzle2, blacktile, puzzle3, textRect
	drag = 0
	p2pos = 0
	# see in which cadre you picked the tile
	pos3 = False
	scenario = 0
	def check(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					play("click")
                    # Until you press you will see the image
                    # under the mouse arrow icon
					Event_listener.drag = 1
					x, y = event.pos
                    # Avoid working out of the middle area
					if x > Puzzle.width // 2 + 7 and x < Puzzle.width * 2 - Puzzle.width // 2 + 7:
						Event_listener.scenario = 1
						coord = get_coordinates(event.pos)
						if puzzle2[coord[0]][1] == blacktile:
							Event_listener.drag = 0
						else:
                            # check if the mouse is over a tile and
                            # get it into Event...tile
							puzzle_get = puzzle2[coord[0]][1]
							Event_listener.tile = puzzle_get
							puzzle2[coord[0]][1] = blacktile
                            # Memorize the position of the tile
							Event_listener.p2pos = coord[0]
							show_puzzleTwo()
							Event_listener.pos3 = False
					elif x > Puzzle.width * 2 - Puzzle.width // 2 + 7: 
						Event_listener.scenario = 2
						coord2 = get_coordinates2(event.pos)
                        # you picked the tile in the 3rd painting
						if puzzle[coord2[0]][1] == puzzle3[coord2[0]][1] or puzzle3[coord2[0]][1] == blacktile:
							Event_listener.drag = 0
						else:
							Event_listener.pos3 = True
							Event_listener.p3pos = coord2[0] 
    
							tile_in_3o = puzzle3[coord2[0]][1]
							Event_listener.tile = tile_in_3o
							puzzle3[coord2[0]][1] = blacktile
                           
							coord2 = get_coordinates2(event.pos)
							if puzzle3[coord2[0]][1] == blacktile:
								puzzle_get = puzzle3[coord2[0]][1]
					#back button clicked, making playing false so that user returns to main menu.
					elif textRect.collidepoint( event.pos):
						puzzle_get = []
						Event_listener.tile = puzzle_get
						global playing
						playing = False
                                
            # when you mouse up on many tile the tile disappear
			elif event.type == pygame.MOUSEBUTTONUP:
				# just disable getting new titles from the first image. only drag from 2nd to 3rd part.
				if Event_listener.scenario == 0:
					continue
				Event_listener.scenario = 0
				if Event_listener.drag:
					play("click")
					if event.pos[0] > Puzzle.width // 2 + Puzzle.width + 14:
						Event_listener.drag = 0
                        # See where you are leaving the piece
						coord2 = get_coordinates2(event.pos)
                        # Number of the tile where you are putting the piece
						casella = puzzle3[coord2[0]]
						tile3 = casella[1]
						if tile3 == blacktile:
							Event_listener.drag = 0                              
							puzzle3[coord2[0]][1] = Event_listener.tile
							check_if_ok(Event_listener.tile, puzzle[coord2[0]][1], coord2[0])
						elif Event_listener.pos3:
							puzzle3[Event_listener.p3pos][1] = Event_listener.tile
						else:
							self.back_in_place()
					else:
						self.back_in_place()

	def back_in_place(self):
		for n, tile in enumerate(puzzle2):
			if tile[1] == blacktile:
				Event_listener.drag = 0
				puzzle2[n][1] = Event_listener.tile
				break
	def quit(self):
		"Quite pygame and the python interpreter"
		pygame.quit()
		sys.exit()

def create_puzzle():
    "Take the image and makes a puzzle, returns list of pieces and coordinates"
    global puzzle, puzzle2, puzzle3,blacktile,coords, origcoords
    puzzle = []
    puzzle2 = [] # this will be shuffled
    puzzle3 = []
    coords = []
    blit(Puzzle.photo, 0, 0)
    pygame.display.update()
    order = 0
    for m in range(Puzzle.height // Tile.height):
        for n in range(Puzzle.width // Tile.width):
            # grab returns a Surface object
            tile = grab(Puzzle.screen, n * Tile.width, m * Tile.height, Tile.width, Tile.height)
            puzzle.append([order, tile])
            puzzle2.append([order, tile])
            puzzle3.append([order, blacktile])
            # The coordinates of the tiles
            coords.append([order, n * Tile.width, m * Tile.height])
            order += 1
    shuffle(puzzle2)
    origcoords = coords[:]

def show_puzzleOne():
    "This shows the puzzle, if sfl=1, shuffles it"
    global puzzle, coords, origcoords
    rects = []
    coords = origcoords[:]
    screen1 = pygame.Surface((Puzzle.width // 2, Puzzle.height // 2))
    index = 0
    for num_tile, x, y in coords:
        # The tiles are half the normal size
        screen1.blit(pygame.transform.scale(puzzle[index][1], (Tile.width // 2, Tile.height // 2)), (x // 2, y // 2))
        rects.append(pygame.Rect(x + Puzzle.width, y, Tile.width // 2, Tile.height // 2))
        index += 1
    Puzzle.screen.blit(screen1, (0, 0))

def show_puzzleTwo():
    global puzzle2
    rects2 = []
    index = 0
    # the coordinates=[[0, 50, 0], [1, 100, 0]...]
    for num_tile, x, y in coords:
        blit(puzzle2[index][1], x + Puzzle.width // 2 + 7, y)
        index += 1
    draw_grid()

def show_puzzleThree():
	global puzzle3
	rects3 = []
	index = 0
	for num_tile, x, y in coords:
		blit(puzzle3[index][1], x + Puzzle.width * 2 - Puzzle.width // 2 + 14, y)
		index += 1
	draw_grid2()

def draw_grid():
    "Draws the grid. if level 5 = 10x10 for 40x50 tiles"
    def draw_horizzontal():
        x = Puzzle.width // 2 + 7 # always equal to 500
        y = index * Tile.height
        width = Puzzle.width * 2 + 7 - Puzzle.width // 2
        height = index * Tile.height
        pygame.draw.line(Puzzle.screen, (0, 0, 0), (x, y), (width, height), 2)

    def draw_vertical():
        xv = Puzzle.width // 2 + 7 + index * Tile.width
        yv = 0 
        wv = Puzzle.width  // 2 + 7 + index * Tile.width 
        hv = Puzzle.height  
        pygame.draw.line(Puzzle.screen, (0, 0, 0), (xv, yv), (wv, hv), 2)

    for index in range(10):
        draw_horizzontal()
        draw_vertical()

def draw_grid2():
    "Draws the grid .if level 5 = 10x10 for 40x50 tiles"
    def draw_horizzontal():
        x = Puzzle.width * 2 - Puzzle.width // 2 + 14 # always equal to 500
        y = index * Tile.height # goes down by 50, 100 .....
        width = Puzzle.width * 3 - Puzzle.width // 2 + 14 # abscissa 2 = 1500
        height = index * Tile.height # ordered as above 50, 100 ...
        pygame.draw.line(Puzzle.screen, (128, 128, 128, 64), (x, y), (width, height), 1)

    def draw_vertical():
        xv = Puzzle.width * 2 - Puzzle.width // 2+ 14 + index * Tile.width 
        yv = 0 # always starts from height 0 (top)
        wv = Puzzle.width * 2 - Puzzle.width // 2 + 14 + index * Tile.width
        hv = Puzzle.height 
        pygame.draw.line(Puzzle.screen, (128, 128, 128, 128), (xv, yv), (wv, hv), 1)

    for index in range(10):
        draw_horizzontal()
        draw_vertical()

def bars():
    Puzzle.screen.blit(Puzzle.bar, (Puzzle.width // 2, 0))
    Puzzle.screen.blit(Puzzle.bar, (Puzzle.width // 2 + Puzzle.width + 7, 0))

def mainStart(imageUrl,level):
	#you need to call here to start the game, by passing the image path parameter. Also the level.
	global imageSelected,blacktile
	#set the image selected to play jigsaw puzzle game
	imageSelected = imageUrl
	pyzzlemania = Puzzle()
	Puzzle.setValues()
	Tile.setValues(level)
	blacktile = pygame.Surface((Tile.width, Tile.height))
	blacktile.fill(Puzzle.BLACKTILE)
	start()
	
def start():
	"The game begins here"
	global textRect,playing,postCongratulations
	# creates puzzle grabbing pieces from this image
	create_puzzle()
	playing = True
	postCongratulations = False
	while playing:
		Puzzle.screen.fill((0,0,0))
		show_puzzleOne()
		show_puzzleTwo()
		show_puzzleThree()
		bars()      
		try:
			if Event_listener.drag == 1:
				Puzzle.screen.blit(Event_listener.tile, (pygame.mouse.get_pos()[0] - Tile.width // 2, pygame.mouse.get_pos()[1] - Tile.height // 2))
		except:
			pass
		# User input
		Event_listener().check()
		txtMsg = "Back"
		
		# let us add the back button to the game, allow user to return to main menu.
		smallText = pygame.font.Font("freesansbold.ttf", 30)
		yellow = (255,255,187)
		textSurface = smallText.render(txtMsg,True, yellow)
		textSurf,textRect =   textSurface, textSurface.get_rect()
		textRect.center = (Puzzle.width // 4 ,Puzzle.height/2 + Puzzle.height/4)  # to center image
		Puzzle.screen.blit(textSurf, textRect)
		
		pygame.display.update()
		Puzzle.clock.tick(60)
	# resize screen for user to return to menu
	size = (850,880)
	pygame.display.set_mode(size, pygame.RESIZABLE)
	pygame.display.set_caption('Pacific Games: Jigsaw Puzzle')