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
from egg_parse import *
#---------------------------------------------------------------------#

## Main World Class
class World(DirectObject):
	
	"""
	World Class:
	
	Handels the World and all the things in it.
	"""
	
	def __init__(self):
		
		# Testing light: Remove if done
		############################################
		# Setup lights for the level
		plight = PointLight('plight')
		plight.setColor(VBase4(0.7, 0.7, 0.7, 1))
		plnp = render.attachNewNode(plight)
		plnp.setPos(0, 0, 8)
		render.setLight(plnp)
		############################################
		
		# Keeps all geoms under this node: Game_Objects
		self.master_GeomNP = render.attachNewNode('MASTER_GEOM')
		# Keeps all Lights under this node
		self.master_LightNP = render.attachNewNode('MASTER_LIGHTS')
		
		# subnodes for Game_Objects
		self.sensorNP = self.master_GeomNP.attachNewNode('SENSORS')
		self.doorNP = self.master_GeomNP.attachNewNode('DOORS')
		self.playerNP = self.master_GeomNP.attachNewNode('PLAYER')
		self.suitNP = self.master_GeomNP.attachNewNode('SUIT')
		self.triggerNP = self.master_GeomNP.attachNewNode('TRIGGERS')
		self.itemNP = self.master_GeomNP.attachNewNode('ITEMS')
		self.screenNP = self.master_GeomNP.attachNewNode('SCREENS')
		self.particlesNP = self.master_GeomNP.attachNewNode('PARTICLES')
		self.decorNP = self.master_GeomNP.attachNewNode('DECOR')
		self.visLightsNP = self.master_GeomNP.attachNewNode('VIS_LIGHTS')
		
		# subnodes for lights
		self.lightsNP = self.master_LightNP.attachNewNode('LIGHTS')
		
		
		
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
	
	def __init__(self, _base, _world, levelName, levelModelPath):
		"""
		constructor:
		
		@param levelName: String_Name for the level itself.
		@param levelModelPath: The path to the model file, for the level
		"""
		# Base Class
		self._base = _base
		
		# Base World
		self._world = _world
		
		# Set the level name
		self.levelName = levelName
		
		# Load the model for the level
		self.level = loader.loadModel(levelModelPath)
		
		# Parse the egg model file and setup the level
		Parse(self._base, self._world, self.level)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
