#!/usr/bin/python

"""
See LICENSE in main folder.
---------------------------


* This file contains the main class and methods to start the game.


---------------------------
Developers:

- MJ-meo-dmt
"""

# System imports
import sys
import os

# Panda Engine imports
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""	
	window-title Ecliptic - Space
	fullscreen 0
	win-size 1024 768
	cursor-hidden 0
	sync-video 0
	show-frame-rate-meter 1
"""
)
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.core import WindowProperties, Camera
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.DirectObject import DirectObject

# Game imports
from world import *
from player import *
#from collisions import *
from globals import *
from physics import *



#----------------------------------------------------------------------#

class Main(ShowBase):
	
	def __init__(self):
		ShowBase.__init__(self)

		print "Running game..."
		
		# Needs fix
		# Hide the cursor
		props = WindowProperties() 
		props.setCursorHidden(True) 
		self.win.requestProperties(props)
		
		# Master Instances
		self.WorldClass = World()
		self.PhysicsClass = Physics(self, self.WorldClass)
		self.PlayerClass = Player()
		
		# init the main methods
		self.init_player()
		self.init_world()
		
		# Debug: Show the scene graph.
		self.render.ls()
		print sys.getsizeof(OBJECTS)
		
		
		
		
	def init_world(self):
		
		self.level1 = MakeLevel(self, self.PhysicsClass, self.WorldClass, "Level1", "../assets/models/advancelevel2.egg")
		
		
	def init_player(self):

		self.playerPC = MakePlayer(self, self.PhysicsClass, self.WorldClass, 'Player')
		
		self.PlayerClass.addEntity("PC", self.playerPC)
	    

game = Main()
game.run()



#### QUICK THOUGHTS :P














