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
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.core import WindowProperties, Camera
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.DirectObject import DirectObject

# Game imports
from world import *
from player import *
from collisions import *
from globals import *



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
		
		# init the main methods
		self.init_player()
		self.init_collisions()
		self.init_world()
		self.init_input()
		
	def init_world(self):
		
		self.WorldClass = World()
		
		self.level1 = MakeLevel('level', "../assets/models/stage1")
		self.testWall = MakeLevel('wall', "../assets/models/wall")
		
		self.WorldClass.addLevel('Level', self.level1)
		self.WorldClass.addLevel('Wall', self.testWall)
		LEVELS['Wall'].dummylevel.setTwoSided(True)
		
		
	def init_player(self):
		
		## Make the actor and add it to the entity dict.
		self.PlayerClass = Player()
		
		self.playerPC = MakePlayer("PC_Player")
		
		self.PlayerClass.addEntity("PC", self.playerPC)
		
	def init_collisions(self):
	    
		# Setup collisions
		self.CollisionClass = Collisions()
		
	def init_input(self):
		
		# Setup the controls
		self.playerControl = PlayerInput()
		
		
		
	
	
game = Main()
game.run()
















