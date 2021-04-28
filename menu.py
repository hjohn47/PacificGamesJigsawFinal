#!/usr/bin/env python3
"""
	Main menu screen.
"""

import pygame
import random
import math
from pygame import mixer
import os
import sys
import subprocess
import platform
from pygame.locals import *
import jigsawpuzzle
from os import path
import json
from urllib.request import urlopen
import threading
import shutil

__author__ = "Hailey Johnson, Krikor Herlopian, Charitha Sree Jayaramireddy , Syrina Haldiman and Tatiyana Bramwell"
__copyright__ = "Copyright 2021, University of New Haven Final Project"




level = 1 #number of tiles
music_on = True
#one place to store the positions of buttons and their text. Modify here to change their placing, without touching the logic.
dictInstructionButton = {'text': "Instructions", 'x': 35, 'y':125, 'w': 230, 'h':60}
dictUploadImageButton = {'text': "Upload Image", 'x': 35, 'y':195, 'w': 230, 'h':60}
dictDownloadImageButton = {'text': "Download", 'x': 35, 'y':265, 'w': 230, 'h':60}
dictSurveyButton = {'text': "Survey Results", 'x': 35, 'y':335, 'w': 230, 'h':60}
dictLevelButton = {'text': "Level", 'x': 35, 'y':405, 'w': 230, 'h':60}
dictBackButton = {'text': "Back",'x': 300, 'y':780, 'w': 100, 'h':60}
dictNextButton = {'text': "Next",'x': 700, 'y':780, 'w': 100, 'h':60}
dictPuzzleButton = {'text': "Play", 'x': 450, 'y':780, 'w': 200, 'h':60}

# list of images in basimages folder, and also downloaded from net.
lstOfPics = []	
selectedPath = 0	# the image selected index in lstOfPics.
selectedImg = None
downloading = False	#indicates if download button clicked or not. If clicked we will use this to disable downloading while another downloading is going on.



yellow = (255,252,187)
white = (255,255,255)
black = (0,0,0)

def mainStart():
	global background, window
	pygame.init()
	size = (850,880)
	window = pygame.display.set_mode(size, pygame.RESIZABLE)
	pygame.display.set_caption('Pacific Games: Jigsaw Puzzle')

	icon = pygame.image.load("pacificicon.png").convert_alpha()
	pygame.display.set_icon(icon)

	background = pygame.image.load("MAIN.jpg").convert()

	#play relaxing music during the game.
	mixer.music.load("sounds/Relaxing_Green_Nature.mp3")
	mixer.music.play(-1)                #play on loop
	textboxGroup = pygame.sprite.OrderedUpdates()
	gameloop()

def text_objects (text, font):
    textSurface = font.render(text,True, black)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):   #ic inactive color, ac active color
	global selectedPath,lstOfPics
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
    # print(mouse)
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(background, ac, (x, y, w, h))
		if click[0] == 1 and action != None:
			if action == "instructionsfile":
                #open in wordpad for windows and textedit for mac
				if platform.system() == 'Darwin':  # macOS
					subprocess.call(('open', "Instructions.pdf"))    #could also use text file
				elif platform.system() == 'Windows':  # Windows
					os.startfile("Instructions.pdf")
				else:  # linux variants
					subprocess.call(('xdg-open', "Instructions.pdf"))
	else:
		pygame.draw.rect(background, ic, (x, y, w, h))

	smallText = pygame.font.Font("freesansbold.ttf", 30)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x + (w / 2)), (y + (h / 2)))  # to center image
	background.blit(textSurf, textRect)

#puzzle selected to be played drawn on screen.		
def drawPuzzleSelected():
	global selectedImg,lstOfPics,selectedPath
	if len(lstOfPics) > 0:
		selectedImg = pygame.image.load(lstOfPics[selectedPath]).convert()		
		selectedImg = pygame.transform.scale(selectedImg, (500, 500))
		background.blit(selectedImg, (300,50))

#download puzzles from internet
def downloadImages():
	global downloading
	print("downloading...")
	#call api to get list of all images
	page = "http://fancycars.atwebpages.com/images.json"
	req = urlopen(page)
	data = json.load(req)
	#if puzzles folder doesnt exist create it.
	if not os.path.exists("baseimages"):
		os.makedirs("baseimages")

	base_dir = path.join(path.dirname(path.realpath(__file__)), "baseimages")
	#loop over json data returned, and download image by image to puzzles folder.
	for img in data:
		resource = urlopen(img['img'])	
		# if image already downloaded , dont download again.
		if not os.path.exists(base_dir+"/"+img['name']):
			with open(path.join(base_dir, img['name']),"wb") as file: 
				file.write(resource.read())
				lstOfPics.append(base_dir+"/"+img['name'])
		else:
			print(img['name'], " image exists already")
	downloading = False
	
#check if baseimages folder exists, if yes lets find images in them.
def searchImages():
	dir = "baseimages"
	if os.path.exists(dir):
		findImages(dir)

#loop over directory, to find images and add them to lstOfPics. First image will be displayed.
def findImages(d):
	global selectedImg,lstOfPics,selectedPath
	for path in os.listdir(d):
		full_path = os.path.join(d, path)
		if os.path.isfile(full_path):
			head,tail = os.path.split(full_path)
			if tail != ".DS_Store":
				lstOfPics.append(full_path)
				
#opens a dialog for user to select a file to add to the game.
def choose_a_file():
	try:
		global lstOfPics,selectedPath
		image_file_name = subprocess.check_output([sys.executable, "filedialog.py"])
		encoding = 'utf-8'
		image_file_name = image_file_name.decode(encoding).rstrip()
		if image_file_name:
			lstOfPics.append(image_file_name)
			selectedPath = len(lstOfPics)-1
			print(image_file_name)
			#copy the file selected to baseimages folder
			shutil.copy2(image_file_name, "baseimages")
		drawPuzzleSelected()
	except:
		pass
	
#user chooses level of game, number of titles.	
def choose_a_level():
	try:
		global level
		new_level = subprocess.check_output([sys.executable, "level.py"])
		encoding = 'utf-8'
		new_level = new_level.decode(encoding).rstrip()
		if new_level:
			level = new_level
	except:
		pass

#turn music on/off
def play_stop_music():
	global music_on
	music_on = not music_on
	if music_on:
		mixer.music.load("sounds/Relaxing_Green_Nature.mp3")
		mixer.music.play(-1)                #play on loop
	else:
		mixer.music.pause()   
		
		
def gameloop():
    #game loop
	global selectedPath,lstOfPics,level
	running = True
	lstOfPics = []
	selectedPath = 0
	#search for images in folder base images.
	searchImages()
	drawPuzzleSelected()
	
	dictDownloadImageButton['x+w'] = dictDownloadImageButton['x'] + dictDownloadImageButton['w']
	dictDownloadImageButton['y+h'] = dictDownloadImageButton['y'] + dictDownloadImageButton['h']
	dictBackButton['x+w'] = dictBackButton['x'] + dictBackButton['w']
	dictBackButton['y+h'] = dictBackButton['y'] + dictBackButton['h']
	dictNextButton['x+w'] = dictNextButton['x'] + dictNextButton['w']
	dictNextButton['y+h'] = dictNextButton['y'] + dictNextButton['h']
	dictPuzzleButton['x+w'] = dictPuzzleButton['x'] + dictPuzzleButton['w']
	dictPuzzleButton['y+h'] = dictPuzzleButton['y'] + dictPuzzleButton['h']
	dictUploadImageButton['x+w'] = dictUploadImageButton['x'] + dictUploadImageButton['w']
	dictUploadImageButton['y+h'] = dictUploadImageButton['y'] + dictUploadImageButton['h']
	dictSurveyButton['x+w'] = dictSurveyButton['x'] + dictSurveyButton['w']
	dictSurveyButton['y+h'] = dictSurveyButton['y'] + dictSurveyButton['h']
	dictLevelButton['x+w'] = dictLevelButton['x'] + dictLevelButton['w']
	dictLevelButton['y+h'] = dictLevelButton['y'] + dictLevelButton['h']	
	
	#read lev.txt, and set level to it.
	with open("lev.txt") as file: 
		level = int(file.readline())
	index = 0
	while running:
		if index == 4:
			subprocess.check_output([sys.executable, "stressSurvey.py"])
		index += 1
		window.fill((0, 0, 0))
		window.blit(background, (0, 0))
		for event in pygame.event.get():
			mouse = pygame.mouse.get_pos()
			if event.type == pygame.KEYDOWN:
				#space pressed play or stop the music
				if event.key == pygame.K_SPACE:
					play_stop_music()
			elif event.type == pygame.QUIT:
				running = False
				subprocess.check_output([sys.executable, "stressSurvey.py"])
			elif event.type == pygame.MOUSEBUTTONDOWN:
				#user clicked next.Update selectedpath by 1.and redraw new image 
				if dictNextButton['x+w'] > mouse[0] > dictNextButton['x'] and dictNextButton['y+h'] > mouse[1] > dictNextButton['y']:
					if len(lstOfPics) > (selectedPath+1):
						selectedPath = selectedPath +1
					drawPuzzleSelected()
				#user clicked back . Update selectedpath by minus 1. and redraw new image 
				elif dictBackButton['x+w'] > mouse[0] > dictBackButton['x'] and dictBackButton['y+h'] > mouse[1] > dictBackButton['y']:	
					if selectedPath > 0:
						selectedPath = selectedPath - 1
					else:
						selectedPath = 0
					drawPuzzleSelected()
				# user clicks text puzzle to start game.
				elif dictPuzzleButton['x+w'] > mouse[0] > dictPuzzleButton['x'] and dictPuzzleButton['y+h'] > mouse[1] > dictPuzzleButton['y']:
					#make sure selectedPath in range of lstOfPics. We dont want it to crash array out of bound exception	
					if selectedPath < len(lstOfPics):
						if int(level) == 1:
							jigsawpuzzle.mainStart(lstOfPics[selectedPath], 2)
						elif int(level) == 2:
							jigsawpuzzle.mainStart(lstOfPics[selectedPath], 5)
						elif int(level) == 3:
							jigsawpuzzle.mainStart(lstOfPics[selectedPath], 6)
						elif int(level) == 4:
							jigsawpuzzle.mainStart(lstOfPics[selectedPath], 8)
						elif int(level) == 5:
							jigsawpuzzle.mainStart(lstOfPics[selectedPath], 10)
				#download images from internet, since download button is clicked. 
				elif dictDownloadImageButton['x+w'] > mouse[0] > dictDownloadImageButton['x'] and dictDownloadImageButton['y+h'] > mouse[1] > dictDownloadImageButton['y']:	
					global downloading
					#making sure only one download is going on.
					if not downloading:
						downloading = True
						#since downloading is long operation, we do it in different thread.
						th = threading.Thread(target=downloadImages)
						th.start()
				#upload image button clicked
				elif dictUploadImageButton['x+w'] > mouse[0] > dictUploadImageButton['x'] and dictUploadImageButton['y+h'] > mouse[1] > dictUploadImageButton['y']:	
					file_name = choose_a_file()
				#survey
				elif dictSurveyButton['x+w'] > mouse[0] > dictSurveyButton['x'] and dictSurveyButton['y+h'] > mouse[1] > dictSurveyButton['y']:	
					#open survey
					if platform.system() == 'Darwin':  # macOS
						subprocess.call(('open', "stressSurveyResults.txt"))  # could also use text file
					elif platform.system() == 'Windows':  # Windows
						os.startfile("stressSurveyResults.txt")
					else:  # linux variants
						subprocess.call(('xdg-open', "stressSurveyResults.txt"))
				#user clicked level button to choose a new level
				elif dictLevelButton['x+w'] > mouse[0] > dictLevelButton['x'] and dictLevelButton['y+h'] > mouse[1] > dictLevelButton['y']:	
					choose_a_level()
				
		dictLevelButton['text'] = "Level "+str(level)
        #if downloading , display wait in button. And its unclikable.
        #User cannot download while another download is going on.      
		if downloading:
			dictDownloadImageButton['text'] = "Wait"
		else:
			dictDownloadImageButton['text'] = "Download"
		
			
		button(dictLevelButton['text'], dictLevelButton['x'],dictLevelButton['y'],dictLevelButton['w'],dictLevelButton['h'], yellow, white) 
		button(dictSurveyButton['text'], dictSurveyButton['x'],dictSurveyButton['y'],dictSurveyButton['w'],dictSurveyButton['h'], yellow, white) 
		button(dictDownloadImageButton['text'], dictDownloadImageButton['x'],dictDownloadImageButton['y'],dictDownloadImageButton['w'],dictDownloadImageButton['h'], yellow, white) 
		button(dictUploadImageButton['text'], dictUploadImageButton['x'],dictUploadImageButton['y'],dictUploadImageButton['w'],dictUploadImageButton['h'], yellow, white) #"upload")
		button(dictInstructionButton['text'],dictInstructionButton['x'],dictInstructionButton['y'],dictInstructionButton['w'],dictInstructionButton['h'], yellow, white, "instructionsfile")
		button(dictPuzzleButton['text'], dictPuzzleButton['x'], dictPuzzleButton['y'], dictPuzzleButton['w'], dictPuzzleButton['h'], yellow, white, "play")
		button(dictBackButton['text'], dictBackButton['x'], dictBackButton['y'], dictBackButton['w'], dictBackButton['h'], yellow, white,"back")  #back button
		button(dictNextButton['text'], dictNextButton['x'], dictNextButton['y'], dictNextButton['w'], dictNextButton['h'], yellow, white,"next")  #next button
		pygame.display.update()
		pygame.time.Clock().tick(60)






