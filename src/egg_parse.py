## This file will parse egg files for TAG's.

# System imports


# Panda imports
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

# Game imports
from globals import *
from gameprop import *


#----------------------------------------------------------------------#

# Main egg parser.
# For all visual objects
class ParseMain(NodePath):
	
    """
    Parse Class:
    
    Handles the parsing of egg files.
    Sorts each object/Node found into a specific object/Type
    
    Constructor:
    @param _base: Main base class
    @param _physics: Main physics class 
    @param _world: Main world class
    @param _model: The egg file to be parsed, send from world.py under MakeLevel.
    """
    
    def __init__(self, _base, _physics, _world, _model):
		NodePath.__init__(self, 'object')
		# Base class
		self._base = _base
	
		# Base Physics
		self._physics = _physics
	
		# Base world
		self._world = _world
	
		# Keep track of num_of_objects
		num_sensors = 0
		num_doors = 0
		num_triggers = 0
		num_lights = 0
		num_items = 0
		num_particles = 0
	
		# Get the model to be parsed:
		self._model = _model
	
		# Find all the objects inside the egg file, and save them.
		self.objects = self._model.findAllMatches('**')
	
	
		# Now check all objects and then init the class for that tag:
		for object in self.objects:
		
			"""
			@param [key]: The name of the object.
			"""
			#-------------------------------------------------------------------------------------------#
			## LEVEL SETUP
			#
			## ROOM
			
			if object.hasTag('ROOM'):
				OBJECTS['ROOM'][object.getTag('ROOM')] = GameObject(self._base, self._physics, self._world, self._model, object)
			
			#-------------------------------------------------------------------------------------------#
			## GAME OBJECTS / LOGIC
			
			if object.hasTag('SENSOR'):
				OBJECTS['SENSOR'][object.getTag('SENSOR')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_sensors += 1
			
			if object.hasTag('DOOR'):
				OBJECTS['DOOR'][object.getTag('DOOR')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_doors += 1
			
			if object.hasTag('PLAYER'):
				OBJECTS['PLAYER'][object.getTag('PLAYER')] = GameObject(self._base, self._physics, self._world, self._model, object)
			
			if object.hasTag('TRIGGER'):
				OBJECTS['TRIGGER'][object.getTag('TRIGGER')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_triggers += 1
			
			if object.hasTag('LIGHT'):
				OBJECTS['LIGHT'][object.getTag('LIGHT')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_lights += 1
			
			if object.hasTag('ITEM'):
				OBJECTS['ITEM'][object.getTag('ITEM')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_items += 1
			
			if object.hasTag('SCREEN'):
				OBJECTS['SCREEN'][object.getTag('SCREEN')] = GameObject(self._base, self._physics, self._world, self._model, object)
			
			if object.hasTag('PARTICLES'):
				OBJECTS['PARTICLES'][object.getTag('PARTICLES')] = GameObject(self._base, self._physics, self._world, self._model, object)
				num_particles += 1
			
			if object.hasTag('SUIT'):
				OBJECTS['SUIT'][object.getTag('SUIT')] = GameObject(self._base, self._physics, self._world, self._model, object)
			
			if object.hasTag('DECOR'):
				OBJECTS['DECOR'][object.getTag('DECOR')] = GameObject(self._base, self._physics, self._world, self._model, object)

