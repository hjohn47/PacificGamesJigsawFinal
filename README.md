# PacificGamesJigsawFinal
Programming in python final project

You need to install the below for project to work
- pygame
- pillow

To run the game, just run 
python3 main.py

Some feature of the game:
- You can turn the music on or off at first screen menu by clicking space bar 
- You can upload your own image to play puzzle with, given that it should be between 500-700 pixel
- You can download puzzle images from api http://fancycars.atwebpages.com/images.json to add to the game.
- Survey shows up at start of game, and end of it. It surveys your stress level.The results will be saved in a file.
- You can choose the level you want to play. 5 levels available. for ex. level 1 you will only have 2*2 tiles
- Prev, Next buttons to select the image you want to play puzzle
- play button, to play the game with selected image


Puzzle Game
- Has 3 parts. 
- first part the real image + back button to go back. 
- second part the shuffled pieces of the image. 
- third part where you will drag the pieces from 2nd part.
- once you correctly place the pieces, you get congratulations screen for 4 seconds.


The game covered many things we learned in class:
- Calling internet, making API call and parsing the json file ( images to download)
- Writing the results of survey to a file
- When uploading we copy image selected to baseimages folder
- We used both pygame, and tkinter.
- Searching directories ( the baseimages directory), and adding the images in baseimages folder to a list of images we have.
- From our operating systems class, we learned about threading. And when we download images we do it on different thread to avoid the game to be frozen
- Using random, to shuffle pieces.
- List Comprehension, in floor (jigsawpuzzle.py) function.
- Class Attributes (check Puzzle, Tile)
- Keen Framework