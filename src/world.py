#!/usr/bin/python

# System imports
import sys, os, math

# Panda imports
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from direct.task import Task
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.showbase.DirectObject import DirectObject

# Game imports
from globals import *

#---------------------------------------------------------------------#

## Main World Class
class World(DirectObject):
	
	"""
	World Class:
	
	Handels the World and all the things in it.
	"""
	
	def __init__(self):
		
		pass 
		
	def addLevel(self, levelName, levelObject):
		"""
		This method adds created levels to the LEVELS dict{}
		
		@param levelName: String_key for the level.
		@param levelObject: The created level itself.
		"""
		LEVELS[levelName] = levelObject
		
		
	

## MakeLevel Class
class MakeLevel():
	
	"""
	MakeLevel Class:
	
	Handles the creation of levels.
	"""
	
	def __init__(self, levelName, levelModelPath):
		"""
		constructor:
		
		@param levelName: String_Name for the level itself.
		@param levelModelPath: The path to the model file, for the level
		"""
		
		# Set the level name
		self.levelName = levelName
		
		# Load the model for the level
		self.dummylevel = loader.loadModel(levelModelPath)
		self.dummylevel.reparentTo(render)
		
		
		# Setup lights for the level
		
		plight = PointLight('plight')
		plight.setColor(VBase4(0.7, 0.7, 0.7, 1))
		plnp = render.attachNewNode(plight)
		plnp.setPos(0, 0, 5)
		render.setLight(plnp)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
